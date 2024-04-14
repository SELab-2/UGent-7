<script setup lang="ts">
import BaseLayout from '@/components/layout/BaseLayout.vue';
import StudentCourseView from './roles/StudentCourseView.vue';
import TeacherCourseView from './roles/TeacherCourseView.vue';
import AssistantCourseView from './roles/AssistantCourseView.vue';
import { onMounted } from 'vue';
import { useCourses } from '@/composables/services/courses.service.ts';
import { useAssistant } from '@/composables/services/assistant.service';
import { useTeacher } from '@/composables/services/teachers.service';
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/store/authentication.store.ts';
import { storeToRefs } from 'pinia';

/* Service injection */
const { user } = storeToRefs(useAuthStore());
const { params } = useRoute();
const { course, getCourseByID } = useCourses();
const { assistants, getAssistantByCourse } = useAssistant();
const { teachers, getTeacherByCourse } = useTeacher();

onMounted(async () => {
    await getCourseByID(params.courseId as string);

    // Get assistants and teachers
    if (course.value !== null) {
        await getAssistantByCourse(course.value.id);
        await getTeacherByCourse(course.value.id);

        // Set the course's assistants and teachers
        course.value.assistants = assistants.value ?? [];
        course.value.teachers = teachers.value ?? [];
    }
});
</script>

<template>
    <BaseLayout>
        <div v-if="course">
            <StudentCourseView v-if="user?.isStudent()" :course="course" />
            <TeacherCourseView v-else-if="user?.isTeacher()" :course="course" />
            <AssistantCourseView v-else-if="user?.isAssistant()" :course="course" />
        </div>
    </BaseLayout>
</template>

<style scoped lang="scss"></style>
