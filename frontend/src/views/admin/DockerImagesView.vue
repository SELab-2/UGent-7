<script setup lang="ts">
import FileUpload, { type FileUploadUploaderEvent } from 'primevue/fileupload';
import InputText from 'primevue/inputtext';
import InputSwitch from 'primevue/inputswitch';
import SelectButton from 'primevue/selectbutton';
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
const public_status = ref(false);

const selectOptions = ref(['admin.list', 'admin.add'])
const selected = ref<string>(t(selectOptions.value[0]));

const upload = async (event: FileUploadUploaderEvent): Promise<void> => {
    const files: File[] = event.files as File[];
    const endpoint = endpoints.dockerImages.index;
    const data = {
        file: files[0],
        name: name.value,
        public: public_status.value
    };
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
            <SelectButton class="mb-3 gap-3" v-model="selected" :options="selectOptions.map(t)"/>
            <div v-if="selected === t(selectOptions[0])">

            </div>
            <div v-else>
                <InputText class="mb-3 gap-3" v-model:model-value="name" :placeholder="t('admin.docker_images.name')" />
                <div v-if="name.length > 0">
                    <div class="flex align-items-center mb-3 gap-3">
                        <label class="font-semibold w-12rem">{{ t('admin.docker_images.public') }}</label>
                        <InputSwitch v-model:model-value="public_status" />
                    </div>
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
                </div>
            </div>
        </Body>
    </AdminLayout>
</template>

<style scoped lang="scss"></style>
