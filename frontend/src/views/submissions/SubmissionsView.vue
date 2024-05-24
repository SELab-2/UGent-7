<script setup lang="ts">
import Button from 'primevue/button';
import FileUpload from 'primevue/fileupload';
import { PrimeIcons } from 'primevue/api';
import Loading from '@/components/Loading.vue';
import { useI18n } from 'vue-i18n';
import { onMounted, ref } from 'vue';
import { useProject } from '@/composables/services/project.service.ts';
import { useRoute } from 'vue-router';
import AllSubmission from '@/components/submissions/AllSubmission.vue';
import ProjectStructure from '@/components/projects/ProjectStructure.vue';
import { useGroup } from '@/composables/services/group.service.ts';
import { useSubmission } from '@/composables/services/submission.service.ts';
import { useStructureCheck } from '@/composables/services/structure_check.service.ts';
import { useMessagesStore } from '@/store/messages.store.ts';
import BaseLayout from '@/views/layout/base/BaseLayout.vue';
import Title from '@/views/layout/Title.vue';

const { t } = useI18n();
const route = useRoute();
const { project, getProjectByID } = useProject();
const { group, getGroupByID } = useGroup();
const { submission, submissions, createSubmission, getSubmissionByGroup } = useSubmission();
const { structureChecks, getStructureCheckByProject } = useStructureCheck();
const { addSuccessMessage, addErrorMessage } = useMessagesStore();

/* State */
const files = ref<File[]>([]);

/**
 * Fetches the project, course and group data on component mount
 *
 * @param callback
 */
const onUpload = async (callback: () => void): Promise<void> => {
    if (group.value !== null) {
        try {
            await createSubmission(files.value as File[], group.value.id, false);
            addSuccessMessage(t('toasts.messages.success'), t('toasts.messages.submissions.create.success'));

            if (submission.value != null) {
                submissions.value = [...(submissions.value ?? []), submission.value];
            }

            files.value = [];
            callback();
        } catch (e) {
            addErrorMessage(t('toasts.messages.error'), t('toasts.messages.submissions.create.error'));
        }
    }
};

/**
 * Adds the selected files to the files array
 *
 * @param event
 */
const onFileSelect = (event: any): void => {
    files.value = [...files.value, ...event.files];
};

/**
 * Removes a file from the files array
 *
 * @param removeFileCallback
 * @param index
 */
const removeFile = (removeFileCallback: (index: number) => void, index: number): void => {
    removeFileCallback(index);
    files.value.splice(index, 1);
};

/* Lifecycle hooks */
onMounted(async () => {
    await getProjectByID(route.params.projectId as string);
    await getGroupByID(route.params.groupId as string);
    await getSubmissionByGroup(route.params.groupId as string);

    if (project.value !== null) {
        await getStructureCheckByProject(project.value.id);
    }
});
</script>

<template>
    <BaseLayout>
        <Title> {{ t(`views.submissions.title`) }}: {{ project ? project.name : 'Loading' }} </Title>
        <template v-if="group !== null && submissions != null && structureChecks !== null">
            <div class="grid fadein">
                <div class="col-12 md:col-6">
                    <div class="flex-column">
                        <!-- Project info column -->
                        <!-- Submission structure -->
                        <ProjectStructure :structure-checks="structureChecks" />

                        <!-- Submission upload -->
                        <div class="py-2">
                            <h2>{{ t('views.submissions.submit') }}</h2>
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
                                <template #empty>
                                    <span>{{ t('views.submissions.noFiles') }}</span>
                                </template>
                            </FileUpload>
                        </div>
                    </div>
                </div>
                <!-- Overview of all given submissions -->
                <div class="col-12 md:col-5 col-offset-1">
                    <h2>{{ t('views.submissions.allSubmissions') }}</h2>
                    <AllSubmission
                        v-if="group && submissions"
                        :group="group"
                        :submissions="submissions"
                    ></AllSubmission>
                </div>
            </div>
        </template>
        <template v-else>
            <Loading height="70vh" />
        </template>
    </BaseLayout>
</template>
