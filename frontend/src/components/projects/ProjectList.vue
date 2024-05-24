<script setup lang="ts">
import moment from 'moment';
import Checkbox from 'primevue/checkbox';
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

/* Props */
const props = defineProps<{
    projects: Project[];
}>();

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
        return student.value !== null ? student.value?.groups : [];
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
const sortedProjects = computed<Project[]>(() => {
    const projects = props.projects.filter((project) => (!showPast.value ? moment(project.deadline).isAfter() : true));

    return [...projects].sort((a, b) => new Date(a.deadline).getTime() - new Date(b.deadline).getTime());
});

/* Filters the projects by incoming deadline (less than one week) */
const incomingProjects = computed<Project[]>(() => {
    return (
        sortedProjects.value?.filter((project) => moment(project.deadline).isBefore(moment().add(1, 'week'))) ?? null
    );
});
</script>

<template>
    <div>
        <!-- Show past projects switch -->
        <div class="p-4 surface-100 inline-block mb-5">
            <div class="flex gap-3 align-items-center">
                <Checkbox input-id="show-past" v-model="showPast" binary />
                <label for="show-past">
                    {{ t('components.list.showPastProjects') }}
                </label>
            </div>
        </div>
        <!-- Project list -->
        <template v-if="sortedProjects.length > 0">
            <div class="grid nested-grid">
                <div class="col-12 md:col-5">
                    <h2 class="mt-0">
                        {{ t('views.projects.coming') }}
                    </h2>
                    <div class="grid">
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
                    </div>
                </div>
                <div class="col-12 md:col-7">
                    <h2 class="mt-0">
                        {{ t('views.projects.all') }}
                    </h2>
                    <div class="grid">
                        <div class="col-12" v-for="project in sortedProjects" :key="project.id">
                            <ProjectDetailCard
                                class="h-100"
                                :project="project"
                                :course="project.course"
                                :studentGroups="getUserGroups()"
                            />
                        </div>
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
                        <RouterLink id="courses" :to="{ name: 'courses' }">
                            <Button :label="t('components.button.searchCourse')" icon="pi pi-search" />
                        </RouterLink>
                    </slot>
                </div>
            </div>
        </template>
    </div>
</template>

<style scoped lang="scss"></style>
