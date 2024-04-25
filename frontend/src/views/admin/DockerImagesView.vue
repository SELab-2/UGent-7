<script setup lang="ts">
import DataTable from 'primevue/datatable';
import FileUpload, { type FileUploadUploaderEvent } from 'primevue/fileupload';
import InputText from 'primevue/inputtext';
import InputSwitch from 'primevue/inputswitch';
import SelectButton from 'primevue/selectbutton';
import AdminLayout from '@/components/layout/admin/AdminLayout.vue';
import Title from '@/components/layout/Title.vue';
import Body from '@/components/layout/Body.vue';
import { useDockerImages } from '@/composables/services/docker.service.ts';
import { useI18n } from 'vue-i18n';
import { ref } from 'vue';
import {DockerImage} from "@/types/DockerImage.ts";

/* Injection */
const { t } = useI18n();
const { pagination, searchDockerImages, createDockerImage } = useDockerImages();

const addItem = ref<DockerImage>(DockerImage.blankDockerImage())

const selectOptions = ref(['admin.list', 'admin.add']);
const selected = ref<string>(t(selectOptions.value[0]));

const upload = async (event: FileUploadUploaderEvent): Promise<void> => {
    const files: File[] = event.files as File[];
    await createDockerImage(addItem.value, files[0]);
    addItem.value.name = '';
};
</script>

<template>
    <AdminLayout>
        <Title>
            <div class="gap-3 mb-3">{{ t('admin.docker_images.title') }}</div>
        </Title>
        <Body>
            <SelectButton class="mb-3 gap-3" v-model="selected" :options="selectOptions.map(t)" />
            <div v-if="selected === t(selectOptions[0])">
                <DataTable
                    :value="pagination?.results"
                    lazy
                    paginator
                    v-mode:f>

                </DataTable>
            </div>
            <div v-else>
                <InputText class="mb-3 gap-3" v-model:model-value="addItem.name" :placeholder="t('admin.docker_images.name')" />
                <div v-if="addItem.name.length > 0">
                    <div class="flex align-items-center mb-3 gap-3">
                        <label class="font-semibold w-12rem">{{ t('admin.docker_images.public') }}</label>
                        <InputSwitch v-model:model-value="addItem.public" />
                    </div>
                    <FileUpload
                        class="mb-3 gap-3"
                        :custom-upload="true"
                        @uploader="upload"
                        :file-limit="1"
                    >
                        <template #empty>
                            <strong>No file selected.</strong>
                        </template>
                    </FileUpload>
                </div>
            </div>
        </Body>
    </AdminLayout>
</template>

<style scoped lang="scss"></style>
