<script setup lang="ts">
import Accordion from 'primevue/accordion';
import AccordionTab from 'primevue/accordiontab';
import InputText from 'primevue/inputtext';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import Checkbox from 'primevue/checkbox';
import Paginator from 'primevue/paginator';
import Title from '@/components/layout/Title.vue';
import BaseLayout from '@/components/layout/BaseLayout.vue';
import CourseList from '@/components/courses/CourseList.vue';
import { onMounted, watch } from 'vue';
import { useCourses } from '@/composables/services/courses.service.ts';
import { useAuthStore } from '@/store/authentication.store.ts';
import { useFaculty } from '@/composables/services/faculties.service.ts';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';
import { useFilter } from '@/composables/filters/filter.ts';
import { usePaginator } from '@/composables/filters/paginator.ts';
import { useRoute, useRouter } from 'vue-router';
import { getCourseFilters } from '@/types/filter/Filter.ts';

/* Composable injections */
const { t } = useI18n();
const { query } = useRoute();
const { user } = storeToRefs(useAuthStore());
const { faculties, getFaculties } = useFaculty();
const { pagination, searchCourses } = useCourses();
const { onPaginate, paginate, page, first, pageSize } = usePaginator();
const { filter, onFilter } = useFilter(getCourseFilters(query));

/* Fetch the faculties */
onMounted(async () => {
    // Fetch the faculties
    await getFaculties();

    /* Reset current page on filter changes */
    watch(
        filter,
        () => {
            paginate(0);
            pagination.value = null;
        },
        { deep: true },
    );

    /**
     * Fetch the courses based on the filter.
     */
    async function fetchCourses(): Promise<void> {
        await searchCourses(filter.value, page.value, pageSize.value);
    }

    /* Search courses on page change */
    onPaginate(fetchCourses);

    /* Search courses on filter change */
    onFilter(fetchCourses);
});
</script>

<template>
    <BaseLayout>
        <div class="grid">
            <div class="col-12 xl:col-3">
                <Accordion :active-index="[0]" multiple>
                    <AccordionTab :header="t('views.courses.search.search')">
                        <IconField iconPosition="left">
                            <InputText
                                :placeholder="t('views.courses.search.placeholder')"
                                v-model="filter.search"
                                class="w-full"
                            />
                            <InputIcon class="pi pi-search"></InputIcon>
                        </IconField>
                    </AccordionTab>
                    <AccordionTab :header="t('views.courses.search.faculty')" v-if="faculties">
                        <div v-for="faculty in faculties" :key="faculty.id" class="flex align-items-center mb-2">
                            <Checkbox
                                v-model="filter.faculties"
                                :inputId="faculty.id"
                                name="faculties"
                                :value="faculty.id"
                            />
                            <label :for="faculty.id" class="ml-2 text-sm">{{ faculty.name }}</label>
                        </div>
                    </AccordionTab>
                    <AccordionTab :header="t('views.courses.search.year')" v-if="user">
                        <div v-for="year in user.academic_years" :key="year" class="flex align-items-center mb-2">
                            <Checkbox
                                v-model="filter.years"
                                :inputId="year.toString()"
                                name="faculties"
                                :value="year"
                            />
                            <label :for="year.toString()" class="ml-2 text-sm">{{ year }} - {{ year + 1 }}</label>
                        </div>
                    </AccordionTab>
                </Accordion>
            </div>
            <div class="col-12 xl:col-9">
                <Title>
                    {{ t('views.courses.search.title') }}
                </Title>
                <p class="mt-3" v-if="pagination">
                    {{ t('views.courses.search.results', [pagination.count]) }}
                </p>
                <CourseList class="mt-3" :courses="pagination?.results ?? null" :cols="3" :detail="false" />
                <Paginator
                    :rows="pageSize"
                    :total-records="pagination?.count"
                    :first="first"
                    @update:first="paginate($event)"
                />
            </div>
        </div>
    </BaseLayout>
</template>

<style scoped lang="scss"></style>
