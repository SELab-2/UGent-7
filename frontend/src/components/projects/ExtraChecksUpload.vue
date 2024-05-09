<script setup lang="ts">
import { PrimeIcons } from 'primevue/api';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import InputNumber from 'primevue/inputnumber';
import InputText from 'primevue/inputtext';
import FileUpload from 'primevue/fileupload';
import InputSwitch from 'primevue/inputswitch';
import { useI18n } from 'vue-i18n';
import { type Course } from '@/types/Course.ts';
import { ref, reactive, computed } from 'vue';
import { required, helpers } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';

/* Composable injections */
const { t } = useI18n();

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
function onDockerImageUpload(event: any): void {
    form.dockerImage = event.files[0];
}
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
                                    title="hellaur"
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
                        <div class="grid">
                            <!-- Docker image -->
                            <div class="field col">
                                <label for="dockerImage">
                                    {{ t('views.projects.extraChecks.dockerImage') }}
                                </label>
                                <FileUpload
                                    input="dockerImage"
                                    mode="basic"
                                    :multiple="false"
                                    title="hellaur"
                                    @select="onDockerImageUpload"
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