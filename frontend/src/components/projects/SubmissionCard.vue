<script setup lang="ts">
/* Component props */
import { type Project } from '@/types/Project.ts';
import { PrimeIcons } from 'primevue/api';
import Card from 'primevue/card';
import { useI18n } from 'vue-i18n';
import { computed, onMounted } from 'vue';
import { useSubmission } from '@/composables/services/submission.service.ts';
import { type Group } from '@/types/Group.ts';
import Button from 'primevue/button';

const { t } = useI18n();
const { submissions, getSubmissionByGroup } = useSubmission();

const props = defineProps<{
    project: Project;
    group: Group;
}>();

onMounted(async () => {
    await getSubmissionByGroup(props.group.id);
});

const formattedDeadline = computed(() => {
    // changes deadline format to dd/mm.yyyy
    const date = new Date(props.project.deadline);
    return `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()}`;
});
</script>

<template>
    <Card class="border-round">
        <template #content>
            <div>
                <div class="mb-3">
                    <i :class="['pi', PrimeIcons.CALENDAR_PLUS, 'icon-color']" class="mr-2"></i>
                    {{ t('views.projects.deadline') }}: {{ formattedDeadline }}<br />
                </div>
                <div>
                    <i :class="['pi', PrimeIcons.INFO_CIRCLE, 'icon-color']" class="mr-2"></i>
                    {{ t('views.projects.submissionStatus') }}:
                    {{ submissions ? submissions.at(-1)?.structure_checks_passed : 'false' }}
                </div>
            </div>
        </template>
        <template #footer>
            <RouterLink
                :to="{
                    name: 'submission',
                    params: { groupId: props.group.id },
                }"
            >
                <Button :icon="PrimeIcons.ARROW_RIGHT" :label="t('components.submission')" icon-pos="right" outlined />
            </RouterLink>
        </template>
    </Card>
</template>

<style scoped lang="scss"></style>
@/types/Project
