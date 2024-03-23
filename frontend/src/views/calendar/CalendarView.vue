<script setup lang="ts">
import moment from 'moment';
import 'moment/dist/locale/nl';
import BaseLayout from '@/components/layout/BaseLayout.vue';
import Calendar from 'primevue/calendar';
import Title from '@/components/Title.vue';
import { useProject } from '@/composables/services/project.service';
import { computed, onMounted } from 'vue';
import {useI18n} from 'vue-i18n';
import { ref } from 'vue';

const { t, locale } = useI18n();

/* Keeps track of the selected date */
const selectedDate = ref(new Date());

const formattedDate = computed(() => {
    // Format the selected date using moment.js
    return moment(selectedDate.value).locale(locale.value).format('DD MMMM YYYY');
});

/* Load the projects of the current student */
const { projects, getProjectsByStudent } = useProject();

// TODO: Set correct user ID
const loadProjects = async () => {
    await getProjectsByStudent("000210394313");
};

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

                <!-- List of projects -->
                <div v-for="project in projects" :key="project.id">
                    <p>{{ project.name }}</p>
                </div>
            </div>
        </div>
    </BaseLayout>
</template>

<style scoped lang="scss">

</style>