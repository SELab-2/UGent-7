<script setup lang="ts">
import { PrimeIcons } from 'primevue/api';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import InputNumber from 'primevue/inputnumber';
import InputText from 'primevue/inputtext';
import FileUpload from 'primevue/fileupload';
import InputSwitch from 'primevue/inputswitch';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import DataView from 'primevue/dataview';
import ErrorMessage from '@/components/forms/ErrorMessage.vue';
import { DockerImage } from '@/types/DockerImage';
import { ExtraCheck } from '@/types/ExtraCheck';
import { useI18n } from 'vue-i18n';
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { required, helpers } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { useDockerImages } from '@/composables/services/docker.service.ts';
import { useExtraCheck } from '@/composables/services/extra_checks.service';

/* Composable injections */
const { t } = useI18n();
const { dockerImages, getDockerImages, createDockerImage } = useDockerImages();
const { extraChecks, getExtraChecksByProject, addExtraCheck, deleteExtraCheck } = useExtraCheck();

/* Props */
const props = defineProps<{ projectId: string; createChecksBackend: boolean }>();

/* State for the dialog to create an extra check */
const displayExtraCheckCreation = ref(false);

/* List with all the extra checks */
const extraChecksList = ref<ExtraCheck[]>([]);

/* List with the extra checks that are already in the backend */
const extraChecksInBackendList = ref<ExtraCheck[]>([]);

/* Form content */
const form = reactive({
    name: '',
    dockerImage: null,
    bashFile: null,
    timeLimit: 30,
    memoryLimit: 128,
    showLog: true,
});

// Define validation rules for each form field
const rules = computed(() => {
    return {
        name: { required: helpers.withMessage(t('validations.required'), required) },
        dockerImage: { required: helpers.withMessage(t('validations.required'), required) },
        bashFile: { required: helpers.withMessage(t('validations.required'), required) },
        timeLimit: { required: helpers.withMessage(t('validations.required'), required) },
        memoryLimit: { required: helpers.withMessage(t('validations.required'), required) },
    };
});

// useVuelidate function to perform form validation
const v$ = useVuelidate(rules, form);

/**
 * Function to save the extra check
 */
async function saveExtraCheck(): Promise<void> {
    // Validate the form
    const validated = await v$.value.$validate();

    // Save the extra checks component
    if (validated) {
        // Create the extra check
        const extraCheck = new ExtraCheck(
            '', // The ID is not needed
            form.name,
            form.dockerImage,
            form.bashFile,
            form.timeLimit,
            form.memoryLimit,
            form.showLog,
        );

        // Add the extra check to the list with checks
        extraChecksList.value.push(extraCheck);

        // Close the dialog
        displayExtraCheckCreation.value = false;

        // Reset the form
        form.name = '';
        form.dockerImage = null;
        form.bashFile = null;
        form.timeLimit = 30;
        form.memoryLimit = 128;
        form.showLog = true;

        // Reset the validation
        v$.value.$reset();
    }
}

/**
 * Function to upload the bash script
 */
function onBashScriptUpload(event: any): void {
    form.bashFile = event.files[0];
}

/**
 * Function to upload the docker image
 */
async function onDockerImageUpload(event: any): Promise<void> {
    // Create a new docker image
    const dockerImage = new DockerImage(
        '', // The ID is not needed
        event.files[0].name as string,
        '', // File string is not needed
        false, // Docker image should be private, no possibility to upload public images
        '', // Owner is not needed
    );

    // Create the docker image in the backend
    await createDockerImage(dockerImage, event.files[0] as File);

    // Refresh the list of docker images
    await getDockerImages();
}

/**
 * Watcher to create the checks in the backend when the signal is received
 */
watch(
    () => props.createChecksBackend,
    async (value) => {
        if (value) {
            // Create the extra checks in the backend. If a check has already an id, this means that the check is already in the backend.
            // If this is the case, the check should not be created again.
            extraChecksList.value.forEach((extraCheck) => {
                // Create the extra check in the backend, if the check has no id yet
                if (extraCheck.id === '') {
                    addExtraCheck(extraCheck, props.projectId);
                }
            });

            // Delete all the extra checks that are in the backend list, but not in the extra checks list.
            // This means that the user has removed the extra check from the list and it should be deleted from the backend.
            extraChecksInBackendList.value.forEach((extraCheck) => {
                if (!extraChecksList.value.includes(extraCheck)) {
                    // Delete the extra check from the backend
                    deleteExtraCheck(extraCheck.id);
                }
            });
        }
    },
);

/**
 * Load the docker images and extra checks when the component is mounted
 */
onMounted(async () => {
    await getDockerImages();

    // If a project ID is provided, load the extra checks for this project
    if (props.projectId !== '') {
        // Load the extra checks for the project
        await getExtraChecksByProject(props.projectId);

        // Save the extra checks in the list
        extraChecksList.value = extraChecks.value ?? [];

        // Save the checks that are already in the backend in a separate list (to avoid duplicated / enable deletion)
        extraChecksInBackendList.value = extraChecks.value?.slice() ?? [];
    }
});
</script>

