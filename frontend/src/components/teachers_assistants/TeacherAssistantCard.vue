<script setup lang="ts">
import Card from 'primevue/card';
import CourseRoleAddButton from '@/components/teachers_assistants/buttons/CourseRoleAddButton.vue';
import LeaveCourseButton from '@/components/teachers_assistants/buttons/LeaveCourseButton.vue';
import { type User } from '@/types/users/User.ts';
import { type Course } from '@/types/Course';
import { useI18n } from 'vue-i18n';
import { storeToRefs } from 'pinia';
import { useAuthStore } from '@/store/authentication.store.ts';
import { PrimeIcons } from 'primevue/api';

/* Component props */
const props = defineProps<{ userValue: User; course: Course; detail?: boolean }>();

/* Composable injections */
const { t } = useI18n();
const { user } = storeToRefs(useAuthStore());
</script>

<template>
    <Card class="course-card">
        <template #title>
            <div class="flex justify-content-between">
                <h2 class="text-primary mt-2 mb-0 text-xl">
                    <span :class="PrimeIcons.USER" class="mr-2" /> {{ props.userValue.getFullName() }}
                </h2>

                <!-- Display the delete button on a detail card, only if the user is not the last teacher of the course -->
                <LeaveCourseButton
                    :user="props.userValue"
                    :course="course"
                    v-if="
                        props.detail &&
                        user?.isTeacher() &&
                        // Explicit check on role, because the roles field in not initialized in the user object
                        !(userValue.getRole() === 'types.roles.teacher' && course.teachers?.length == 1)
                    "
                />
            </div>
        </template>
        <template #subtitle v-if="props.detail">
            <span class="text-sm m-0">{{ t(props.userValue.getRole()) }}</span>
        </template>
        <template #content>
            {{ props.userValue.email }}
        </template>
        <!-- Display the role switch button, only if the card is not in detail mode, and the user is not the last teacher of the course -->
        <template
            #footer
            v-if="!props.detail && !(course.teachers?.length == 1 && course.teachers[0].id == props.userValue.id)"
        >
            <CourseRoleAddButton :user="props.userValue" :course="course" />
        </template>
    </Card>
</template>

<style lang="scss">
.course-card {
    display: flex;
    flex-direction: column;
    height: 100%;
}
</style>
