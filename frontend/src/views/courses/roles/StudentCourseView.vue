<script setup lang="ts">
import Title from '@/components/layout/Title.vue';
import Button from 'primevue/button';
import ProjectList from '@/components/projects/ProjectList.vue';
import TeacherAssistantList from '@/components/teachers_assistants/TeacherAssistantList.vue';
import { type Course } from '@/types/Course.ts';
import { useI18n } from 'vue-i18n';
import ConfirmDialog from 'primevue/confirmdialog';
import { useConfirm } from 'primevue/useconfirm';
import { useStudents } from '@/composables/services/student.service';
import { useAuthStore } from '@/store/authentication.store.ts';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';
import { useProject } from '@/composables/services/project.service.ts';
import { computed } from 'vue';
import { watchImmediate } from '@vueuse/core';

/* Props */
const props = defineProps<{
    course: Course;
}>();

/* Composable injections */
const confirm = useConfirm();
const { user } = storeToRefs(useAuthStore());
const { t } = useI18n();
const { studentLeaveCourse } = useStudents();
const { refreshUser } = useAuthStore();
const { projects, getProjectsByCourse } = useProject();
const { push } = useRouter();

/* State */
const instructors = computed(() => {
    return props.course.teachers.concat(props.course.assistants);
});

const visibleProjects = computed(() => projects.value?.filter((project) => project.visible) ?? null);

/**
 * Leave the course as a student.
 */
async function leaveCourse(): Promise<void> {
    // Show a confirmation dialog before leaving the course, to prevent accidental clicks
    confirm.require({
        message: t('confirmations.leaveCourse'),
        header: t('views.courses.leave'),
        accept: () => {
            (async () => {
                if (user.value !== null) {
                    // Leave the course
                    await studentLeaveCourse(props.course.id, user.value.id);

                    // Refresh the user so the course is removed from the user's courses
                    await refreshUser();

                    // Redirect to the dashboard
                    await push({ name: 'dashboard' });
                }
            })();
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
    </div>

    <!-- Description -->
    <div v-html="props.course.description" />

    <!-- Project heading -->
    <div class="flex justify-content-between align-items-center my-6">
        <!-- Project list title -->
        <Title class="m-0">{{ t('views.dashboard.projects') }}</Title>
    </div>

    <!-- Project list body -->
    <ProjectList :projects="visibleProjects">
        <template #empty>
            <p>
                {{ t('views.courses.noProjects') }}
            </p>
        </template>
    </ProjectList>

    <!-- Heading for teachers and assistants -->
    <div class="flex justify-content-between align-items-center my-6">
        <Title class="m-0">{{ t('views.courses.teachersAndAssistants.title') }}</Title>
    </div>

    <!-- List with teachers and assistants -->
    <TeacherAssistantList :course="props.course" :users="instructors" />

    <!-- Button to leave the course -->
    <div class="text-right mt-6">
        <ConfirmDialog>
            <template #container="{ message, acceptCallback, rejectCallback }">
                <div class="flex flex-column p-5 surface-overlay border-round" style="max-width: 600px">
                    <span class="font-bold text-2xl">{{ message.header }}</span>
                    <p class="mb-4">{{ message.message }}</p>
                    <div class="flex gap-2 justify-content-end">
                        <Button outlined rounded @click="rejectCallback">{{ t('primevue.cancel') }}</Button>
                        <Button @click="acceptCallback" rounded>{{ t('views.courses.leave') }}</Button>
                    </div>
                </div>
            </template>
        </ConfirmDialog>

        <Button @click="leaveCourse" icon="pi pi-sign-out" :label="t('views.courses.leave')"></Button>
    </div>
</template>

<style scoped lang="scss"></style>
