<script setup lang="ts">
import StudentCourseJoinButton from '@/components/courses/students/StudentCourseJoinButton.vue';
import type { Course } from '@/types/Course.ts';
import { useAuthStore } from '@/store/authentication.store.ts';
import { storeToRefs } from 'pinia';
import { type Student } from '@/types/users/Student.ts';
import { useGlob } from '@/composables/glob.ts';

/* Props */
defineProps<{
    course: Course;
    courses: Course[];
}>();

/* Emits */
const emit = defineEmits(['update:courses']);

/* Composable injections */
const { user } = storeToRefs(useAuthStore());

/* State */
const { getImport } = useGlob(import.meta.glob('@/assets/img/faculties/*.png', { eager: true }));
</script>

<template>
    <div class="surface-300 pl-7 p-4 relative">
        <img
            :src="getImport(course.faculty.id + '.png')"
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
                <StudentCourseJoinButton
                    :student="user as Student"
                    :courses="courses"
                    :course="course"
                    @update:courses="emit('update:courses')"
                />
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss"></style>
