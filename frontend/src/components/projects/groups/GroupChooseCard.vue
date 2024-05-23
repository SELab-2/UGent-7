<script setup lang="ts">
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Message from 'primevue/message';
import { ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { type Group } from '@/types/Group.ts';
import { PrimeIcons } from 'primevue/api';
import { type Student } from '@/types/users/Student.ts';
import { type Project } from '@/types/Project.ts';
import { useStudents } from '@/composables/services/student.service.ts';

/* Props */
const props = defineProps<{
    project: Project;
    groups: Group[];
    student: Student;
}>();

/* Composable injections */
const { t } = useI18n();
const { students, getStudentsByGroup } = useStudents();

/* Emits */
const emit = defineEmits(['join:group']);

/* State */
const dialogVisible = ref<boolean>(false);
const selectedGroup = ref<Group | null>(null);

/* Watch the selected group for changes */
watch(selectedGroup, async (group: Group | null) => {
    if (group !== null) {
        await getStudentsByGroup(group.id);
    }

    dialogVisible.value = true;
});

/**
 * Joins the selected group.
 *
 */
async function joinSelectedGroup(): Promise<void> {
    if (selectedGroup.value !== null) {
        emit('join:group', selectedGroup.value, props.student);
        selectedGroup.value = null;
        dialogVisible.value = false;
    }
}
</script>

<template>
    <div class="p-4 border-1 border-300 border-round-2xl">
        <h2 class="mt-0">
            {{ t('views.projects.chooseGroup') }}
        </h2>
        <Message severity="warn" class="my-4 text-sm" :closable="false">
            {{ t('views.projects.chooseGroupMessage', [project.getFormattedStartDate()]) }}
        </Message>
        <template v-if="groups.length > 0 && !project.isLocked()">
            <DataTable
                :value="groups"
                v-model:selection="selectedGroup"
                selection-mode="single"
                class="border-1 border-300"
            >
                <Column :header="t('views.projects.groupName')">
                    <template #body="{ data }">
                        {{ t('views.projects.group') }} {{ project.getGroupNumber(data) }}
                    </template>
                </Column>
                <Column :header="t('views.projects.groupPopulation')">
                    <template #body="{ data }">
                        <i class="pi pi-users mr-2" /> {{ data.getSize() }} / {{ project.group_size }}
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
            v-if="selectedGroup !== null && students !== null"
            v-model:visible="dialogVisible"
            modal
            :header="`${t('views.projects.group')} ${project.getGroupNumber(selectedGroup)}`"
            :style="{ width: '25rem' }"
        >
            <template v-if="students.length > 0">
                <ul class="mt-0">
                    <li v-for="student in students" :key="student.id">
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
