<script setup lang="ts">
import FileUpload, { type FileUploadUploaderEvent } from 'primevue/fileupload';
import InputText from 'primevue/inputtext';
import AdminLayout from '@/components/layout/admin/AdminLayout.vue';
import Title from '@/components/layout/Title.vue';
import Body from '@/components/layout/Body.vue';
import { create } from '@/composables/services/helpers.ts';
import { Response } from '@/types/Response.ts';
import { endpoints } from '@/config/endpoints.ts';
import { useI18n } from 'vue-i18n';
import { ref } from 'vue';

const { t } = useI18n();

const response = ref<Response | null>(null);
const name = ref('');

const upload = async (event: FileUploadUploaderEvent): Promise<void> => {
    const files: File[] = event.files as File[];
    const endpoint = endpoints.dockerImages.index;
    const data = {
        'file': files[0],
        'name': name.value,
    }
    await create<Response>(endpoint, data, response, Response.fromJSON, 'multipart/form-data');
    name.value = '';
};
</script>

<template>
    <AdminLayout>
        <Title>
            <div class="gap-3 mb-3">{{ t('admin.docker_images.title') }}</div>
        </Title>
        <Body>
            <InputText
                class="mb-3 gap-3"
                v-model:model-value="name"
                :placeholder="t('admin.docker_images.name')"
            />
            <FileUpload
                v-if="name.length > 0"
                class="mb-3 gap-3"
                :custom-upload="true"
                @uploader="upload"
                :file-limit="1"
            >
                <template #empty>
                    <strong>No file selected.</strong>
                </template>
            </FileUpload>
        </Body>
    </AdminLayout>
</template>

<style scoped lang="scss"></style>
