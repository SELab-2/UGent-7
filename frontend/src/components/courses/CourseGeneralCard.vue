<script setup lang="ts">
import StudentCourseJoinButton from '@/components/courses/students/StudentCourseJoinButton.vue';
import type { Course } from '@/types/Course.ts';
import { type Faculty } from '@/types/Faculty.ts';
import { useAuthStore } from '@/store/authentication.store.ts';
import { storeToRefs } from 'pinia';

/* Props */
defineProps<{
    course: Course;
}>();

/* Composable injections */
const { user, student } = storeToRefs(useAuthStore());

/* State */
const images = Object.keys(
    import.meta.glob('@/assets/img/faculties/*', {
        eager: true,
    }),
);

/**
 * Get the faculty icon based on the faculty id.
 * @param faculty
 */
function getFacultyIcon(faculty: Faculty): string {
    return images.find((image) => {
        image = image.replace('/src/assets/img/faculties/', '');
        return image === faculty.id + '.png';
    }) ?? '';
}
</script>

<template>
    <div class="surface-300 pl-7 p-4 relative">
        <img
            :src="getFacultyIcon(course.faculty)"
            :alt="course.faculty.name"
            class="absolute top-0 left-0 w-3rem"
            v-if="course.faculty !== null"
        />
        <div class="h-full flex flex-column justify-content-between">
            <div>
                <div class="text-primary font-semibold text-lg">
                    {{ course.name }}
                </div>
                <div class="text-sm text-black-alpha-80">
                    {{ course.getCourseYear() }}
                </div>
            </div>
            <div v-if="user && user.isStudent()">
                <StudentCourseJoinButton :student="student" :course="course" />
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss"></style>
