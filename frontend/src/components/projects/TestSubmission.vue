<script setup lang="ts">
import Button from 'primevue/button';
import { PrimeIcons } from 'primevue/api';
import { onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useSubmission } from '@/composables/services/submission.service.ts';
import { type Project } from '@/types/Project.ts';
import FileUpload from 'primevue/fileupload';
import { ExtraCheckResult } from '@/types/submission/ExtraCheckResult.ts';
import { StructureCheckResult } from '@/types/submission/StructureCheckResult.ts';

/* State */
const files = ref<File[]>([]);

/* Props */
const props = defineProps<{
    project: Project;
}>();

/* Composable injections */
const { t } = useI18n();
const { submission, submissions, createTestSubmission } = useSubmission();

/* Functions */
const onFileSelect = (event: any): void => {
    files.value = [...files.value, ...event.files];
};

const removeFile = (removeFileCallback: (index: number) => void, index: number): void => {
    removeFileCallback(index);
    files.value.splice(index, 1);
};

const onUpload = async (callback: () => void): Promise<void> => {
    if (props.project !== null) {
        await createTestSubmission(files.value as File[], props.project.id);
        if (submission.value != null) {
            submissions.value = [...(submissions.value ?? []), submission.value];
            alert("make submission")
        }
        files.value = [];
        callback();
    }
};

</script>

<template>
    <FileUpload
        class="justify-between"
        :show-cancel-button="false"
        :multiple="true"
        :chooseLabel="t(`views.submissions.chooseFile`)"
        @select="onFileSelect"
    >
        <template #header="{ chooseCallback, clearCallback, files }">
            <div class="flex justify-content-between align-items-center flex-1 gap-2">
                <Button
                    @click="chooseCallback()"
                    :icon="PrimeIcons.PLUS"
                    :label="t(`views.submissions.chooseFile`)"
                ></Button>
                <Button
                    @click="onUpload(clearCallback)"
                    :label="`Upload`"
                    :icon="PrimeIcons.UPLOAD"
                    :disabled="!files || files.length === 0"
                ></Button>
            </div>
        </template>
        <template #content="{ files, removeFileCallback }">
            <div v-if="files.length > 0" class="flex-column">
                <div
                    v-for="(file, index) of files"
                    :key="file.name + file.type + file.size"
                    class="m-0 p-0 flex sm:p-2 justify-content-between align-items-center"
                >
                    <span class="font-semibold">{{ file.name }}</span>
                    <Button
                        class="w-2rem h-2rem"
                        icon="pi pi-times"
                        @click="removeFile(removeFileCallback, index)"
                        outlined
                        rounded
                        severity="danger"
                    />
                </div>
            </div>
        </template>
    </FileUpload>
</template>

<style scoped lang="scss"></style>
