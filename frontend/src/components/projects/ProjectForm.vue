<script setup lang="ts">
import InputNumber from 'primevue/inputnumber';
import InputText from 'primevue/inputtext';
import FileUpload from 'primevue/fileupload';
import ErrorMessage from '@/components/forms/ErrorMessage.vue';
import Button from 'primevue/button';
import Editor from '@/components/forms/Editor.vue';
import Calendar from 'primevue/calendar';
import InputSwitch from 'primevue/inputswitch';
import { Project } from '@/types/Project.ts';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';
import { useProject } from '@/composables/services/project.service.ts';
import { computed, onMounted, ref } from 'vue';
import { helpers, required } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { type Course } from '@/types/Course.ts';
import ProjectStructureTree from '@/components/projects/ProjectStructureTree.vue';

/* Props */
const props = defineProps<{
    course: Course;
    project?: Project | undefined;
}>();

/* Composable injections */
const { t } = useI18n();
const { push } = useRouter();
const { createProject, updateProject } = useProject();

/* State */
const form = ref(new Project());
const numberOfGroups = ref(0);

const rules = computed(() => {
    return {
        name: { required: helpers.withMessage(t('validations.required'), required) },
        start_date: { required: helpers.withMessage(t('validations.required'), required) },
        deadline: {
            required: helpers.withMessage(t('validations.required'), required),
            minDate: helpers.withMessage(t('validations.deadline'), (value: Date) => value > form.value.start_date),
        },
        group_size: { required: helpers.withMessage(t('validations.required'), required) },
    };
});

const v$ = useVuelidate(rules, form);

/**
 * Save the project form to the API backend.
 */
async function saveProject(): Promise<void> {
    // Validate the form.
    const result = await v$.value.$validate();

    // Only submit the form if the validation was successful
    if (result) {
        // Update the course if it has been provided before.
        if (props.project !== undefined) {
            await updateProject(form.value);
            await push({ name: 'course-project', params: { courseId: props.course.id, projectId: props.project.id } });
        }

        // Create a course in the other case.
        if (props.project === undefined) {
            await createProject(form.value, props.course.id, numberOfGroups.value);
            await push({ name: 'course', params: { courseId: props.course.id } });
        }
    }
}

onMounted(async () => {
    /* Set the form values with the existing project */
    if (props.project !== undefined) {
        // Convenient way of copying the project fields.
        form.value = Project.fromJSON(props.project);
    }
});
</script>

<template>
    <form @submit.prevent="saveProject">
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
                            v-model="form.start_date"
                            dateFormat="dd-mm-yy"
                            :min-date="new Date()"
                            showIcon
                        />
                        <ErrorMessage :field="v$.start_date" />
                    </div>

                    <!-- Deadline of the project -->
                    <div class="field col">
                        <label for="projectDeadline">{{ t('views.projects.deadline') }}</label>
                        <Calendar
                            id="projectDeadline"
                            class="w-full"
                            v-model="form.deadline"
                            dateFormat="dd-mm-yy"
                            :min-date="form.deadline"
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
                        <InputNumber input-id="groupSize" class="w-full" v-model="form.group_size" :min="1" />
                        <ErrorMessage :field="v$.group_size" />
                    </div>

                    <!-- Max score for the project -->
                    <div class="field col">
                        <label for="maxScore">{{ t('views.projects.max_score') }}</label>
                        <InputNumber
                            input-id="maxScore"
                            class="w-full"
                            v-model="form.max_score"
                            :min="1"
                            :max="100"
                            show-buttons
                        />
                    </div>
                </div>

                <!-- Visibility of the project -->
                <div class="grid">
                    <div class="flex align-items-center field-checkbox col-12">
                        <InputSwitch id="visibility" v-model="form.visible" />
                        <label for="visibility">{{ t('views.projects.visibility') }}</label>
                    </div>
                </div>

                <!-- Score visibility of the project -->
                <div class="grid">
                    <div class="flex align-items-center field-checkbox col-12">
                        <InputSwitch id="scoreVisibility" v-model="form.score_visible" />
                        <label for="scoreVisibility">{{ t('views.projects.scoreVisibility') }}</label>
                    </div>
                </div>

                <!-- Submit button -->
                <Button :label="t('views.projects.edit')" type="submit" icon="pi pi-check" iconPos="right" rounded />
            </div>

            <div class="col-12 lg:col-6">
                <!-- Define the submission structure checks -->
                <div class="grid">
                    <div class="field col">
                        <label for="structure">{{ t('views.projects.structureChecks') }}</label>
                        <ProjectStructureTree id="structure" v-model="form.structureChecks" />
                    </div>
                </div>

                <!-- Upload field for docker script -->
                <div class="field col">
                    <label for="dockerScript">
                        {{ t('views.projects.dockerUpload') }}
                    </label>
                    <FileUpload input="dockerScript" mode="basic" accept=".sh" :multiple="false" />
                </div>
            </div>
        </div>
    </form>
</template>

<style scoped lang="scss"></style>