<template>
    <!-- List with the extra checks -->
    <DataView :value="extraChecksList" data-key="id" v-if="extraChecksList.length > 0">
        <template #list="slotProps">
            <div
                v-for="(item, index) in slotProps.items"
                :key="index"
            >
                <div class="flex align-items-center justify-content-between">
                    <p style="max-width: 300px">{{ item.name }}</p>
                    <Button icon="pi pi-times" class="p-button-danger p-button-sm" @click="extraChecksList.splice(index, 1)" />
                </div>
            </div>
        </template>
    </DataView>

    <!-- Button to add a new extra check -->
    <Button
        class="p-button-primary"
        @click="displayExtraCheckCreation = true"
        :icon="PrimeIcons.PLUS"
        :label="t('views.projects.extraChecks.add')"
        icon-pos="left"
    />
    <!-- Dialog with a form to create a new extra check -->
    <Dialog
        v-model:visible="displayExtraCheckCreation"
        class="m-3"
        :draggable="false"
        :contentStyle="{ 'min-width': '50vw', 'max-width': '1080px' }"
        modal
    >
        <template #header>
            <h2 class="my-3 text-primary">
                {{ t('views.projects.extraChecks.add') }}
            </h2>
        </template>
        <template #default>
            <!-- Extra checks form -->
            <form @submit.prevent="saveExtraCheck">
                <div class="grid">
                    <div class="col-12 lg:col-6">
                        <div class="grid formgrid">
                            <!-- Extra check name -->
                            <div class="field col-12">
                                <label for="name">
                                    {{ t('views.projects.extraChecks.name') }}
                                </label>
                                <InputText id="projectName" class="w-full" v-model="form.name" />
                                <ErrorMessage :field="v$.name" />
                            </div>
                        </div>

                        <div class="grid">
                            <!-- Bash script -->
                            <div class="field col">
                                <label for="bashScript">
                                    {{ t('views.projects.extraChecks.bashScript') }}
                                </label>
                                <FileUpload
                                    input="bashScript"
                                    mode="basic"
                                    accept=".sh"
                                    :multiple="false"
                                    @select="onBashScriptUpload"
                                />
                                <ErrorMessage :field="v$.bashFile" />
                            </div>
                        </div>

                        <div class="grid align-items-end">
                            <!-- Time limit -->
                            <div class="field col">
                                <label for="timeLimit">
                                    {{ t('views.projects.extraChecks.timeLimit') }}
                                </label>
                                <InputNumber
                                    id="timeLimit"
                                    class="w-full"
                                    v-model="form.timeLimit"
                                    :min="10"
                                    :max="1000"
                                />
                                <ErrorMessage :field="v$.timeLimit" />
                            </div>

                            <div class="field col">
                                <label for="memoryLimit">
                                    {{ t('views.projects.extraChecks.memoryLimit') }}
                                </label>
                                <InputNumber
                                    id="numberOfGroups"
                                    class="w-full"
                                    v-model="form.memoryLimit"
                                    :min="50"
                                    :max="1024"
                                />
                                <ErrorMessage :field="v$.memoryLimit" />
                            </div>
                        </div>

                        <!-- Visibility of the log files for students -->
                        <div class="grid">
                            <div class="field-checkbox col-12">
                                <InputSwitch id="showLog" v-model="form.showLog" style="min-width: 50px;"/>
                                <label for="showLog">{{ t('views.projects.extraChecks.showLog') }}</label>
                            </div>
                        </div>
                    </div>

                    <div class="col-12 lg:col-6">
                        <!-- List to select/add the docker image -->
                        <div class="grid formgrid">
                            <div class="col">
                                <label for="dockerImage">
                                    {{ t('views.projects.extraChecks.dockerImage') }}
                                </label>
                                <!-- Data table with the docker images -->
                                <DataTable
                                    v-model:selection="form.dockerImage"
                                    :value="dockerImages"
                                    selectionMode="single"
                                    dataKey="id"
                                    tableStyle="min-width: 30rem"
                                    id="dockerImage"
                                    class="w-full mt-2 mb-2"
                                    scrollable
                                    scrollHeight="300px"
                                >
                                    <Column field="name" :header="t('views.projects.extraChecks.name')"></Column>
                                    <Column field="public" :header="t('views.projects.extraChecks.public')">
                                        <template #body="slotProps">
                                            <!-- Use check and cross icons to indicate if the image is public or not -->
                                            <i v-if="slotProps.data.public" class="pi pi-check" />
                                            <i v-else class="pi pi-times" />
                                        </template>
                                    </Column>
                                </DataTable>
                                <ErrorMessage :field="v$.dockerImage" />

                                <!-- Button to add a private docker image for this project -->
                                <FileUpload
                                    mode="basic"
                                    :multiple="false"
                                    :auto="true"
                                    @select="onDockerImageUpload"
                                    :chooseLabel="t('views.projects.extraChecks.dockerImage')"
                                />
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Submit button -->
                <div class="grid align-items-end justify-content-end mr-3">
                    <Button
                        :label="t('views.projects.extraChecks.add')"
                        type="submit"
                        icon="pi pi-plus"
                        iconPos="left"
                        rounded
                    />
                </div>
            </form>
        </template>
    </Dialog>
</template>

<style scoped lang="scss"></style>
