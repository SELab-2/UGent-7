<script setup lang="ts">
import StudentProjectView from '@/views/projects/roles/StudentProjectView.vue';
import TeacherProjectView from '@/views/projects/roles/TeacherProjectView.vue';
import BaseLayout from '@/views/layout/base/BaseLayout.vue';
import Button from 'primevue/button';
import { type Student } from '@/types/users/Student';
import { type Teacher } from '@/types/users/Teacher';
import { type Assistant } from '@/types/users/Assistant';
import { useRoute } from 'vue-router';
import { PrimeIcons } from 'primevue/api';
import { useI18n } from 'vue-i18n';
import { storeToRefs } from 'pinia';
import { useAuthStore } from '@/store/authentication.store.ts';

/* Service injection */
const { user } = storeToRefs(useAuthStore());
const { params } = useRoute();
const { t } = useI18n();
</script>

<template>
    <BaseLayout>
        <RouterLink :to="{ name: 'course', params: { courseId: params.courseId } }">
            <Button
                class="mb-4 p-0 text-sm text-black-alpha-70"
                :icon="PrimeIcons.ARROW_LEFT"
                :label="t('views.projects.backToCourse')"
                link
            />
        </RouterLink>
        <template v-if="user !== null">
            <StudentProjectView v-if="user.isStudent()" :student="user as Student"> </StudentProjectView>
            <TeacherProjectView v-else-if="user.isTeacher()" :teacher="user as Teacher"> </TeacherProjectView>
            <TeacherProjectView v-else-if="user.isAssistant()" :teacher="user as Assistant"> </TeacherProjectView>
        </template>
    </BaseLayout>
</template>

<style lang="scss" scoped></style>
