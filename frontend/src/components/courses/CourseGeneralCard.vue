<script setup lang="ts">
import Button from 'primevue/button';
import type { Course } from '@/types/Course.ts';
import { Faculty } from '@/types/Faculty.ts';
import { useAuthStore } from '@/store/authentication.store.ts';
import { storeToRefs } from 'pinia';
import { useStudents } from '@/composables/services/students.service.ts';
import { useMessagesStore } from '@/store/messages.store.ts';

/* Props */
const props = defineProps<{
    course: Course;
}>();

/* Component injections */
const { user, student } = storeToRefs(useAuthStore());
const { refresh } = useAuthStore();
const { add } = useMessagesStore();
const { studentJoinCourse, studentLeaveCourse } = useStudents();

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
    return images.find(image => image.includes(faculty.id)) ?? '';
}

/**
 * Enroll the student in the course.
 */
function joinCourse() {
    if (student.value && student.value.isStudent()) {
        studentJoinCourse(props.course.id, student.value.id).then(() => {
            add({
                severity: 'success',
                summary: 'Inschrijving voltooid',
                detail: `Je bent succesvol ingeschreven voor ${props.course.name}`
            });
            refresh();
        });
    }
}

/**
 * Leave the course.
 */
function leaveCourse() {
    if (student.value && student.value.isStudent()) {
        studentLeaveCourse(props.course.id, student.value.id).then(() => {
            add({
                severity: 'success',
                summary: 'Uitgeschreven',
                detail: `Je bent succesvol uitgeschreven voor ${props.course.name}`
            });
            refresh();
        });
    }
}
</script>

<template>
    <div class="surface-300 pl-7 p-4 relative">
        <img :src="getFacultyIcon(course.faculty)" :alt="course.faculty.name" class="absolute top-0 left-0 w-3rem" v-if="course.faculty !== null"/>
        <div class="h-full flex flex-column justify-content-between">
            <div>
                <div class="text-primary font-semibold text-lg">
                    {{ course.name }}
                </div>
                <div class="text-sm text-black-alpha-80">
                    {{ course.getCourseYear() }}
                </div>
            </div>
            <div v-if="user">
                <template v-if="user.isStudent()">
                    <Button severity="secondary" class="text-sm p-0" label="Inschrijven" icon-pos="right" icon="pi pi-arrow-right" @click="joinCourse" v-if="!student!.hasCourse(course)" link/>
                    <Button severity="secondary" class="text-sm p-0" label="Uitschrijven" icon-pos="right" icon="pi pi-arrow-right" @click="leaveCourse" v-else link/>
                </template>
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss">

</style>