<script setup lang="ts">
import Title from '@/views/layout/Title.vue';
import ProjectList from '@/components/projects/ProjectList.vue';
import TeacherAssistantList from '@/components/instructors/TeacherAssistantList.vue';
import ProjectCreateButton from '@/components/projects/ProjectCreateButton.vue';
import TeacherAssistantUpdateButton from '@/components/instructors/TeacherAssistantUpdateButton.vue';
import ShareCourseButton from '@/components/courses/ShareCourseButton.vue';
import Button from 'primevue/button';
import ButtonGroup from 'primevue/buttongroup';
import InputSwitch from 'primevue/inputswitch';
import ConfirmDialog from 'primevue/confirmdialog';
import { useConfirm } from 'primevue/useconfirm';
import { type Course } from '@/types/Course.ts';
import { useI18n } from 'vue-i18n';
import { RouterLink } from 'vue-router';
import { PrimeIcons } from 'primevue/api';
import { useCourses } from '@/composables/services/course.service';
import { useProject } from '@/composables/services/project.service.ts';
import { computed, ref } from 'vue';
import { watchImmediate } from '@vueuse/core';

/* Props */
const props = defineProps<{
    course: Course;
}>();

/* Composable injections */
const confirm = useConfirm();
const { t } = useI18n();
const { cloneCourse } = useCourses();
const { projects, getProjectsByCourse } = useProject();

/* State */
const instructors = computed(() => {
    return props.course.teachers.concat(props.course.assistants);
});

/* State for the confirm dialog to clone a course */
const cloneAssistants = ref<boolean>(false);
const cloneTeachers = ref<boolean>(false);

/**
 * Clones the course with the given ID.
 */
async function handleClone(): Promise<void> {
    // Show a confirmation dialog before cloning the course
    confirm.require({
        message: t('confirmations.cloneCourse'),
        header: t('views.courses.clone'),
        accept: () => {
            cloneCourse(props.course.id, cloneAssistants.value, cloneTeachers.value);
        },
        reject: () => {},
    });
}

/**
 * Watch for changes in the course ID and fetch the projects for the course.
 */
watchImmediate(
    () => props.course.id,
    async (courseId: string) => {
        await getProjectsByCourse(courseId);
    },
);
</script>

<template>
    <!-- Course heading -->
    <div class="flex justify-content-between align-items-center mb-6">
        <!-- Course title -->
        <Title class="m-0">{{ props.course.name }}</Title>

        <ButtonGroup class="flex align-items-center gap-2">
            <!-- Update course button -->
            <div v-tooltip.top="t('views.courses.edit')">
                <RouterLink :to="{ name: 'course-edit', params: { courseId: props.course.id } }">
                    <Button
                        :icon="PrimeIcons.PENCIL"
                        icon-pos="right"
                        class="custom-button"
                        style="height: 51px; width: 51px"
                    />
                </RouterLink>
            </div>

            <!-- Clone button to clone the course -->
            <div v-tooltip.top="t('views.courses.clone')">
                <ConfirmDialog :key="props.course.id">
                    <template #container="{ message, acceptCallback, rejectCallback }">
                        <div class="flex flex-column p-5 surface-overlay border-round" style="max-width: 600px">
                            <span class="font-bold text-2xl">{{ message.header }}</span>
                            <p class="mb-4">{{ message.message }}</p>

                            <div class="flex items-center mb-4">
                                <label for="cloneTeachers" class="mr-2">{{ t('views.courses.cloneTeachers') }}</label>
                                <InputSwitch v-model="cloneTeachers" id="cloneTeachers" class="p-inputswitch-sm" />
                            </div>
                            <div class="flex items-center mb-4">
                                <label for="cloneAssistants" class="mr-2">{{
                                    t('views.courses.cloneAssistants')
                                }}</label>
                                <InputSwitch v-model="cloneAssistants" id="cloneAssistants" class="p-inputswitch-sm" />
                            </div>
                            <div class="flex gap-2 justify-content-end">
                                <Button outlined rounded @click="rejectCallback">{{ t('primevue.cancel') }}</Button>
                                <Button @click="acceptCallback" rounded>{{ t('views.courses.clone') }}</Button>
                            </div>
                        </div>
                    </template>
                </ConfirmDialog>
                <Button
                    :icon="PrimeIcons.CLONE"
                    icon-pos="right"
                    class="custom-button"
                    style="height: 51px; width: 51px"
                    @click="handleClone()"
                />
            </div>

            <!-- Share button to create a invitation link, only if the course is private -->
            <ShareCourseButton :course="props.course" v-if="props.course.private_course" />
        </ButtonGroup>
    </div>

    <!-- Description -->
    <div v-html="props.course.description" />

    <!-- Project heading -->
    <div class="flex justify-content-between align-items-center my-6">
        <!-- Project list title -->
        <Title class="m-0">{{ t('views.dashboard.projects') }}</Title>

        <!-- Create project button -->
        <div v-tooltip.top="t('views.projects.create')">
            <ProjectCreateButton :courses="[props.course]" />
        </div>
    </div>

    <!-- Project list body -->
    <ProjectList :projects="projects">
        <template #empty>
            <p>
                {{ t('views.courses.noProjects') }}
            </p>

            <ProjectCreateButton :courses="[course]" :label="t('components.button.createProject')" />
        </template>
    </ProjectList>

    <!-- Heading for teachers and assistants -->
    <div class="flex justify-content-between align-items-center my-6">
        <Title class="m-0">{{ t('views.courses.teachersAndAssistants.title') }}</Title>

        <div v-tooltip.top="t('views.courses.teachersAndAssistants.edit')">
            <TeacherAssistantUpdateButton :course="props.course" />
        </div>
    </div>
    <!-- List with teachers and assistants -->
    <TeacherAssistantList :course="props.course" :users="instructors" />
</template>

<style lang="scss"></style>
