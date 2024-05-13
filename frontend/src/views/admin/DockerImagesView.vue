<script setup lang="ts">
import FileUpload, { type FileUploadUploaderEvent } from 'primevue/fileupload';
import InputText from 'primevue/inputtext';
import InputSwitch from 'primevue/inputswitch';
import ToggleButton from 'primevue/togglebutton';
import SelectButton from 'primevue/selectbutton';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import AdminLayout from '@/components/layout/admin/AdminLayout.vue';
import Title from '@/components/layout/Title.vue';
import Body from '@/components/layout/Body.vue';
import LazyDataTable from '@/components/admin/LazyDataTable.vue';
import { useDockerImages } from '@/composables/services/docker.service.ts';
import { useFilter } from '@/composables/filters/filter.ts';
import { useI18n } from 'vue-i18n';
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { DockerImage } from '@/types/DockerImage.ts';
import { getDockerImageFilters } from '@/types/filter/Filter.ts';
import InputIcon from 'primevue/inputicon';
import Column from 'primevue/column';
import IconField from 'primevue/iconfield';

/* Injection */
const { t } = useI18n();
const { query } = useRoute();
const { pagination, dockerImages, getDockerImages, searchDockerImages, patchDockerImage, createDockerImage } =
    useDockerImages();
const { filter, onFilter } = useFilter(getDockerImageFilters(query));

const dataTable = ref();

const editItem = ref<DockerImage>(DockerImage.blankDockerImage());
const addItem = ref<DockerImage>(DockerImage.blankDockerImage());

const selectOptions = ref(['admin.list', 'admin.add']);
const selected = ref<string>(t(selectOptions.value[0]));

const columns = ref([
    { field: 'id', header: 'admin.id' },
    { field: 'name', header: 'admin.docker_images.name' },
    { field: 'owner', header: 'admin.docker_images.owner' },
]);
// const publicOptions = ref<Array<{ value: any; label: string }>>([
//     { value: true, label: 'public' },
//     { value: false, label: 'private' },
// ]);
const showSafetyGuard = ref<boolean>(false);

const toggleSafetyGuard = (data: DockerImage): void => {
    editItem.value.public = !data.public;
    editItem.value.id = data.id;
    showSafetyGuard.value = true;
};
const changePublicStatus = async (dockerData: DockerImage): Promise<void> => {
    showSafetyGuard.value = false;
    await patchDockerImage(dockerData);
    await dataTable.value.fetch();
};
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
        <Body class="w-full">
            <SelectButton class="mb-3 gap-3 w-3" v-model="selected" :options="selectOptions.map(t)" />
            <div v-if="selected === t(selectOptions[0])">
                <LazyDataTable
                    :pagination="pagination"
                    :entities="dockerImages"
                    :get="getDockerImages"
                    :search="searchDockerImages"
                    :filter="filter"
                    :on-filter="onFilter"
                    ref="dataTable"
                >
                    <template #header>
                        <div class="flex justify-content-end">
                            <IconField iconPosition="left">
                                <InputIcon>
                                    <i class="pi pi-search" />
                                </InputIcon>
                                <InputText v-model="filter['search']" :placeholder="t('admin.search.general')" />
                            </IconField>
                        </div>
                    </template>
                    <Column
                        v-for="column in columns"
                        :key="column.field"
                        :field="column.field"
                        :header="t(column.header)"
                        :show-filter-menu="false"
                        :header-style="{ width: '25%' }"
                        class="p-col"
                    >
                        <template #filter>
                            <IconField iconPosition="left" class="flex align-items-center">
                                <InputIcon>
                                    <i class="pi pi-search flex justify-content-center" />
                                </InputIcon>
                                <InputText v-model="filter[column.field]" :placeholder="t('admin.search.search')" />
                            </IconField>
                        </template>
                    </Column>
                    <Column
                        key="public"
                        field="public"
                        :header="t('admin.docker_images.public')"
                        :header-style="{ width: '25%' }"
                        class="p-col"
                    >
                        <template #body="{ data }">
                            <InputSwitch
                                class="mb-3 gap-3 justify-content-center"
                                :model-value="data.public"
                                @click="() => toggleSafetyGuard(data)"
                            />
                        </template>
                    </Column>
                </LazyDataTable>
            </div>
            <div v-else>
                <InputText
                    class="mb-3 gap-3"
                    v-model:model-value="addItem.name"
                    :placeholder="t('admin.docker_images.name_input')"
                />
                <div v-if="addItem.name.length > 0">
                    <div class="flex align-items-center mb-3 gap-3">
                        <label class="font-semibold w-12rem">{{ t('admin.docker_images.public') }}</label>
                        <InputSwitch v-model:model-value="addItem.public" />
                    </div>
                    <FileUpload class="mb-3 gap-3" :custom-upload="true" @uploader="upload" :file-limit="1">
                        <template #empty>
                            <strong>No file selected.</strong>
                        </template>
                    </FileUpload>
                </div>
            </div>
        </Body>
    </AdminLayout>
    <Dialog v-model:visible="showSafetyGuard" :style="{ width: '15rem' }">
        <h3>Are you sure?</h3>
        <div class="flex justify-content-between">
            <Button label="No" @click="showSafetyGuard = false" />
            <Button label="Yes" @click="() => changePublicStatus(editItem)" />
        </div>
    </Dialog>
</template>

<style scoped lang="scss"></style>
