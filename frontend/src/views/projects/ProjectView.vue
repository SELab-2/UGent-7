<script setup lang="ts">
import BaseLayout from '@/components/layout/base/BaseLayout.vue';
import { useCourses } from '@/composables/services/courses.service.ts';
import { computed, onMounted, ref } from 'vue';
import { storeToRefs } from 'pinia';
import { useAuthStore } from '@/store/authentication.store.ts';
import ProjectList from '@/components/projects/ProjectList.vue';
import Title from '@/components/layout/Title.vue';
import { useI18n } from 'vue-i18n';
import YearSelector from '@/components/YearSelector.vue';
import { User } from '@/types/users/User.ts';

const { t } = useI18n();
const { user } = storeToRefs(useAuthStore());
const { courses, getCoursesByStudent } = useCourses();

const selectedYear = ref<number>(User.getAcademicYear());

onMounted(async () => {
    if (user.value?.id != null) {
        await getCoursesByStudent(user.value.id);
    }
});

const filteredCourses = computed(
    () => courses.value?.filter((course) => course.academic_startyear === selectedYear.value) ?? [],
);
</script>

<template>
    <BaseLayout>
        <!-- Project heading -->
        <div class="flex justify-content-between align-items-center mb-6">
            <!-- Project list title -->
            <Title class="m-0">{{ t('views.dashboard.projects') }}</Title>
            <YearSelector :years="user.academic_years" v-model="selectedYear" v-if="user" />
        </div>

        <ProjectList v-if="filteredCourses" :courses="filteredCourses" />
    </BaseLayout>
</template>

<style scoped lang="scss"></style>
