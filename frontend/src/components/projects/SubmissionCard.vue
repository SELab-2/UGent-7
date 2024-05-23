<script setup lang="ts">
import Button from 'primevue/button';
import { PrimeIcons } from 'primevue/api';
import { useI18n } from 'vue-i18n';
import { onMounted } from 'vue';
import { useSubmission } from '@/composables/services/submission.service.ts';
import { type Group } from '@/types/Group.ts';
import { type Submission } from '@/types/submission/Submission.ts';

/* Composable injections */
const { t } = useI18n();
const { submissions, getSubmissionByGroup } = useSubmission();

/* Component props */
const props = defineProps<{
    group: Group;
}>();

onMounted(async () => {
    await getSubmissionByGroup(props.group.id);
});

/**
 * Returns the icon name, color and hover text for the submission
 * @param submission
 */
const parseSubmissionStatus = (submission: Submission): string => {
    if (!submission.isSomePassed()) {
        return t('views.submissions.hoverText.allChecksFailed');
    } else if (!submission.isExtraCheckPassed()) {
        return t('views.submissions.hoverText.extraChecksFailed');
    } else if (!submission.isStructureCheckPassed()) {
        return t('views.submissions.hoverText.structureChecksFailed');
    } else {
        return t('views.submissions.hoverText.allChecksPassed');
    }
};
</script>

<template>
    <template v-if="group.project !== null">
        <div class="border-round surface-300 p-4">
            <div class="mb-3">
                <div class="mb-3">
                    <i :class="['pi', PrimeIcons.CALENDAR_PLUS, 'icon-color']" class="mr-2"></i>
                    {{ t('views.projects.deadline') }}: {{ group.project.getFormattedDeadline() }}<br />
                </div>
                <div>
                    <i :class="['pi', PrimeIcons.INFO_CIRCLE, 'icon-color']" class="mr-2"></i>
                    {{ t('views.projects.submissionStatus') }}:
                    <template v-if="submissions !== null">
                        <template v-if="submissions.length > 0">
                            {{ parseSubmissionStatus(submissions.at(-1)!) }}
                        </template>
                        <template v-else>
                            {{ t('views.submissions.noSubmissions') }}
                        </template>
                    </template>
                    <template v-else>
                        {{ t('helpers.loading') }}
                    </template>
                </div>
            </div>
            <RouterLink
                :to="{
                    name: 'submissions',
                    params: { groupId: props.group.id },
                }"
            >
                <Button :icon="PrimeIcons.ARROW_RIGHT" :label="t('components.submission')" icon-pos="right" outlined />
            </RouterLink>
        </div>
    </template>
</template>

<style scoped lang="scss"></style>
