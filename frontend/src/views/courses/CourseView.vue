<script setup lang="ts">
import BaseLayout from '@/views/layout/base/BaseLayout.vue';
import StudentCourseView from './roles/StudentCourseView.vue';
import TeacherCourseView from './roles/TeacherCourseView.vue';
import AssistantCourseView from './roles/AssistantCourseView.vue';
import Loading from '@/components/Loading.vue';
import { onMounted, ref } from 'vue';
import { useAssistant } from '@/composables/services/assistant.service';
import { useTeacher } from '@/composables/services/teacher.service';
import { useCourses } from '@/composables/services/course.service.ts';
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/store/authentication.store.ts';
import { storeToRefs } from 'pinia';

/* Service injection */
const { user } = storeToRefs(useAuthStore());
const { params } = useRoute();
const { course, getCourseByID } = useCourses();
const { assistants, getAssistantsByCourse } = useAssistant();
const { teachers, getTeachersByCourse } = useTeacher();

/* Loading state */
const loading = ref<boolean>(true);

/**
 * Fetch the course by its ID and set the course's assistants and teachers
 */
onMounted(async () => {
    await getCourseByID(params.courseId as string);

    // Get assistants and teachers
    if (course.value !== null) {
        await getAssistantsByCourse(course.value.id);
        await getTeachersByCourse(course.value.id);

        // Set the course's assistants
        if (assistants.value !== null) {
            course.value.assistants = assistants.value;
        }

        // Set the course's teachers
        if (teachers.value !== null) {
            course.value.teachers = teachers.value;
        }

        loading.value = false;
    }
});
</script>

<template>
    <BaseLayout>
        <template v-if="loading === false && course !== null">
            <div class="fadein">
                <StudentCourseView v-if="user?.isStudent()" :course="course" />
                <TeacherCourseView v-else-if="user?.isTeacher()" :course="course" />
                <AssistantCourseView v-else-if="user?.isAssistant()" :course="course" />
            </div>
        </template>
        <template v-else>
            <Loading height="100vh" />
        </template>
    </BaseLayout>
</template>

<style scoped lang="scss"></style>
