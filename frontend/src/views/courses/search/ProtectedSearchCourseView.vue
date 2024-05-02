<script setup lang="ts">
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import ProtectedSearchStepper from '@/components/courses/search/ProtectedSearchStepper.vue';
import Title from '@/components/layout/Title.vue';
import BaseLayout from '@/components/layout/base/BaseLayout.vue';
import { useI18n } from 'vue-i18n';
import { ref, onMounted } from 'vue';
import CourseGeneralList from '@/components/courses/CourseGeneralList.vue';
import { useCourses } from '@/composables/services/course.service.ts';
import { usePaginator } from '@/composables/filters/paginator.ts';
import { useFilter } from '@/composables/filters/filter.ts';
import { getPrivateCourseFilters } from '@/types/filter/Filter.ts';
import { useRoute } from 'vue-router';

/* Composable injections */
const { t } = useI18n();
const { query } = useRoute();

/* State */
const searchQuery = ref('');
const { pagination, searchCourses } = useCourses();
const { onPaginate, resetPagination, page, pageSize } = usePaginator();
const { filter, onFilter } = useFilter(getPrivateCourseFilters(query));

/**
 * Fetch the courses based on the filter.
 */
async function fetchCourses(): Promise<void> {
    filter.value.invitationLink = searchQuery.value;
    await searchCourses(filter.value, page.value, pageSize.value);
}

onMounted(async () => {
    /* Search courses on page change */
    onPaginate(fetchCourses);

    /* Search courses on filter change */
    onFilter(fetchCourses);

    /* Reset pagination on filter change */
    onFilter(
        async () => {
            await resetPagination([pagination]);
        },
        0,
        false,
    );
});
</script>

<template>
    <BaseLayout>
        <div class="grid">
            <div class="col-12 xl:col-3">
                <ProtectedSearchStepper />
            </div>
            <div class="col-12 xl:col-9 mt-4 xl:mt-0">
                <div class="flex justify-content-between align-items-center">
                    <Title>
                        {{ t('views.courses.search.title') }}
                    </Title>
                    <slot name="publicButton" />
                </div>

                <span class="relative flex mt-4">
                    <InputText
                        v-model="searchQuery"
                        :placeholder="t('views.courses.searchByLink.placeholder')"
                        style="width: 80%"
                        type="search"
                    />
                    <Button @click="fetchCourses" icon="pi pi-search" class="p-button-primary" />
                </span>

                <!-- Founded courses -->
                <CourseGeneralList class="mt-3" :courses="pagination?.results ?? null" :cols="3">
                    <template #empty>
                        <p>{{ t('components.list.noCourses.search') }}</p>
                    </template>
                </CourseGeneralList>
            </div>
        </div>
    </BaseLayout>
</template>

<style scoped lang="scss"></style>
