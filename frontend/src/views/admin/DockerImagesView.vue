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
import { computed, ref} from 'vue';
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
    deleteDockerImages
} = useDockerImages();
const { filter, onFilter } = useFilter(getDockerImageFilters(query));

/* State */
const dataTable = ref();

const editItem = ref<DockerImage>(DockerImage.blankDockerImage());
const addItem = ref<DockerImage>(DockerImage.blankDockerImage());

const selectOptions = ref(['admin.list', 'admin.add']);
const selectedOption = ref<string>(selectOptions.value[0]);

const multiRemove = computed(() => {
    return (selectedItems.value?.length === undefined || selectedItems.value?.length === 0) ?? false;
});
const selectedItems = ref<DockerImage[] | null>(null);

const columns = ref([
    { field: 'id', header: 'admin.id' },
    { field: 'name', header: 'admin.docker_images.name' },
    { field: 'owner', header: 'admin.docker_images.owner' },
]);
const showSafetyGuard = ref<boolean>(false);
const safetyGuardFunction = ref<() => Promise<void>>(async () => {});

const fileUpload = ref();

/**
 * Hides safety guard, executes function that safety guard guards against and fetches data again
 */
const safetyGuardCleanup = async (): Promise<void> => {
    showSafetyGuard.value = false;
    await safetyGuardFunction.value();
    await dataTable.value.fetch();
};
/**
 * Show safety guard for changing public status and set up values for when confirmed
 * @param data Docker Image data of docker image whose public status needs to be changed.
 */
const toggleSafetyGuardEdit = (data: DockerImage): void => {
    editItem.value.public = !data.public;
    editItem.value.id = data.id;
    safetyGuardFunction.value = changePublicStatus;
    showSafetyGuard.value = true;
};
/**
 * Changes the public status in the backend of the docker image whose attributes are in editItem's value attribute
 */
const changePublicStatus = async (): Promise<void> => {
    await patchDockerImage(editItem.value);
};
/**
 * Show safety guard for removing a docker image from the backend and set up values for when confirmed
 * @param data Docker Image data of docker image to be removed
 */
const toggleSafetyGuardRemove = (data: DockerImage): void => {
    editItem.value = data;
    safetyGuardFunction.value = removeItem;
    showSafetyGuard.value = true;
};
/**
 * Removes the docker image in the backend whose attributes are in editItem's value attribute
 */
const removeItem = async (): Promise<void> => {
    await deleteDockerImage(editItem.value.id);
    // remove the item from the list of selectedItems
    const index = selectedItems.value?.indexOf(editItem.value) ?? -1;
    if (index !== -1) {
        selectedItems.value?.splice(index, 1);
    }
};
const toggleSafetyGuardMultiRemove = (): void => {
    safetyGuardFunction.value = removeItems;
    showSafetyGuard.value = true;
};
const removeItems = async (): Promise<void> => {
    const ids = selectedItems.value?.map(item => item.id) ?? []
    await deleteDockerImages(ids);
    selectedItems.value = [];
};
/**
 * Handles an upload event containing docker image file and uploads this together with other attributes to backend
 * @param event Event containing docker image file in files attributes
 */
const upload = async (event: FileUploadUploaderEvent): Promise<void> => {
    const files: File[] = event.files as File[];
    await createDockerImage(addItem.value, files[0]);
    addItem.value.name = '';
    selectedOption.value = selectOptions.value[0];
};


/**
 * A function to be triggered when (an) item(s) are selected, and changes the multiRemove Button's disabled status
 * accordingly.
 * @param selected A list of all the selected docker images.
 */
const onSelect = (selected: any[] | null): void => {
    selectedItems.value = selected;
};
</script>

<template>
    <AdminLayout>
        <Title>
            <div class="gap-3 mb-3">{{ t('admin.docker_images.title') }}</div>
        </Title>
        <Body class="w-full">
            <SelectButton
                class="mb-3 gap-3 w-3"
                v-model="selectedOption"
                :options="selectOptions"
                :option-label="(option: string) => t(option)"
            />
            <div v-if="selectedOption === selectOptions[0]">
                <LazyDataTable
                    :pagination="pagination"
                    :entities="dockerImages"
                    :get="getDockerImages"
                    :search="searchDockerImages"
                    :filter="filter"
                    :on-filter="onFilter"
                    ref="dataTable"
                    select
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
                        <Button class="w-1 mb-3 gap-3" :disabled="multiRemove" @click="toggleSafetyGuardMultiRemove">
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
                    ref="fileUpload"
                    custom-upload
                    @uploader="upload"
                    :file-limit="1"
                    :disabled="addItem.name.length === 0"
                >
                    <template #empty>
                        <strong>{{ t('primevue.emptyFileSelect') }}</strong>
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
