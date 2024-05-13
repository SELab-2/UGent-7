<script setup lang="ts">
import Calendar from 'primevue/calendar';
import BaseLayout from '@/components/layout/base/BaseLayout.vue';
import FileUpload from 'primevue/fileupload';
import Title from '@/components/layout/Title.vue';
import ErrorMessage from '@/components/forms/ErrorMessage.vue';
import InputText from 'primevue/inputtext';
import Editor from '@/components/forms/Editor.vue';
import Button from 'primevue/button';
import InputNumber from 'primevue/inputnumber';
import InputSwitch from 'primevue/inputswitch';
import ExtraChecksUpload from '@/components/projects/ExtraChecksUpload.vue';
import { SubmissionStatus } from '@/types/SubmisionStatus';
import { reactive, computed, onMounted, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { Project } from '@/types/Project';
import { useProject } from '@/composables/services/project.service';
import { required, helpers } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { useCourses } from '@/composables/services/course.service';

/* Composable injections */
const { t } = useI18n();
const { push } = useRouter();
const { params } = useRoute();

/* Service injection */
const { course, getCourseByID } = useCourses();
const { project, getProjectByID, updateProject } = useProject();

/* State */
const createExtraChecksBackend = ref<boolean>(false);

/* Load project data */
onMounted(async () => {
    await getProjectByID(params.projectId as string);

    /* Set the form values */
    if (project.value !== null) {
        form.name = project.value.name;
        form.description = project.value.description ?? '';
        form.startDate = project.value.start_date;
        form.deadline = project.value.deadline;
        form.groupSize = project.value.group_size;
        form.maxScore = project.value.max_score;
        form.visibility = project.value.visible;
        form.scoreVisibility = project.value.score_visible;
    }
});

/* Form content */
const form = reactive({
    name: '',
    description: '',
    startDate: new Date(),
    deadline: new Date(),
    groupSize: 1,
    maxScore: 10,
    visibility: true,
    scoreVisibility: false,
    submissionStructure: null,
});

// Define validation rules for each form field
const rules = computed(() => {
    return {
        name: { required: helpers.withMessage(t('validations.required'), required) },
        startDate: { required: helpers.withMessage(t('validations.required'), required) },
        deadline: {
            required: helpers.withMessage(t('validations.required'), required),
            minDate: helpers.withMessage(t('validations.deadline'), (value: Date) => value > form.startDate),
        },
        groupSize: { required: helpers.withMessage(t('validations.required'), required) },
        maxScore: { required: helpers.withMessage(t('validations.required'), required) },
    };
});

// Function to handle the file upload of a zip file containing the submission structure
const onZipStructureUpload = (event: any): void => {
    form.submissionStructure = event.files[0];
};

// useVuelidate function to perform form validation
const v$ = useVuelidate(rules, form);

// Validate the create project form
const validateForm = (): boolean => {
    v$.value.name.$touch();
    v$.value.startDate.$touch();
    v$.value.deadline.$touch();
    v$.value.groupSize.$touch();
    v$.value.maxScore.$touch();
    return (
        !v$.value.name.$invalid &&
        !v$.value.startDate.$invalid &&
        !v$.value.deadline.$invalid &&
        !v$.value.groupSize.$invalid &&
        !v$.value.maxScore.$invalid
    );
};

/**
 * Function to submit the project form.
 */
async function submitProject(): Promise<void> {
    // Validate the form
    const validated = validateForm();

    // Get the course object from the course ID
    await getCourseByID(params.courseId as string);

    // Only submit the form if the validation was successful
    if (validated && course.value !== null) {
        // Pass the project data to the service
        await updateProject(
            new Project(
                params.projectId as string,
                form.name,
                form.description,
                form.visibility,
                false, // Default not archived
                false, // Default the groups are not locked
                form.startDate,
                form.deadline,
                form.maxScore,
                form.scoreVisibility,
                form.groupSize,
                course.value,
                new SubmissionStatus(0, 0, 0), // Default submission status
                form.submissionStructure,
            ),
        );

        // Make sure the extra checks are updated in the backend
        createExtraChecksBackend.value = true;

        // Redirect to the project overview
        await push({
            name: 'course-project',
            params: { courseId: params.courseId as string, projectId: params.projectId as string },
        });
    }
}
</script>

<template>
    <BaseLayout>
        <!-- Update project heading -->
        <Title class="mb-6">
            {{ t('views.projects.edit') }}
        </Title>

        <!-- Project form -->
        <form @submit.prevent="submitProject" v-if="project">
            <div class="grid">
                <div class="col-12 lg:col-6">
                    <div class="grid formgrid">
                        <!-- Project name -->
                        <div class="field col-12">
                            <label for="projectName">
                                {{ t('views.projects.name') }}
                            </label>
                            <InputText id="projectName" class="w-full" v-model="form.name" />
                            <ErrorMessage :field="v$.name" />
                        </div>
                    </div>

                    <div class="grid">
                        <!-- Project description -->
                        <div class="field col">
                            <label for="projectDescription">
                                {{ t('views.projects.description') }}
                            </label>
                            <Editor id="projectDescription" class="w-full" v-model="form.description" />
                        </div>
                    </div>

                    <div class="grid">
                        <!-- Start date of the project -->
                        <div class="field col">
                            <label for="projectStartDate">{{ t('views.projects.start_date') }}</label>
                            <Calendar
                                id="projectStartDate"
                                class="w-full"
                                v-model="form.startDate"
                                dateFormat="dd-mm-yy"
                                :min-date="new Date()"
                                showIcon
                            />
                            <ErrorMessage :field="v$.startDate" />
                        </div>

                        <!-- Deadline of the project -->
                        <div class="field col">
                            <label for="projectDeadline">{{ t('views.projects.deadline') }}</label>
                            <Calendar
                                id="projectDeadline"
                                class="w-full"
                                v-model="form.deadline"
                                dateFormat="dd-mm-yy"
                                :min-date="form.startDate"
                                showTime
                                hourFormat="24"
                                showIcon
                            />
                            <ErrorMessage :field="v$.deadline" />
                        </div>
                    </div>

                    <div class="grid align-items-end">
                        <!-- Group size for the project -->
                        <div class="field col">
                            <label for="groupSize">
                                {{ t('views.projects.group_size') }}
                            </label>
                            <InputNumber id="groupSize" class="w-full" v-model="form.groupSize" :min="1" />
                            <ErrorMessage :field="v$.groupSize" />
                        </div>

                        <!-- Max score for the project -->
                        <div class="field col">
                            <label for="maxScore">{{ t('views.projects.max_score') }}</label>
                            <InputNumber id="maxScore" class="w-full" v-model="form.maxScore" :min="1" />
                            <ErrorMessage :field="v$.maxScore" />
                        </div>
                    </div>

                    <!-- Visibility of the project -->
                    <div class="grid">
                        <div class="flex align-items-center field-checkbox col-12">
                            <InputSwitch id="visibility" v-model="form.visibility" />
                            <label for="visibility">{{ t('views.projects.visibility') }}</label>
                        </div>
                    </div>

                    <!-- Score visibility of the project -->
                    <div class="grid">
                        <div class="flex align-items-center field-checkbox col-12">
                            <InputSwitch id="scoreVisibility" v-model="form.scoreVisibility" />
                            <label for="scoreVisibility">{{ t('views.projects.scoreVisibility') }}</label>
                        </div>
                    </div>

                    <!-- Submit button -->
                    <Button
                        :label="t('views.projects.edit')"
                        type="submit"
                        icon="pi pi-check"
                        iconPos="right"
                        rounded
                    />
                </div>

                <div class="col-12 lg:col-6 checks">
                    <!-- Extra checks upload -->
                    <div class="field col-8">
                        <label for="extraChecks">{{ t('views.projects.extraChecks.title') }}</label>
                        <ExtraChecksUpload
                            id="extraChecks"
                            :create-checks-backend="createExtraChecksBackend"
                            :project-id="project.id"
                        />
                    </div>

                    <!-- Upload field for a zip file that contains the submission structure -->
                    <div class="field col">
                        <label for="submissionStructure">
                            {{ t('views.projects.submissionStructure') }}
                        </label>
                        <FileUpload
                            id="submissionStructure"
                            mode="basic"
                            accept=".zip"
                            :multiple="false"
                            @select="onZipStructureUpload"
                        />
                    </div>
                </div>
            </div>
        </form>
    </BaseLayout>
</template>

<style scoped>
.checks .field.col > * {
    display: block;
}
</style>
@/types/Project
