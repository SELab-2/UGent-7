<script setup lang="ts">
import FileUpload, { type FileUploadUploaderEvent } from 'primevue/fileupload';
import InputText from 'primevue/inputtext';
import InputSwitch from 'primevue/inputswitch';
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
const {
    pagination,
    dockerImages,
    getDockerImages,
    searchDockerImages,
    patchDockerImage,
    createDockerImage,
    deleteDockerImage,
} = useDockerImages();
const { filter, onFilter } = useFilter(getDockerImageFilters(query));

const dataTable = ref();

const editItem = ref<DockerImage>(DockerImage.blankDockerImage());
const addItem = ref<DockerImage>(DockerImage.blankDockerImage());

const selectOptions = ref(['admin.list', 'admin.add']);
const selectedOption = ref<string>(t(selectOptions.value[0]));

const multiRemove = ref<boolean>(false);
const selectedItems = ref<any[] | null>(null);

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
const safetyGuardFunction = ref<() => Promise<void>>(async () => {});

const safetyGuardCleanup = async (): Promise<void> => {
    showSafetyGuard.value = false;
    await safetyGuardFunction.value();
    await dataTable.value.fetch();
};
const toggleSafetyGuardEdit = (data: DockerImage): void => {
    editItem.value.public = !data.public;
    editItem.value.id = data.id;
    safetyGuardFunction.value = changePublicStatus;
    showSafetyGuard.value = true;
};
const changePublicStatus = async (): Promise<void> => {
    await patchDockerImage(editItem.value);
};
const upload = async (event: FileUploadUploaderEvent): Promise<void> => {
    const files: File[] = event.files as File[];
    await createDockerImage(addItem.value, files[0]);
    addItem.value.name = '';
};
const toggleSafetyGuardRemove = (data: DockerImage): void => {
    editItem.value = data;
    safetyGuardFunction.value = removeItem;
    showSafetyGuard.value = true;
};
const removeItem = async (): Promise<void> => {
    await deleteDockerImage(editItem.value.id);
};

const onSelect = (selected: any[] | null): void => {
    multiRemove.value = (selected?.length === undefined || selected?.length === 0) ?? false;
    selectedItems.value = selected;
};
</script>

<template>
    <AdminLayout>
        <Title>
            <div class="gap-3 mb-3">{{ t('admin.docker_images.title') }}</div>
        </Title>
        <Body class="w-full">
            <SelectButton class="mb-3 gap-3 w-3" v-model="selectedOption" :options="selectOptions.map(t)" />
            <div v-if="selectedOption === t(selectOptions[0])">
                <LazyDataTable
                    :pagination="pagination"
                    :entities="dockerImages"
                    :get="getDockerImages"
                    :search="searchDockerImages"
                    :filter="filter"
                    :on-filter="onFilter"
                    ref="dataTable"
                    @select="onSelect"
                >
                    <template #header>
                        <div class="mb-3 gap-3">
                            <IconField iconPosition="left">
                                <InputIcon>
                                    <i class="pi pi-search flex justify-content-center" />
                                </InputIcon>
                                <InputText v-model="filter['search']" :placeholder="t('admin.search.general')" />
                            </IconField>
                        </div>
                        <Button class="w-1 mb-3 gap-3" :disabled="multiRemove">
                            {{ t('admin.delete') }}
                        </Button>
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
                        :header-style="{ width: '10%' }"
                        class="p-col"
                    >
                        <template #body="{ data }">
                            <InputSwitch
                                class="mb-3 gap-3 justify-content-center"
                                :model-value="data.public"
                                @click="() => toggleSafetyGuardEdit(data)"
                            />
                        </template>
                    </Column>
                    <Column key="remove" :header-style="{ width: '11%' }" class="p-col">
                        <template #body="{ data }">
                            <Button @click="() => toggleSafetyGuardRemove(data)" class="justify-content-center">
                                {{ t('admin.delete') }}
                            </Button>
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
                <div class="flex align-items-center mb-3 gap-3">
                    <label class="font-semibold w-12rem">{{ t('admin.docker_images.public') }}</label>
                    <InputSwitch v-model="addItem.public" />
                </div>
                <FileUpload
                    class="mb-3 gap-3"
                    :custom-upload="true"
                    @uploader="upload"
                    :file-limit="1"
                    :disabled="addItem.name.length === 0"
                >
                    <template #empty>
                        <strong>No file selected.</strong>
                    </template>
                </FileUpload>
            </div>
        </Body>
    </AdminLayout>
    <Dialog v-model:visible="showSafetyGuard" :style="{ width: '15rem' }">
        <h3>{{ t('admin.safeGuard') }}</h3>
        <div class="flex justify-content-between">
            <Button :label="t('primevue.reject')" @click="showSafetyGuard = false" />
            <Button :label="t('primevue.accept')" @click="safetyGuardCleanup" />
        </div>
    </Dialog>
</template>

<style scoped lang="scss"></style>
