<script setup lang="ts">
import Accordion from 'primevue/accordion';
import AccordionTab from 'primevue/accordiontab';
import InputText from 'primevue/inputtext';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import Checkbox from 'primevue/checkbox';
import Paginator from 'primevue/paginator';
import TeacherAssistantList from './TeacherAssistantList.vue';
import { type Course} from '@/types/Course.ts';
import { onMounted, ref } from 'vue';
import { useTeacher } from '@/composables/services/teachers.service';
import { useAssistant } from '@/composables/services/assistant.service';
import { useAuthStore } from '@/store/authentication.store.ts';
import { useFaculty } from '@/composables/services/faculties.service.ts';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';
import { useFilter } from '@/composables/filters/filter.ts';
import { usePaginator } from '@/composables/filters/paginator.ts';
import { useRoute } from 'vue-router';
import { getUserFilters } from '@/types/filter/Filter.ts';
import { User } from '@/types/users/User';

/* Composable injections */
const { t } = useI18n();
const { query } = useRoute();
const { user } = storeToRefs(useAuthStore());
const { faculties, getFaculties } = useFaculty();
const { teacherPagination, searchTeachers } = useTeacher();
const { assistantPagination, searchAssistants } = useAssistant();
const { onPaginate, resetPagination, page, first, pageSize } = usePaginator();
const { filter, onFilter } = useFilter(getUserFilters(query));

/* Props */
const props = defineProps<{ course: Course }>();

/* Teacher and assistant roles */
const roles = [
    { label: 'teacher', value: 'types.roles.teacher' },
    { label: 'assistant', value: 'types.roles.assistant' },
]

/* Ref that contains all the filtered users */
const filteredUsers = ref<User[]>([]);

/**
 * Fetch the users based on the filter.
 */
async function fetchUsers(): Promise<void> {
    await searchTeachers(filter.value, page.value, pageSize.value);
    await searchAssistants(filter.value, page.value, pageSize.value);

    // Set the filtered users
    filteredUsers.value = [...(teacherPagination.value?.results ?? []), ...(assistantPagination.value?.results ?? [])];
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
            await resetPagination([teacherPagination, assistantPagination]);
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
                <AccordionTab :header="t('views.courses.teachers_and_assistants.search.role')" v-if="user">
                    <div
                        v-for="role in roles"
                        :key="role.label"
                        class="flex align-items-center mb-2"
                    >
                        <Checkbox
                            v-model="filter.roles"
                            :inputId="role.label"
                            name="roles"
                            :value="role.label"
                        />
                        <label :for="role.label" class="ml-2 text-sm"> {{ t(role.value) }} </label>
                    </div>
                </AccordionTab>
            </Accordion>
        </div>
        <div class="col-12 xl:col-9">
            <TeacherAssistantList :users="filteredUsers" :cols="3" :course="props.course" />
            <Paginator :rows="pageSize" :total-records="filteredUsers?.length" :first="first" />
        </div>
    </div>
</template>

<style scoped lang="scss"></style>
