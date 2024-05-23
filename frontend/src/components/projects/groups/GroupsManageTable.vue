<script setup lang="ts">
import DataTable, { type DataTableRowExpandEvent } from 'primevue/datatable';
import Column from 'primevue/column';
import AllSubmission from '@/components/submissions/AllSubmission.vue';
import InputNumber from 'primevue/inputnumber';
import { type Project } from '@/types/Project.ts';
import { useStudents } from '@/composables/services/student.service.ts';
import { ref } from 'vue';
import { type Group } from '@/types/Group.ts';
import { useSubmission } from '@/composables/services/submission.service.ts';
import { useI18n } from 'vue-i18n';
import { PrimeIcons } from 'primevue/api';

/* Props */
defineProps<{
    project: Project;
    groups: Group[];
}>();

/* Emits */
const emit = defineEmits(['update:group-score']);

/* Composable injections */
const { t } = useI18n();
const { students, getStudentsByGroup } = useStudents();
const { submissions, getSubmissionByGroup } = useSubmission();

/* State */
const expandedRows = ref<any[]>();
const editingGroup = ref<Group | null>();

/**
 * Updates the score of a group.
 *
 * @param group The group to update.
 * @param score The new score.
 */
function updateGroupScore(group: Group, score: number): void {
    emit('update:group-score', group, score);
    editingGroup.value = null;
}

/**
 * Logic when triggering the collapse of a row.
 * @param event
 */
async function expandGroup(event: DataTableRowExpandEvent): Promise<void> {
    // Extract the group from the event data.
    const group: Group = event.data;

    // Load the group's students.
    await getStudentsByGroup(group.id);
    group.students = students.value ?? [];

    // Load the group's submissions.
    await getSubmissionByGroup(group.id);
    group.submissions = submissions.value ?? [];
}
</script>

<template>
    <DataTable data-key="id" :value="groups" v-model:expanded-rows="expandedRows" @row-expand="expandGroup">
        <Column expander />

        <Column :header="t('views.projects.groupName')">
            <template #body="{ data }">
                <i :class="PrimeIcons.TAG" class="mr-2" />{{ t('views.projects.group') }}
                {{ project.getGroupNumber(data) }}
            </template>
        </Column>

        <Column :header="t('views.projects.groupPopulation')">
            <template #body="{ data }">
                <i :class="PrimeIcons.USERS" class="mr-2" /> {{ data.getSize() }} / {{ project.group_size }}
            </template>
        </Column>

        <Column :header="t('views.projects.groupScore')">
            <template #body="{ data }">
                <i :class="PrimeIcons.CHART_BAR" class="mr-2" />
                <template v-if="editingGroup === data">
                    <InputNumber :model-value="data.score" @change="updateGroupScore(data, $event.target.value)" /> /
                    {{ project.max_score }}
                </template>
                <template v-else>
                    <template v-if="data.score !== null && data.score !== undefined">
                        {{ data.score }} / {{ project.max_score }}
                    </template>
                    <template v-else>
                        {{ t('views.projects.noGroupScore') }}
                    </template>
                    <i :class="PrimeIcons.PENCIL" class="ml-3" @click="editingGroup = data" />
                </template>
            </template>
        </Column>

        <template #expansion="{ data }">
            <div class="grid">
                <div class="col">
                    <h3>{{ t('views.projects.groupMembers') }}</h3>
                    <template v-if="data.students.length > 0">
                        <div class="flex flex-column gap-3">
                            <div
                                class="flex align-items-center gap-2"
                                v-for="student in data.students"
                                :key="student.id"
                            >
                                <i class="pi pi-user" /> <span>{{ student.getFullName() }}</span>
                            </div>
                        </div>
                    </template>
                    <template v-else>
                        {{ t('views.projects.noGroupMembers') }}
                    </template>
                </div>
                <div class="col">
                    <h3>{{ t('views.projects.submissionStatus') }}</h3>
                    <AllSubmission :submissions="data.submissions" />
                </div>
            </div>
        </template>

        <template #empty> </template>
    </DataTable>
</template>

<style scoped lang="scss"></style>
