<script setup lang="ts">
import Accordion from 'primevue/accordion';
import AccordionTab from 'primevue/accordiontab';
import InputText from 'primevue/inputtext';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import Checkbox from 'primevue/checkbox';
import Paginator from 'primevue/paginator';
import TeacherAssistantList from './TeacherAssistantList.vue';
import { type Course } from '@/types/Course.ts';
import { onMounted } from 'vue';
import { useUser } from '@/composables/services/users.service';
import { useFaculty } from '@/composables/services/faculty.service.ts';
import { useI18n } from 'vue-i18n';
import { useFilter } from '@/composables/filters/filter.ts';
import { usePaginator } from '@/composables/filters/paginator.ts';
import { useRoute } from 'vue-router';
import { getUserFilters } from '@/types/filter/Filter.ts';

/* Composable injections */
const { t } = useI18n();
const { query } = useRoute();
const { faculties, getFaculties } = useFaculty();
const { searchUsers, pagination } = useUser();
const { onPaginate, resetPagination, page, first, pageSize } = usePaginator();
const { filter, onFilter } = useFilter(getUserFilters(query));

/* Props */
const props = defineProps<{ course: Course }>();

/**
 * Fetch the users based on the filter.
 */
async function fetchUsers(): Promise<void> {
    await searchUsers(filter.value, page.value, pageSize.value);
}

/* Fetch the faculties */
onMounted(async () => {
    // Fetch the faculties
    await getFaculties();

    /* Search users on page change */
    onPaginate(fetchUsers);

    /* Search users on filter change */
    onFilter(fetchUsers);

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
    <div class="grid">
        <div class="col-12 xl:col-3">
            <Accordion :active-index="[0]" multiple>
                <AccordionTab :header="t('views.courses.teachers_and_assistants.search.search')">
                    <IconField iconPosition="left">
                        <InputText
                            :placeholder="t('views.courses.teachers_and_assistants.search.placeholder')"
                            v-model="filter.name"
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
            </Accordion>
        </div>
        <div class="col-12 xl:col-9">
            <TeacherAssistantList :users="pagination?.results ?? null" :cols="3" :course="props.course" :detail="false" />
            <Paginator :rows="pageSize" :total-records="pagination?.count" v-model:first="first" />
        </div>
    </div>
</template>

<style scoped lang="scss"></style>
