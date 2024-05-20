<script setup lang="ts">
import Button from 'primevue/button';
import { PrimeIcons } from 'primevue/api';
import { useI18n } from 'vue-i18n';
import { onMounted } from 'vue';
import { useSubmission } from '@/composables/services/submission.service.ts';
import { type Project } from '@/types/Project.ts';

/* Props */
const props = defineProps<{
    project: Project;
}>();

/* Composable injections */
const { t } = useI18n();
const { submissions, getSubmissionByGroup } = useSubmission();

/* Functions */
const testSubmission = async (): Promise<void> => {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.addEventListener('change', (event) => {
        const file = (event.target as HTMLInputElement).files[0];
        if (file) {
            alert(`Selected file: ${file.name}`);
        }
    });
    fileInput.click();
};

</script>

<template>
    <Button @click="testSubmission">
        Upload a test submission
    </Button>
</template>

<style scoped lang="scss"></style>
