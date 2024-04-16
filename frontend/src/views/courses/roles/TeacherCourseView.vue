<script setup lang="ts">
import Title from '@/components/layout/Title.vue';
import ProjectList from '@/components/projects/ProjectList.vue';
import TeacherAssistantList from '@/components/teachers_assistants/TeacherAssistantList.vue';
import ProjectCreateButton from '@/components/projects/ProjectCreateButton.vue';
import TeacherAssistantUpdateButton from '@/components/teachers_assistants/TeacherAssistantUpdateButton.vue';
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
import { ref, watch } from 'vue';

/* Props */
const props = defineProps<{
    course: Course;
}>();

/* Composable injections */
const confirm = useConfirm();
const { t } = useI18n();
const { cloneCourse } = useCourses();
const { projects, getProjectsByCourse } = useProject();

/* State for the confirm dialog to clone a course */
const cloneAssistants = ref<boolean>(false);
const cloneTeachers = ref<boolean>(false);

/* Methods */
async function handleClone(): Promise<void> {
    // Show a confirmation dialog before cloning the course
    confirm.require({
        message: t('confirmations.clone_course'),
        header: t('views.courses.clone'),
        accept: () => {
            cloneCourse(props.course.id, cloneAssistants.value, cloneTeachers.value);
        },
        reject: () => {},
    });
}

watch(() => props.course, async () => {
    await getProjectsByCourse(props.course.id);
}, { immediate: true });
</script>

<template>
    <!-- Course heading -->
    <div class="flex justify-content-between align-items-center mb-6">
        <!-- Course title -->
        <Title class="m-0">{{ props.course.name }}</Title>

        <ButtonGroup class="flex align-items-center space-x-2">
            <!-- Update course button -->
            <div v-tooltip.top="t('views.courses.edit')">
                <RouterLink :to="{ name: 'course-edit', params: { courseId: props.course.id } }">
                    <Button
                        :icon="PrimeIcons.PENCIL"
                        icon-pos="right"
                        class="custom-button"
                        style="height: 51px; width: 51px; margin-right: 10px"
                    />
                </RouterLink>
            </div>

            <!-- Clone button to clone the course -->
            <div v-tooltip.top="t('views.courses.clone')">
                <ConfirmDialog>
                    <template #container="{ message, acceptCallback, rejectCallback }">
                        <div class="flex flex-column p-5 surface-overlay border-round" style="max-width: 600px">
                            <span class="font-bold text-2xl">{{ message.header }}</span>
                            <p class="mb-4">{{ message.message }}</p>
                            <div class="flex items-center mb-4">
                                <label for="cloneTeachers" class="mr-2">{{ t('views.courses.clone_teachers') }}</label>
                                <InputSwitch v-model="cloneTeachers" id="cloneTeachers" class="p-inputswitch-sm" />
                            </div>
                            <div class="flex items-center mb-4">
                                <label for="cloneAssistants" class="mr-2">{{
                                    t('views.courses.clone_assistants')
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
        </ButtonGroup>
    </div>
    <!-- Description -->
    <p>{{ props.course.description }}</p>
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
    <ProjectList :projects="projects" />

    <!-- Heading for teachers and assistants -->
    <div class="flex justify-content-between align-items-center my-6">
        <Title class="m-0">{{ t('views.courses.teachers_and_assistants.title') }}</Title>

        <div v-tooltip.top="t('views.courses.teachers_and_assistants.edit')">
            <TeacherAssistantUpdateButton :course="props.course" />
        </div>
    </div>
    <!-- List with teachers and assistants -->
    <TeacherAssistantList :course="props.course" :users="course.teachers.concat(course.assistants)" />
</template>

<style scoped lang="scss"></style>
