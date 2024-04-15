<script setup lang="ts">
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
import Dialog from 'primevue/dialog';
import { useStudents } from '@/composables/services/student.service.ts';
import { storeToRefs } from 'pinia';
import { useAuthStore } from '@/store/authentication.store.ts';
import { type Group } from '@/types/Group.ts';
import { PrimeIcons } from 'primevue/api';
import Button from 'primevue/button';

/* Props */
defineProps<{
    groups: Group[];
}>();

/* Composable injections */
const { t } = useI18n();
const { student } = storeToRefs(useAuthStore());
const { students, getStudentsByGroup, studentJoinGroup } = useStudents();

/* Emits */
const emit = defineEmits(['group-joined']);

/* State */
const dialogVisible = ref<boolean>(false);
const selectedGroup = ref<Group | null>(null);

/**
 * Shows the group dialog.
 *
 * @param group
 */
async function showGroupDialog(group: Group): Promise<void> {
    selectedGroup.value = group;
    await getStudentsByGroup(group.id);
    dialogVisible.value = true;
}

/**
 * Joins the selected group.
 *
 */
async function joinSelectedGroup(): Promise<void> {
    if (selectedGroup.value !== null && student.value !== null) {
        await studentJoinGroup(selectedGroup.value.id, student.value.id);
        dialogVisible.value = false;
        emit('group-joined', selectedGroup.value);
    }
}
</script>

<template>
    <div>
        <div class="groupcard">
            <h2>{{ t('views.projects.chooseGroup') }}</h2>
            <div v-if="groups">
                <button
                    class="groupSelectionButton p-3"
                    v-for="group in groups"
                    :key="group.id"
                    @click="showGroupDialog(group)"
                >
                    {{ t('views.projects.group') }} {{ group.id }}
                </button>
            </div>
            <Dialog
                v-model:visible="dialogVisible"
                modal
                :header="`${t('views.projects.group')} ${selectedGroup?.id}`"
                :style="{ width: '25rem' }"
            >
                <ul v-if="students">
                    <li v-for="student in students" :key="student.id">
                        {{ student.first_name }} {{ student.last_name }}
                    </li>
                </ul>
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
    </div>
</template>

<style scoped lang="scss">
@import '@/assets/scss/theme/theme.scss';
.groupSelectionButton {
    display: block;
    background: none;
    border: none;
    text-align: left;
    font-size: $fontSize;
    padding: 0.5rem 1rem;
    cursor: pointer;
    color: $textSecondaryColor;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid #e0e0e0;
    :last-child {
        border-bottom: none;
    }
}
.groupSelectionButton:last-child {
    border-bottom: none;
}
</style>
