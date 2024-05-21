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
import ErrorMessage from '@/components/forms/ErrorMessage.vue';
import { DockerImage } from '@/types/DockerImage';
import { ExtraCheck } from '@/types/ExtraCheck';
import { useI18n } from 'vue-i18n';
import { ref, reactive, computed } from 'vue';
import { required, helpers } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';

/* Composable injections */
const { t } = useI18n();

/* Props */
defineProps<{ dockerImages: DockerImage[] }>();
const extraChecks = defineModel<ExtraCheck[]>();

/* Emits */
const emit = defineEmits(['create:docker-image']);

/* State for the dialog to create an extra check */
const displayExtraCheckCreation = ref(false);

/* Form content */
let form = reactive(new ExtraCheck());

// Define validation rules for each form field
const rules = computed(() => {
    return {
        name: { required: helpers.withMessage(t('validations.required'), required) },
        docker_image: { required: helpers.withMessage(t('validations.required'), required) },
        file: { required: helpers.withMessage(t('validations.required'), required) },
        time_limit: { required: helpers.withMessage(t('validations.required'), required) },
        memory_limit: { required: helpers.withMessage(t('validations.required'), required) },
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
    if (validated && extraChecks.value !== undefined) {
        // Add the extra check to the list with checks
        extraChecks.value.push(form);

        // Close the dialog
        displayExtraCheckCreation.value = false;

        // Reset the form
        form = new ExtraCheck();

        // Reset the validation
        v$.value.$reset();
    }
}

/**
 * Function to upload the bash script.
 * @param event
 */
function onBashScriptUpload(event: any): void {
    form.file = event.files[0];
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

    emit('create:docker-image', dockerImage, event.files[0]);
}
</script>

<template>
    <!-- List with the extra checks -->
    <div class="flex flex-column gap-3 border-round border-1 border-400 p-3">
        <template v-if="extraChecks && extraChecks.length > 0">
            <div
                class="flex align-items-center justify-content-between gap-2"
                v-for="(item, index) in extraChecks"
                :key="index"
            >
                <span>{{ item.name }}</span>
                <Button
                    icon="pi pi-times"
                    class="p-button-danger p-button-sm"
                    @click="extraChecks.splice(index, 1)"
                    outlined
                    rounded
                />
            </div>
        </template>
        <template v-else>
            <span>{{ t('views.projects.extraChecks.empty') }}</span>
        </template>
    </div>

    <!-- Button to add a new extra check -->
    <Button
        class="mt-3"
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
                                <ErrorMessage :field="v$.file" />
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
                                    v-model="form.time_limit"
                                    :min="10"
                                    :max="1000"
                                />
                                <ErrorMessage :field="v$.time_limit" />
                            </div>

                            <div class="field col">
                                <label for="memoryLimit">
                                    {{ t('views.projects.extraChecks.memoryLimit') }}
                                </label>
                                <InputNumber
                                    id="numberOfGroups"
                                    class="w-full"
                                    v-model="form.memory_limit"
                                    :min="50"
                                    :max="1024"
                                />
                                <ErrorMessage :field="v$.memory_limit" />
                            </div>
                        </div>

                        <!-- Visibility of the log files for students -->
                        <div class="grid">
                            <div class="field-checkbox col-12">
                                <InputSwitch id="showLog" v-model="form.show_log" style="min-width: 50px" />
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
                                    v-model:selection="form.docker_image"
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
                                <ErrorMessage :field="v$.docker_image" />

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
