<script setup lang="ts">
import moment from 'moment';
import 'moment/dist/locale/nl';
import BaseLayout from '@/components/layout/BaseLayout.vue';
import ProjectLink from '@/components/projects/ProjectLink.vue';
import Calendar from 'primevue/calendar';
import Title from '@/components/Title.vue';
import { useProject } from '@/composables/services/project.service';
import { computed, onMounted } from 'vue';
import {useI18n} from 'vue-i18n';
import { ref } from 'vue';

const { t, locale } = useI18n();
const { projects, getProjectWithCourseContext } = useProject();


/* Keeps track of the selected date */
const selectedDate = ref(new Date());

const formattedDate = computed(() => {
    // Format the selected date using moment.js
    return moment(selectedDate.value).locale(locale.value).format('DD MMMM YYYY');
});

/* Load the projects of the current student */
// TODO: Set correct user ID
const loadProjects = async () => {
    await getProjectWithCourseContext("000210394313");
};

/* Filter the projects on the date selected on the calendar */
const projectsWithDeadline = computed(() => {
    // Filter the projects with the selected date
    return projects.value?.filter(project => {
        return moment(project.deadline).isSame(moment(selectedDate.value), 'day');
    });
});

/* Load the projects when the component is mounted */
onMounted(() => {
    loadProjects();
});

</script>

<template>
    <BaseLayout>
        <div class="grid">
            <div class="col-12 md:col-6">
                <!-- Calendar heading -->
                <Title class="mb-6">{{ t('views.calendar.title') }}</Title>

                <div>
                    <!-- Calendar itself -->
                    <Calendar class="w-full" v-model="selectedDate" inline/>
                </div>
            </div>
            <div class="col-12 md:col-6">
                <!-- Selected date on the calendar -->
                <Title class="mb-6">{{ formattedDate }}</Title>

                <!-- Listing projects with given deadline -->
                <div>
                    <div class="col-12" v-for="project in projectsWithDeadline" :key="project.id">
                        <!-- Each ProjectLink card -->
                        <ProjectLink class="h-100 mb-2" :project="project"/>
                    </div>
                </div>
            </div>
        </div>
    </BaseLayout>
</template>

<style scoped lang="scss">

</style>