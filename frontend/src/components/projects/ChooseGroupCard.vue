<script setup lang="ts">
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import { ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useStudents } from '@/composables/services/student.service.ts';
import { type Group } from '@/types/Group.ts';
import { PrimeIcons } from 'primevue/api';
import { type Student } from '@/types/users/Student.ts';
import { type Project } from '@/types/Project.ts';

/* Props */
const props = defineProps<{
    project: Project;
    student: Student;
}>();

/* Composable injections */
const { t } = useI18n();
const { studentJoinGroup } = useStudents();

/* Emits */
const emit = defineEmits(['group-joined']);

/* State */
const dialogVisible = ref<boolean>(false);
const selectedGroup = ref<Group | null>(null);

watch(selectedGroup, () => {
    dialogVisible.value = true;
});

/**
 * Joins the selected group.
 *
 */
async function joinSelectedGroup(): Promise<void> {
    if (selectedGroup.value !== null) {
        await studentJoinGroup(selectedGroup.value.id, props.student.id);
        emit('group-joined', selectedGroup.value);
        selectedGroup.value = null;
        dialogVisible.value = false;
    }
}
</script>

<template>
    <div class="p-4 shadow-1">
        <h2 class="mt-0">
            {{ t('views.projects.chooseGroup') }}
        </h2>
        <template v-if="project.groups.length > 0 && !project.isLocked()">
            <DataTable :value="project.groups" v-model:selection="selectedGroup" selection-mode="single">
                <Column :header="t('views.projects.groupName')">
                    <template #body="{ data }">
                        {{ t('views.projects.group') }} {{ project.getGroupNumber(data) }}
                    </template>
                </Column>
                <Column :header="t('views.projects.groupPopulation')">
                    <template #body="{ data }">
                        <i class="pi pi-users mr-2" /> {{ data.students.length }} / {{ project.group_size }}
                    </template>
                </Column>
                <Column :header="t('views.projects.groupStatus')">
                    <template #body="{ data }">
                        <i class="pi pi-lock" v-if="data.isLocked()" />
                        <i class="pi pi-unlock" v-else />
                    </template>
                </Column>
            </DataTable>
        </template>
        <template v-else>
            {{ t('views.projects.noGroups') }}
        </template>
        <Dialog
            v-if="selectedGroup !== null"
            v-model:visible="dialogVisible"
            modal
            :header="`${t('views.projects.group')} ${project.getGroupNumber(selectedGroup)}`"
            :style="{ width: '25rem' }"
        >
            <template v-if="selectedGroup.students.length > 0">
                <ul v-if="selectedGroup.students" class="mt-0">
                    <li v-for="student in selectedGroup.students" :key="student.id">
                        {{ student.first_name }} {{ student.last_name }}
                    </li>
                </ul>
            </template>
            <template v-else>
                {{ t('views.projects.noStudents') }}
            </template>
            <Button
                class="mt-3"
                @click="joinSelectedGroup"
                :icon="PrimeIcons.ARROW_RIGHT"
                :label="t('views.projects.joinGroup')"
                icon-pos="right"
                outlined
            />
        </Dialog>
    </div>
</template>

<style scoped lang="scss"></style>
