<script setup lang="ts">
import moment from 'moment';
import Skeleton from 'primevue/skeleton';
import InputSwitch from 'primevue/inputswitch';
import ProjectCard from '@/components/projects/ProjectCard.vue';
import { computed, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { type Project } from '@/types/Project.ts';

/* Props */
const props = withDefaults(
    defineProps<{
        projects: Project[] | null;
        cols?: number;
    }>(),
    {
        courses: () => [],
        cols: 4,
    },
);

/* Composables */
const { t } = useI18n();

/* State */
const showPast = ref(false);

/* Sorts the projects by deadline */
const sortedProjects = computed<Project[] | null>(() => {
    const projects =
        props.projects?.filter((project) => (!showPast.value ? moment(project.deadline).isAfter() : true)) ?? null;

    if (projects === null) {
        return projects;
    }

    return [...projects].sort((a, b) => new Date(a.deadline).getTime() - new Date(b.deadline).getTime());
});

/* Filters the projects by incoming deadline (less than one week) */
const incomingProjects = computed<Project[] | null>(() => {
    return (
        sortedProjects.value?.filter((project) => moment(project.deadline).isBefore(moment().add(1, 'week'))) ?? null
    );
});
</script>

<template>
    <div>
        <!-- Show past projects switch -->
        <div class="flex gap-3 align-items-center mb-5">
            <InputSwitch input-id="show-past" v-model="showPast" />
            <label for="show-past">
                {{ t('views.dashboard.showPastProjects') }}
            </label>
        </div>
        <!-- Project list -->
        <div class="grid nested-grid">
            <div class="col-12 md:col-5">
                <h2 class="mt-0">
                    {{ t('views.projects.coming') }}
                </h2>
                <div class="grid">
                    <template v-if="incomingProjects !== null">
                        <template v-if="incomingProjects.length > 0">
                            <div class="col-12" v-for="project in incomingProjects" :key="project.id">
                                <ProjectCard
                                    type="small"
                                    :project="project"
                                    :course="project.course"
                                    v-if="project.course !== null"
                                />
                            </div>
                        </template>
                        <template v-else>
                            <div class="col-12">
                                <p class="mt-0">{{ t('views.dashboard.noProjects') }}</p>
                            </div>
                        </template>
                    </template>
                    <template v-else>
                        <div
                            class="col-12 md:col-6 lg:col-4"
                            :class="'xl:col-' + 12 / cols"
                            v-for="index in cols"
                            :key="index"
                        >
                            <Skeleton height="25rem" />
                        </div>
                    </template>
                </div>
            </div>
            <div class="col-12 md:col-7">
                <h2 class="mt-0">
                    {{ t('views.projects.all') }}
                </h2>
                <div class="grid">
                    <template v-if="sortedProjects !== null">
                        <template v-if="sortedProjects.length > 0">
                            <div class="col-12" v-for="project in sortedProjects" :key="project.id">
                                <ProjectCard
                                    class="h-100"
                                    :project="project"
                                    :course="project.course"
                                    v-if="project.course !== null"
                                />
                            </div>
                        </template>
                        <template v-else>
                            <div class="col-12">
                                <p class="mt-0">{{ t('views.dashboard.noProjects') }}</p>
                            </div>
                        </template>
                    </template>
                    <template v-else>
                        <div
                            class="col-12 md:col-6 lg:col-4"
                            :class="'xl:col-' + 12 / cols"
                            v-for="index in cols"
                            :key="index"
                        >
                            <Skeleton height="25rem" />
                        </div>
                    </template>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss"></style>
