<script setup lang="ts">
import InputNumber from 'primevue/inputnumber';
import InputText from 'primevue/inputtext';
import ErrorMessage from '@/components/forms/ErrorMessage.vue';
import Button from 'primevue/button';
import Editor from '@/components/forms/Editor.vue';
import Calendar from 'primevue/calendar';
import Skeleton from 'primevue/skeleton';
import InputSwitch from 'primevue/inputswitch';
import { Project } from '@/types/Project.ts';
import { useI18n } from 'vue-i18n';
import { computed, ref, watchEffect } from 'vue';
import { helpers, required } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { type Course } from '@/types/Course.ts';
import ProjectStructureTree from '@/components/projects/ProjectStructureTree.vue';
import { type DockerImage } from '@/types/DockerImage.ts';
import ExtraChecksUpload from '@/components/projects/ExtraChecksUpload.vue';

/* Props */
const props = defineProps<{
    course: Course;
    dockerImages: DockerImage[];
    project?: Project | undefined;
}>();

/* Emits */
const emit = defineEmits(['update:project', 'create:docker-image']);

/* Composable injections */
const { t } = useI18n();

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

const v$ = useVuelidate(rules, form, {
    $scope: 'form',
});

/**
 * Save the project form to the API backend.
 */
async function saveProject(): Promise<void> {
    // Validate the form.
    const validated = await v$.value.$validate();

    // Only submit the form if the validation was successful
    if (validated) {
        emit('update:project', form.value, numberOfGroups.value);
    }
}

/**
 * Save the docker image by emitting its new value.
 *
 * @param image
 * @param file
 */
function saveDockerImage(image: DockerImage, file: File): void {
    emit('create:docker-image', image, file);
}

/**
 * Watch for changes in the project prop and update the form values.
 */
watchEffect(() => {
    /* Set the form values with the existing project */
    const project = props.project;

    if (project !== undefined) {
        form.value = Project.fromJSON(project);
        form.value.structure_checks = [...(project.structure_checks ?? [])];
        form.value.extra_checks = [...(project.extra_checks ?? [])];
    } else {
        form.value.structure_checks = [];
        form.value.extra_checks = [];
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
                        <label for="projectStartDate">{{ t('views.projects.startDate') }}</label>
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
                            {{ t('views.projects.groupSize') }}
                        </label>
                        <InputNumber input-id="groupSize" class="w-full" v-model="form.group_size" :min="1" />
                        <ErrorMessage :field="v$.group_size" />
                    </div>

                    <!-- Max score for the project -->
                    <div class="field col">
                        <label for="maxScore">{{ t('views.projects.maxScore') }}</label>
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
            </div>

            <div class="col-12 lg:col-6">
                <!-- Define the submission structure checks -->
                <template v-if="form.structure_checks !== null">
                    <div class="grid">
                        <div class="field col">
                            <label for="structure">{{ t('views.projects.structureChecks') }}</label>
                            <ProjectStructureTree id="structure" v-model="form.structure_checks" />
                        </div>
                    </div>
                </template>
                <template v-else>
                    <Skeleton height="10rem" />
                </template>

                <!-- Upload field for docker script -->
                <template v-if="form.extra_checks !== null">
                    <div class="grid">
                        <div class="field col">
                            <label for="dockerScript" class="block">
                                {{ t('views.projects.extraChecks.title') }}
                            </label>
                            <ExtraChecksUpload
                                v-model="form.extra_checks"
                                :docker-images="dockerImages"
                                @create:docker-image="saveDockerImage"
                            />
                        </div>
                    </div>
                </template>
                <template v-else>
                    <Skeleton height="10rem" />
                </template>
            </div>
        </div>

        <!-- Submit button -->
        <Button :label="t('views.projects.edit')" type="submit" icon="pi pi-check" iconPos="right" rounded />
    </form>
</template>

<style scoped lang="scss"></style>
