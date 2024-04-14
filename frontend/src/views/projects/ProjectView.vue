<script setup lang="ts">
import BaseLayout from '@/components/layout/BaseLayout.vue';
import ProjectList from '@/components/projects/ProjectList.vue';
import Title from '@/components/layout/Title.vue';
import YearSelector from '@/components/YearSelector.vue';
import { useCourses } from '@/composables/services/course.service.ts';
import { computed, onMounted, ref } from 'vue';
import { storeToRefs } from 'pinia';
import { useAuthStore } from '@/store/authentication.store.ts';
import { useI18n } from 'vue-i18n';
import { getAcademicYear, getAcademicYears } from '@/types/Course.ts';

/* Composable injections */
const { t } = useI18n();
const { user } = storeToRefs(useAuthStore());
const { courses, getCoursesByStudent } = useCourses();

/* State */
const selectedYear = ref<number>(getAcademicYear());
const allYears = computed(() => getAcademicYears(...(courses.value?.map((course) => course.academic_startyear) ?? [])));

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
        <div
            class="flex gap-6 flex-column md:flex-row justify-content-between align-items-start md:align-items-center mb-5"
        >
            <!-- Project list title -->
            <Title class="m-0">{{ t('views.dashboard.projects') }}</Title>
            <YearSelector :years="allYears" v-model="selectedYear" v-if="user" />
        </div>

        <ProjectList v-if="filteredCourses" :courses="filteredCourses" />
    </BaseLayout>
</template>

<style scoped lang="scss"></style>
