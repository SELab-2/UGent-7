<script setup lang="ts">
import Card from 'primevue/card';
import { type User } from '@/types/users/User.ts';
import { type Course } from '@/types/Course';
import { useI18n } from 'vue-i18n';
import TeacherCourseAddButton from '@/components/teachers_assistants/add_button/TeacherCourseAddButton.vue';
import AssistantCourseAddButton from '@/components/teachers_assistants/add_button/AssistantCourseAddButton.vue';
import { useAuthStore } from '@/store/authentication.store.ts';
import { storeToRefs } from 'pinia';

/* Component props */
const props = defineProps<{ user: User, course: Course }>();

/* Composable injections */
const { t } = useI18n();
const { user } = storeToRefs(useAuthStore());

</script>

<template>
    <Card class="border-round course-card">
        <template #title>
            <h2 class="text-primary m-0 text-xl">{{ props.user.getFullName() }}</h2>
        </template>
        <template #subtitle>
            <span class="text-sm">{{ t(props.user.getRole()) }}</span>
        </template>
        <template #content>
            {{ props.user.email }}
        </template>
        <!-- Display add/remove button on the assistant/teacher card, only when the user is a-->
        <template #footer v-if="user?.isTeacher()">
            <TeacherCourseAddButton :user="props.user" :course="course" v-if="props.user.isTeacher()" />
            <AssistantCourseAddButton :user="props.user" :course="course" v-else-if="props.user.isAssistant()" />
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
