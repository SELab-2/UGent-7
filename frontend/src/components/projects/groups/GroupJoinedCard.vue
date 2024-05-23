<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { type Group } from '@/types/Group.ts';
import { storeToRefs } from 'pinia';
import { useAuthStore } from '@/store/authentication.store.ts';
import { PrimeIcons } from 'primevue/api';
import Button from 'primevue/button';

/* Props */
const props = defineProps<{
    group: Group;
}>();

/* Emits */
const emit = defineEmits(['leave:group']);

/* Composable injections */
const { student } = storeToRefs(useAuthStore());
const { t } = useI18n();

/**
 * Leaves the selected group.
 */
async function leaveGroup(): Promise<void> {
    if (student.value !== null) {
        emit('leave:group', props.group, student.value);
    }
}
</script>

<template>
    <div class="border-round p-4 surface-100 border-1 border-300">
        <h2 class="mt-0">
            {{ t('views.projects.groupMembers') }}
        </h2>
        <div class="flex flex-column gap-3 my-4">
            <div class="flex align-items-center gap-2" v-for="student in group.students" :key="student.id">
                <i class="pi pi-user" /> <span>{{ student.getFullName() }}</span>
            </div>
        </div>
        <Button
            @click="leaveGroup"
            :icon="PrimeIcons.ARROW_RIGHT"
            :label="t('views.projects.leaveGroup')"
            icon-pos="right"
            outlined
        />
    </div>
</template>

<style lang="scss"></style>
