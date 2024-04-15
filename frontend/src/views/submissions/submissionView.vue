<script setup lang="ts">
import BaseLayout from '@/components/layout/BaseLayout.vue';
import Title from '@/components/layout/Title.vue';
import Button from 'primevue/button';
import { useI18n } from 'vue-i18n';
import { onMounted, ref } from 'vue';
import { useProject } from '@/composables/services/project.service.ts';
import { useRoute } from 'vue-router';
import { useCourses } from '@/composables/services/course.service.ts';
import FileUpload from 'primevue/fileupload';
import { PrimeIcons } from 'primevue/api';
import AllSubmission from '@/components/submissions/AllSubmission.vue';
import { useGroup } from '@/composables/services/groups.service.ts';
import { useSubmission } from '@/composables/services/submission.service.ts';

const { t } = useI18n();
const route = useRoute();
const { project, getProjectByID } = useProject();
const { course, getCourseByID } = useCourses();
const { group, getGroupByID } = useGroup();
const { submission, createSubmission } = useSubmission();

/* State */
const files = ref<File[]>([]);

onMounted(async () => {
    await getProjectByID(route.params.projectId as string);
    await getCourseByID(route.params.courseId as string);
    await getGroupByID(route.params.groupId as string);
});

const onUpload = (callback: () => void): void => {
    if (group.value !== null) {
        createSubmission(files.value as File[], group.value.id);
        files.value = [];
        callback();

    }
};

const onFileSelect = (event: any): void => {
    files.value = [...files.value, ...event.files];
};

const removeFile = (removeFileCallback: (index: number) => void, index: number): void => {
    removeFileCallback(index);
    files.value.splice(index, 1);
};

function formatDate(deadline: Date): string {
    // changes deadline format to dd/mm.yyyy
    return `${deadline.getDate()}/${deadline.getMonth() + 1}/${deadline.getFullYear()}`;
}
</script>

<template>
    <BaseLayout>
        <div class="grid">
            <div class="col-12 md:col-4">
                <div>
                    <Title> {{ t(`views.submissions.title`) }}: {{ project ? project.name : 'Loading' }} </Title>
                    <p v-if="course">{{ t(`views.submissions.course`) }}: {{ course.name }}</p>
                    <p v-if="project?.deadline">Deadline: {{ project ? formatDate(project.deadline) : 'Loading' }}</p>
                    <div class="py-2">
                        <h1 class="pb-2">
                            {{ t(`views.submissions.submit`) }}
                        </h1>
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
                    </div>
                </div>
            </div>
            <div class="col-6 col-offset-1">
                <AllSubmission v-if="group" :group="group"></AllSubmission>
            </div>
        </div>
    </BaseLayout>
</template>

<style scoped lang="scss">
@import '@/assets/scss/theme/theme.scss';

h1 {
    color: $primaryDarkColor;
}
</style>
