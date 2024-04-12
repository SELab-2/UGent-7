<script setup lang="ts">
import Accordion from 'primevue/accordion';
import AccordionTab from 'primevue/accordiontab';
import InputText from 'primevue/inputtext';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import Checkbox from 'primevue/checkbox';
import Paginator from 'primevue/paginator';
import TeacherAssistantList from './TeacherAssistantList.vue';
import { onMounted } from 'vue';
import { useCourses } from '@/composables/services/courses.service.ts';
import { useAuthStore } from '@/store/authentication.store.ts';
import { useFaculty } from '@/composables/services/faculties.service.ts';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';
import { useFilter } from '@/composables/filters/filter.ts';
import { usePaginator } from '@/composables/filters/paginator.ts';
import { useRoute } from 'vue-router';
import { getUserFilters } from '@/types/filter/Filter.ts';

/* Composable injections */
const { t } = useI18n();
const { query } = useRoute();
const { user } = storeToRefs(useAuthStore());
const { faculties, getFaculties } = useFaculty();
const { pagination, searchCourses } = useCourses();
const { onPaginate, resetPagination, page, first, pageSize } = usePaginator();
const { filter, onFilter } = useFilter(getUserFilters(query));

/* Teacher and assistant roles */
const roles = ['types.roles.teacher', 'types.roles.assistant'];

/**
 * Fetch the users based on the filter.
 */
async function fetchCourses(): Promise<void> {
    await searchCourses(filter.value, page.value, pageSize.value);
}

/* Fetch the faculties */
onMounted(async () => {
    // Fetch the faculties
    await getFaculties();

    /* Search users on page change */
    onPaginate(fetchCourses);

    /* Search users on filter change */
    onFilter(fetchCourses);

    /* Reset pagination on filter change */
    onFilter(
        async () => {
            await resetPagination(pagination);
        },
        0,
        false,
    );
});
</script>

<template>
    <div class="grid">
        <div class="col-12 xl:col-3">
            <Accordion :active-index="[0]" multiple>
                <AccordionTab :header="t('views.courses.teachers_and_assistants.search.search')">
                    <IconField iconPosition="left">
                        <InputText
                            :placeholder="t('views.courses.teachers_and_assistants.search.placeholder')"
                            v-model="filter.search"
                            class="w-full"
                        />
                        <InputIcon class="pi pi-search"></InputIcon>
                    </IconField>
                </AccordionTab>
                <AccordionTab :header="t('views.courses.teachers_and_assistants.search.faculty')" v-if="faculties">
                    <div v-for="faculty in faculties" :key="faculty.id" class="flex align-items-centFupder mb-2">
                        <Checkbox
                            v-model="filter.faculties"
                            :inputId="faculty.id"
                            name="faculties"
                            :value="faculty.id"
                        />
                        <label :for="faculty.id" class="ml-2 text-sm">{{ faculty.name }}</label>
                    </div>
                </AccordionTab>
                <AccordionTab :header="t('views.courses.teachers_and_assistants.search.role')" v-if="user && pagination !== null">
                    <div
                        v-for="role in roles"
                        :key="role"
                        class="flex align-items-center mb-2"
                    >
                        <Checkbox
                            v-model="filter.roles"
                            :inputId="role"
                            name="roles"
                            :value="t(role)"
                        />
                        <label :for="role" class="ml-2 text-sm"> {{ t(role) }} </label>
                    </div>
                </AccordionTab>
            </Accordion>
        </div>
        <div class="col-12 xl:col-9">
            <Paginator :rows="pageSize" :total-records="pagination?.count" :first="first" v-model:first="first" />
        </div>
    </div>
</template>

<style scoped lang="scss"></style>
