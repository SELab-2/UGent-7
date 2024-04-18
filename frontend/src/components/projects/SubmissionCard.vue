<script setup lang="ts">
import Button from 'primevue/button';
import { PrimeIcons } from 'primevue/api';
import { useI18n } from 'vue-i18n';
import { onMounted } from 'vue';
import { useSubmission } from '@/composables/services/submission.service.ts';
import { type Group } from '@/types/Group.ts';

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
                    {{ submissions ? submissions.at(-1)?.structure_checks_passed : 'false' }}
                </div>
            </div>
            <RouterLink :to="{ name: 'submission' }">
                <Button :icon="PrimeIcons.ARROW_RIGHT" :label="t('components.submission')" icon-pos="right" outlined />
            </RouterLink>
        </div>
    </template>
</template>

<style scoped lang="scss"></style>
