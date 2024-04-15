<script setup lang="ts">
import { useStudents } from '@/composables/services/student.service.ts';
import { onMounted, watch } from 'vue';
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
const emit = defineEmits(['group-left']);

/* Composable injections */
const { student } = storeToRefs(useAuthStore());
const { students, getStudentsByGroup, studentLeaveGroup } = useStudents();
const { t } = useI18n();

watch(
    () => props.group,
    async (newGroup) => {
        await getStudentsByGroup(newGroup.id);
    },
    { deep: true, immediate: true },
);

/**
 * Leaves the selected group.
 */
async function leaveSelectedGroup(): Promise<void> {
    if (student.value !== null) {
        await studentLeaveGroup(props.group.id, student.value.id);
        emit('group-left', null);
    }
}

onMounted(async () => {
    await getStudentsByGroup(props.group.id);
});
</script>

<template>
    <div class="groupcard">
        <h2>{{ t('views.projects.groupMembers') }}</h2>
        <div class="mt-4">
            <p v-for="student in students" :key="student.id">{{ student.first_name }} {{ student.last_name }}</p>
        </div>
        <Button
            class="mt-3"
            @click="leaveSelectedGroup"
            :icon="PrimeIcons.ARROW_RIGHT"
            :label="t('views.projects.leaveGroup')"
            icon-pos="right"
            outlined
        />
    </div>
</template>

<style lang="scss">
@import '@/assets/scss/theme/theme.scss';

.groupcard {
    background-color: white;
    border-radius: $borderRadius;
    padding: $cardBodyPadding;
    border-style: solid;
    border-color: $primaryLightColor;
    border-width: $borderWidth;
    color: $primaryColor;

    div {
        p {
            color: $textSecondaryColor;
            padding-bottom: 1rem;
            margin-bottom: 1rem;
            border-bottom: 1px solid #e0e0e0;
        }

        /* Zorgt ervoor dat er geen lijn onder de laatste naam staat */
        p:last-child {
            border-bottom: none;
            padding-bottom: 0;
        }
    }
}
</style>
