<script setup lang="ts">
import moment from 'moment';
import Skeleton from 'primevue/skeleton';
import InputSwitch from 'primevue/inputswitch';
import ProjectDetailCard from '@/components/projects/ProjectDetailCard.vue';
import ProjectDeadlineCard from '@/components/projects/ProjectDeadlineCard.vue';
import Button from 'primevue/button';
import { computed, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { type Project } from '@/types/Project.ts';
import { type Group } from '@/types/Group.ts';
import { storeToRefs } from 'pinia';
import { useAuthStore } from '@/store/authentication.store.ts';
import { useStudents } from '@/composables/services/student.service';
import { type Course } from '@/types/Course.ts';
import Loading from '@/components/Loading.vue';

/* Props */
const props = withDefaults(
    defineProps<{
        projects?: Project[] | null;
        courses?: Course[] | null;
        cols?: number;
    }>(),
    {
        projects: () => [],
        cols: 4,
    },
);

/* Composables */
const { t } = useI18n();
const { user } = storeToRefs(useAuthStore());
const { student, getStudentByID } = useStudents();

/**
 * Get the groups of the corresponding users
 */
function getUserGroups(): Group[] {
    if (user.value !== null && user.value?.isStudent()) {
        // eslint-disable-next-line @typescript-eslint/prefer-optional-chain
        return student.value !== null && student.value.groups !== null ? student.value?.groups : [];
    }
    return [];
}

/* State */
const showPast = ref(false);

/* Watchers */
watch(
    user,
    () => {
        if (user.value !== null && user.value.isStudent()) {
            getStudentByID(user.value.id);
        }
    },
    {
        immediate: true,
    },
);

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
                {{ t('components.list.showPastProjects') }}
            </label>
        </div>
        <!-- Project list -->
        <template v-if="sortedProjects === null || sortedProjects.length > 0">
            <div class="grid nested-grid">
                <div class="col-12 md:col-5">
                    <h2 class="mt-0">
                        {{ t('views.projects.coming') }}
                    </h2>
                    <div class="grid">
                        <template v-if="incomingProjects !== null">
                            <template v-if="incomingProjects.length > 0">
                                <div class="col-12" v-for="project in incomingProjects" :key="project.id">
                                    <ProjectDeadlineCard type="small" :project="project" :course="project.course" />
                                </div>
                            </template>
                            <template v-else>
                                <div class="col-12">
                                    <p class="mt-0">{{ t('components.list.noIncomingProjects') }}</p>
                                </div>
                            </template>
                        </template>
                        <template v-else>
                            <Loading height="50vh"/>
                        </template>
                    </div>
                </div>
                <div class="col-12 md:col-7">
                    <h2 class="mt-0">
                        {{ t('views.projects.all') }}
                    </h2>
                    <div class="grid">
                        <template v-if="sortedProjects !== null">
                            <div class="col-12" v-for="project in sortedProjects" :key="project.id">
                                <ProjectDetailCard
                                    class="h-100"
                                    :project="project"
                                    :course="project.course"
                                    :studentGroups="getUserGroups()"
                                />
                            </div>
                        </template>
                        <template v-else>
                            <Loading height="50vh"/>
                        </template>
                    </div>
                </div>
            </div>
        </template>
        <template v-else>
            <div class="max-w-30rem text-center mx-auto">
                <span class="pi pi-exclamation-circle text-6xl text-primary" />
                <div class="mt-3">
                    <slot name="empty">
                        <p>{{ t('components.list.noProjects.student') }}</p>
                        <RouterLink :to="{ name: 'courses' }">
                            <Button :label="t('components.button.searchCourse')" icon="pi pi-search" />
                        </RouterLink>
                    </slot>
                </div>
            </div>
        </template>
    </div>
</template>

<style scoped lang="scss"></style>
