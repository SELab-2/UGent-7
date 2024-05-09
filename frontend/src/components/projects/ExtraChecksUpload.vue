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
import { useI18n } from 'vue-i18n';
import { ref, reactive, computed, onMounted } from 'vue';
import { required, helpers } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { useDockerImages } from '@/composables/services/docker.service.ts';

/* Composable injections */
const { t } = useI18n();
const { dockerImages, getDockerImages, createDockerImage } = useDockerImages();

/* Props */
// const props = defineProps<{ course: Course }>();

/* State for the dialog to create an extra check */
const displayExtraCheckCreation = ref(false);

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
    // // Validate the form
    // const validated = await v$.value.$validate();

    // // Get the course object from the course ID
    // await getCourseByID(params.courseId as string);

    // // Only submit the form if the validation was successful
    // if (validated && course.value !== null) {

    // }
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
        '',    // The ID is not needed
        event.files[0].name,
        '',    // File string is not needed
        false, // Docker image should be private, no possibility to upload public images
        '',    // No owner is needed
    );

    // Create the docker image in the backend
    await createDockerImage(dockerImage, event.files[0]);

    // Refresh the list of docker images
    await getDockerImages();
}

/**
 * Load the docker images when the component is mounted
 */
onMounted(async () => {
    await getDockerImages();
});
</script>

<template>
    <Button
        class="p-button-primary"
        @click="displayExtraCheckCreation = true"
        :icon="PrimeIcons.PLUS"
        :label="t('views.projects.extraChecks.add')"
        icon-pos="left"
    />
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
                            </div>
                        </div>

                        <div class="grid align-items-end">
                            <!-- Time limit -->
                            <div class="field col">
                                <label for="timeLimit">
                                    {{ t('views.projects.extraChecks.timeLimit') }}
                                </label>
                                <InputNumber id="timeLimit" class="w-full" v-model="form.timeLimit" :min="10" :max="1000" />
                                <ErrorMessage :field="v$.timeLimit" />
                            </div>

                            <div class="field col">
                                <label for="memoryLimit">
                                    {{ t('views.projects.extraChecks.memoryLimit') }}
                                </label>
                                <InputNumber id="numberOfGroups" class="w-full" v-model="form.memoryLimit" :min="50" :max="1024" />
                                <ErrorMessage :field="v$.memoryLimit" />
                            </div>
                        </div>

                        <!-- Visibility of the log files for students -->
                        <div class="grid">
                            <div class="flex align-items-center field-checkbox col-12">
                                <InputSwitch id="showLog" v-model="form.showLog" />
                                <label for="showLog">{{ t('views.projects.extraChecks.showLog') }}</label>
                            </div>
                        </div>

                    </div>

                    <div class="col-12 lg:col-6">
                        <!-- List to select/add the docker image -->
                        <div class="grid formgrid">
                            <label for="dockerImage">
                                {{ t('views.projects.extraChecks.dockerImage') }}
                            </label>
                            <DataTable v-model:selection="form.dockerImage" :value="dockerImages" selectionMode="single" dataKey="id" tableStyle="min-width: 30rem" id="dockerImage" class="w-full mt-2 mb-2" scrollable scrollHeight="300px">
                                <Column field="name" header="Name"></Column>
                                <Column field="public" header="Public">
                                    <template #body="slotProps">
                                        <!-- Use check and cross icons to indicate if the image is public or not -->
                                        <i v-if="slotProps.data.public" class="pi pi-check"/>
                                        <i v-else class="pi pi-times"/>
                                    </template>
                                </Column>                            
                            </DataTable>

                            <!-- Button to add a private docker image for this project -->
                            <FileUpload
                                mode="basic"
                                :multiple="false"
                                :auto="true"
                                @select="onDockerImageUpload"
                            />
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