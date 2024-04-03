<script setup lang="ts">
import Accordion from 'primevue/accordion';
import AccordionTab from 'primevue/accordiontab';
import InputText from 'primevue/inputtext';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import Checkbox from 'primevue/checkbox';
import Title from '@/components/layout/Title.vue';
import BaseLayout from '@/components/layout/BaseLayout.vue';
import CourseList from '@/components/courses/CourseList.vue';
import { onMounted, ref, watch } from 'vue';
import { useCourses } from '@/composables/services/courses.service.ts';
import { useAuthStore } from '@/store/authentication.store.ts';
import { useFaculty } from '@/composables/services/faculties.service.ts';
import { Filters } from '@/types/Pagination.ts';
import { storeToRefs } from 'pinia';
import { watchDebounced } from '@vueuse/core';

/* Composable injections */
const { user } = storeToRefs(useAuthStore());
const { faculties, getFaculties } = useFaculty();
const { pagination, searchCourses } = useCourses();

/* State */
const filters = ref<Filters>({
    search: '',
    faculties: [],
    years: [user!.value!.getAcademicYear()],
});

watch(
    filters,
    () => pagination.value = null,
    { deep: true },
)

watchDebounced(
    filters,
    async () => {
        await searchCourses(filters.value);
    },
    { deep: true, immediate: true, debounce: 500 },
);

onMounted(async () => {
    await getFaculties();
});
</script>

<template>
    <BaseLayout>
        <div class="grid">
            <div class="col-12 xl:col-3">
                <Accordion :active-index="[0]" multiple>
                    <AccordionTab header="Zoeken">
                        <IconField iconPosition="left">
                            <InputText
                                placeholder="Zoek een vak op naam"
                                v-model="filters.search"
                                class="w-full" />
                            <InputIcon class="pi pi-search"></InputIcon>
                        </IconField>
                    </AccordionTab>
                    <AccordionTab header="Faculteit" v-if="faculties">
                        <div v-for="faculty in faculties" :key="faculty.id" class="flex align-items-center mb-2">
                            <Checkbox v-model="filters.faculties" :inputId="faculty.id" name="faculties" :value="faculty.id" />
                            <label :for="faculty.id" class="ml-2 text-sm">{{ faculty.name }}</label>
                        </div>
                    </AccordionTab>
                    <AccordionTab header="Academiejaar" v-if="user">
                        <div v-for="year in user.academic_years" :key="year" class="flex align-items-center mb-2">
                            <Checkbox v-model="filters.years" :inputId="year.toString()" name="faculties" :value="year" />
                            <label :for="year.toString()" class="ml-2 text-sm">{{ year }} - {{ year + 1}}</label>
                        </div>
                    </AccordionTab>
                </Accordion>
            </div>
            <div class="col-12 xl:col-9">
                <Title class="mb-5">
                    Zoek een vak
                </Title>
                <CourseList :courses="pagination?.results ?? null" :cols="3" :detail="false"/>
            </div>
        </div>
    </BaseLayout>
</template>

<style scoped lang="scss"></style>
