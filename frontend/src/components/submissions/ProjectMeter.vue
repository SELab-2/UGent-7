<script setup lang="ts">
import MeterGroup from 'primevue/metergroup';
import Skeleton from 'primevue/skeleton';
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { type Project } from '@/types/Project.ts';

/* Props */
const props = defineProps<{
    project: Project | null;
}>();

/* Composable injections */
const { t } = useI18n();

/* State */
const meterItems = computed(() => {
    const groups = props.project !== null ? props.project.status.non_empty_groups : 0;
    const groupsSubmitted = props.project !== null ? props.project.status.groups_submitted : 0;
    const hasStructurechecks = props.project !== null ? props.project.status.has_structure_checks : false;
    const hasExtraChecks = props.project !== null ? props.project.status.has_extra_checks : false;
    const extraChecksPassed = props.project !== null ? props.project.status.extra_checks_passed : 0;
    const structureChecksPassed = props.project !== null ? props.project.status.structure_checks_passed : 0;
    const submissionsFailed = groupsSubmitted - structureChecksPassed;

    const extraChecksFailed = structureChecksPassed - extraChecksPassed;

    const green = '#76DD78';
    const orange = '#FFB84F';
    const red = '#F37142';

    const submissionsFailedItem = {
        value: (submissionsFailed / groups) * 100,
        color: red,
        label: t('components.card.testsFail'),
        icon: 'pi pi-times',
    };
    const structureChecksPassedItem = {
        value: (extraChecksFailed / groups) * 100,
        color: orange,
        label: t('components.card.structureTestsSucceed'),
        icon: 'pi pi-exclamation-circle',
    };
    const extraChecksPassedItem = {
        value: (extraChecksPassed / groups) * 100,
        color: green,
        label: t('components.card.extraTestsSucceed'),
        icon: 'pi pi-check',
    };

    if (hasStructurechecks) {
        if (hasExtraChecks) {
            return [submissionsFailedItem, structureChecksPassedItem, extraChecksPassedItem];
        }
        structureChecksPassedItem.color = green;
        structureChecksPassedItem.icon = 'pi pi-check';
        return [submissionsFailedItem, structureChecksPassedItem];
    }
    return [
        {
            value: (groupsSubmitted / groups) * 100,
            color: green,
            label: t('components.card.successfulSubmission'),
            icon: 'pi pi-check',
        },
    ];
});
</script>

<template>
    <template v-if="project !== null">
        <template v-if="project.status.groups_submitted > 0">
            <MeterGroup :value="meterItems" labelOrientation="horizontal">
                <template #start>
                    <div class="flex justify-between mt-2 relative">
                        <span>
                            {{ project.status.groups_submitted }}
                            {{ t('components.card.submissions', project.status.groups_submitted) }}
                        </span>
                        <span class="w-full absolute text-right">
                            {{ project.status.non_empty_groups }}
                            {{ t('components.card.groups', project.status.non_empty_groups) }}
                        </span>
                    </div>
                </template>
            </MeterGroup>
        </template>
        <template v-else>
            <p class="mb-0">{{ t('components.card.noSubmissions') }}</p>
        </template>
    </template>
    <template v-else>
        <Skeleton height="10rem" />
    </template>
</template>

<style scoped lang="scss"></style>
