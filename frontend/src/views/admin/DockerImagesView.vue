<script setup lang="ts">
import FileUpload, { type FileUploadUploaderEvent } from 'primevue/fileupload';
import InputText from 'primevue/inputtext';
import InputSwitch from 'primevue/inputswitch';
import SelectButton from 'primevue/selectbutton';
import AdminLayout from '@/components/layout/admin/AdminLayout.vue';
import Title from '@/components/layout/Title.vue';
import Body from '@/components/layout/Body.vue';
import LazyDataTable from '@/components/admin/LazyDataTable.vue';
import { useDockerImages } from '@/composables/services/docker.service.ts';
import { useFilter } from "@/composables/filters/filter.ts";
import { useI18n } from 'vue-i18n';
import { ref } from 'vue';
import { useRoute } from "vue-router";
import { DockerImage } from "@/types/DockerImage.ts";
import { getDockerImageFilters } from "@/types/filter/Filter.ts";
import type {Role} from "@/types/users/User.ts";
import InputIcon from "primevue/inputicon";
import MultiSelect from "primevue/multiselect";
import Column from "primevue/column";
import IconField from "primevue/iconfield";

/* Injection */
const { t } = useI18n();
const { query } = useRoute();
const { pagination, dockerImages, getDockerImages, searchDockerImages, createDockerImage } = useDockerImages();
const { filter, onFilter } = useFilter(getDockerImageFilters(query));

const addItem = ref<DockerImage>(DockerImage.blankDockerImage())

const selectOptions = ref(['admin.list', 'admin.add']);
const selected = ref<string>(t(selectOptions.value[0]));

const columns = ref([
    { field: 'id', header: 'admin.users.id' },
    { field: 'username', header: 'admin.users.username' },
    { field: 'email', header: 'admin.users.email' },
    { field: 'roles', header: 'admin.users.roles' },
]);

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
                <LazyDataTable
                    :pagination="pagination"
                    :entities="dockerImages"
                    :get="getDockerImages"
                    :search="searchDockerImages"
                    :filter="filter"
                    :on-filter="onFilter">
                        <Column
                            v-for="column in columns"
                            :key="column.field"
                            :field="column.field"
                            :header="t(column.header)"
                            :show-filter-menu="false"
                            :style="{ minWidth: '14rem' }"
                        >
                            <template #filter>
                                <IconField
                                    iconPosition="left"
                                    class="flex align-items-center"
                                >
                                    <InputIcon>
                                        <i class="pi pi-search flex justify-content-center" />
                                    </InputIcon>
                                    <InputText v-model="filter[column.field]" :placeholder="t('admin.search.search')" />
                                </IconField>
                            </template>
                        </Column>
                </LazyDataTable>
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
