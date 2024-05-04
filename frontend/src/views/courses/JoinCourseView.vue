<script setup lang="ts">
import BaseLayout from '@/components/layout/base/BaseLayout.vue';
import Title from '@/components/layout/Title.vue';
import Button from 'primevue/button';
import TeacherAssistantList from '@/components/teachers_assistants/TeacherAssistantList.vue';
import ConfirmDialog from 'primevue/confirmdialog';
import { useConfirm } from 'primevue/useconfirm';
import { onMounted, computed } from 'vue';
import { useAssistant } from '@/composables/services/assistant.service';
import { useTeacher } from '@/composables/services/teacher.service';
import { useCourses } from '@/composables/services/course.service.ts';
import { useStudents } from '@/composables/services/student.service';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/store/authentication.store.ts';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';

/* Service injection */
const { t } = useI18n();
const confirm = useConfirm();
const { refreshUser } = useAuthStore();
const { user } = storeToRefs(useAuthStore());
const { params } = useRoute();
const { push } = useRouter();
const { course, getCourseByID } = useCourses();
const { assistants, getAssistantsByCourse } = useAssistant();
const { teachers, getTeachersByCourse } = useTeacher();
const { studentJoinCourse } = useStudents();

/* State */
const instructors = computed(() => {
    if (course.value !== null) {
        if (course.value.teachers !== null && course.value.assistants !== null) {
            return course.value.teachers.concat(course.value.assistants);
        }
    }

    return null;
});

/**
 * Join the course as a student.
 */
 async function joinCourse(): Promise<void> {
    // Show a confirmation dialog before joining the course, to prevent accidental clicks
    confirm.require({
        message: t('confirmations.joinCourse'),
        header: t('views.courses.enroll'),
        accept: (): void => {
            if (user.value !== null && course.value !== null) {
                // Join the course
                studentJoinCourse(course.value.id, user.value.id).then(() => {
                    // Refresh the user so the course is added to the user's courses
                    refreshUser();
                    // Redirect to the dashboard
                    push({ name: 'dashboard' });
                });
            }
        },
        reject: () => {},
    });
}

onMounted(async () => {
    await getCourseByID(params.courseId as string);

    console.log(course.value);

    // Get assistants and teachers
    if (course.value !== null) {
        await getAssistantsByCourse(course.value.id);
        await getTeachersByCourse(course.value.id);

        // Set the course's assistants and teachers
        course.value.assistants = assistants.value ?? [];
        course.value.teachers = teachers.value ?? [];
    }
});
</script>

<template>
    <BaseLayout>
        <!-- Course heading -->
        <div class="flex justify-content-between align-items-center mb-6">
            <!-- Course title -->
            <Title class="m-0">{{ course?.name }}</Title>

            
            <!-- Button to join the course -->
            <div class="text-right" v-if="user?.isStudent()">
                <ConfirmDialog>
                    <template #container="{ message, acceptCallback, rejectCallback }">
                        <div class="flex flex-column p-5 surface-overlay border-round" style="max-width: 600px">
                            <span class="font-bold text-2xl">{{ message.header }}</span>
                            <p class="mb-4">{{ message.message }}</p>
                            <div class="flex gap-2 justify-content-end">
                                <Button outlined rounded @click="rejectCallback">{{ t('primevue.cancel') }}</Button>
                                <Button @click="acceptCallback" rounded>{{ t('views.courses.enroll') }}</Button>
                            </div>
                        </div>
                    </template>
                </ConfirmDialog>

                <Button @click="joinCourse" icon="pi pi-sign-in" :label="t('views.courses.enroll')"></Button>
            </div>
        </div>

        <!-- Description -->
        <div class="surface-300 px-4 py-3" v-html="course?.description"></div>

        <!-- Heading for teachers and assistants -->
        <div class="flex justify-content-between align-items-center my-6">
            <Title class="m-0">{{ t('views.courses.teachersAndAssistants.title') }}</Title>
        </div>

        <!-- List with teachers and assistants -->
        <TeacherAssistantList :course="course" :users="instructors" v-if="course" />

    </BaseLayout>
</template>

<style scoped lang="scss"></style>
