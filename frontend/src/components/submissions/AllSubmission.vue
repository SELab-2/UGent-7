<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { Submission } from '@/types/submission/Submission.ts';
import { type Group } from '@/types/Group.ts';
import Tooltip from 'primevue/tooltip';
import { useSubmission } from '@/composables/services/submission.service.ts';
import { ExtraCheckResult } from '@/types/submission/ExtraCheckResult.ts';
import { StructureCheckResult } from '@/types/submission/StructureCheckResult.ts';

const { submissions, getSubmissionByGroup } = useSubmission();

const testSubmissions = ref<Submission[]>([
    new Submission(
        '1',
        1,
        new Date(),
        [],
        [new ExtraCheckResult('1', 'FAILURE', null, null, 1, 1, 'ExtraCheckResult')],
        [new StructureCheckResult('1', 'FAILURE', null, 1, 1, 'StructureCheckResult')],
        true,
    ),
    new Submission(
        '2',
        2,
        new Date(),
        [],
        [new ExtraCheckResult('2', 'SUCCESS', null, null, 2, 1, 'ExtraCheckResult')],
        [new StructureCheckResult('2', 'FAILURE', null, 2, 1, 'StructureCheckResult')],
        true,
    ),
    new Submission(
        '3',
        3,
        new Date(),
        [],
        [new ExtraCheckResult('3', 'FAILURE', null, null, 2, 1, 'ExtraCheckResult')],
        [new StructureCheckResult('3', 'SUCCESS', null, 2, 1, 'StructureCheckResult')],
        true,
    ),
    new Submission(
        '4',
        4,
        new Date(),
        [],
        [new ExtraCheckResult('3', 'SUCCESS', null, null, 2, 1, 'ExtraCheckResult')],
        [new StructureCheckResult('3', 'SUCCESS', null, 2, 1, 'StructureCheckResult')],
        true,
    ),
]);

const props = defineProps<{
    group: Group;
}>();

onMounted(async () => {
    await getSubmissionByGroup(props.group.id);
    console.log('submissions');
    console.log(submissions.value?.at(-1));
    submissions.value = testSubmissions.value;
});

const submissionsExtra = computed(() => {
    const result =
        submissions.value != null
            ? submissions.value.map((submission) => {
                  const iconDetails = getIcon(submission);
                  return {
                      ...submission,
                      iconName: iconDetails.iconName,
                      color: iconDetails.color,
                      // hoverText: getHoverText(submission),
                  };
              })
            : null;
    return result;
});

const getIcon = (submission: Submission): { iconName: string; color: string } => {
    if (
        !(
            submission.extraCheckResults.map((check: ExtraCheckResult) => check.result === 'SUCCESS').every(Boolean) ||
            submission.structureCheckResults
                .map((check: StructureCheckResult) => check.result === 'SUCCESS')
                .every(Boolean)
        )
    ) {
        return { iconName: 'times', color: 'red' };
    } else if (
        !submission.extraCheckResults.map((check: ExtraCheckResult) => check.result === 'SUCCESS').every(Boolean)
    ) {
        return { iconName: 'cloud', color: 'lightblue' };
    } else if (
        !submission.structureCheckResults
            .map((check: StructureCheckResult) => check.result === 'SUCCESS')
            .every(Boolean)
    ) {
        return { iconName: 'bolt', color: 'yellow' };
    } else {
        return { iconName: 'check', color: 'lightgreen' };
    }
};
/*
const getHoverText = (submission: Submission): string => {
    if (submission) return '';
};

 */
</script>

<template>
    <div>
        <div
            v-for="submission in submissionsExtra"
            class="flex submission align-content-center align-items-center"
            v-tooltip="submission"
        >
            <p
                :class="'font-semibold m-2 p-1 pi pi-' + submission.iconName"
                :style="{ color: submission.color, fontSize: '1.25rem' }"
            ></p>
            <label>#{{ submission.submission_number }}</label>
        </div>
    </div>
</template>

<style scoped lang="scss">
@import '@/assets/scss/theme/theme.scss';
.submission {
    border-bottom: 1.5px solid black;
}
.submission:last-child {
    border-bottom: none;
}
</style>
