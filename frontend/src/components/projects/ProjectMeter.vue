<script setup lang="ts">
import MeterGroup from 'primevue/metergroup';
import Skeleton from 'primevue/skeleton';
import { computed } from 'vue';
import { type SubmissionStatus } from '@/types/SubmisionStatus.ts';
import { useI18n } from 'vue-i18n';

/* Props */
const props = defineProps<{
    submissionStatus: SubmissionStatus | null;
}>();

/* Composable injections */
const { t } = useI18n();

/* State */
const meterItems = computed(() => {
    const groups = props.submissionStatus !== null ? props.submissionStatus.non_empty_groups : 0;
    const groupsSubmitted = props.submissionStatus !== null ? props.submissionStatus.groups_submitted : 0;
    const submissionsPassed = props.submissionStatus !== null ? props.submissionStatus.submissions_passed : 0;
    const submissionsFailed = groupsSubmitted - submissionsPassed;
    return [
        {
            value: (submissionsPassed / groups) * 100,
            color: '#749b68',
            label: t('components.card.testsSucceed'),
            icon: 'pi pi-check',
        },
        {
            value: (submissionsFailed / groups) * 100,
            color: '#FF5445',
            label: t('components.card.testsFail'),
            icon: 'pi pi-times',
        },
    ];
});
</script>

<template>
    <template v-if="submissionStatus !== null">
        <template v-if="submissionStatus.groups_submitted > 0">
            <MeterGroup :value="meterItems" labelOrientation="vertical">
                <template #start>
                    <div class="flex justify-between mt-2 relative">
                        <span>
                            {{ submissionStatus.groups_submitted }}
                            {{ t('components.card.submissions', submissionStatus.groups_submitted) }}
                        </span>
                        <span class="w-full absolute text-right">
                            {{ submissionStatus.non_empty_groups }}
                            {{ t('components.card.groups', submissionStatus.non_empty_groups) }}
                        </span>
                    </div>
                </template>
            </MeterGroup>
        </template>
        <template v-else>
            {{ t('components.card.noSubmissions') }}
        </template>
    </template>
    <template v-else>
        <Skeleton height="10rem" />
    </template>
</template>

<style scoped lang="scss"></style>
