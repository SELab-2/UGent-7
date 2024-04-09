<script setup lang="ts">
import Dropdown from 'primevue/dropdown';
import BaseLayout from '@/components/layout/BaseLayout.vue';
import Title from '@/components/layout/Title.vue';
import { reactive, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';
import Button from 'primevue/button';
import { Course } from '@/types/Course';
import { useCourses } from '@/composables/services/courses.service';
import { useFaculty } from '@/composables/services/faculties.service.ts';
import { required, helpers } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import ErrorMessage from '@/components/forms/ErrorMessage.vue';

/* Composable injections */
const { t } = useI18n();
const { push } = useRouter();
const { faculties, getFaculties } = useFaculty();

/* Service injection */
const { createCourse } = useCourses();

/* Fetch the faculties */
onMounted(async () => {
    await getFaculties();
});

/* Form content */
const form = reactive({
    name: '',
    description: '',
    faculty: null,
});

// Define validation rules for each form field
const rules = computed(() => {
    return {
        name: { required: helpers.withMessage(t('validations.required'), required) },
        faculty: { required: helpers.withMessage(t('validations.required'), required) },
    };
});

// useVuelidate function to perform form validation
const v$ = useVuelidate(rules, form);

const submitCourse = async (): Promise<void> => {
    // Validate the form
    const result = await v$.value.$validate();

    // Only submit the form if the validation was successful
    if (result) {
        // Pass the course data to the service
        await createCourse(
            new Course(
                '',
                form.name,
                form.description,
                currentAcademicYear(),
                null, // No parent course
                form.faculty,
            ),
        );

        // Redirect to the dashboard overview
        push({ name: 'dashboard' });
    }
};

/* Get the current academic year */
const currentAcademicYear = (): number => {
    if (new Date().getMonth() < 9) {
        return new Date().getFullYear() - 1;
    } else {
        return new Date().getFullYear();
    }
};
</script>

<template>
    <BaseLayout>
        <div class="grid fadein">
            <div class="col-12 md:col-6">
                <!-- Create course heading -->
                <Title class="mb-6">{{ t('views.courses.create') }}</Title>

                <!-- Course form -->
                <form @submit.prevent="submitCourse">
                    <!-- Course name -->
                    <div class="mb-4">
                        <label for="courseName">{{ t('views.courses.name') }}</label>
                        <InputText id="courseName" v-model="form.name" />
                        <ErrorMessage :field="v$.name" />
                    </div>

                    <!-- Course description -->
                    <div class="mb-4">
                        <label for="courseDescription">{{ t('views.courses.description') }}</label>
                        <Textarea id="courseDescription" v-model="form.description" autoResize rows="5" cols="30" />
                    </div>

                    <!-- Course faculty -->
                    <div class="mb-4">
                        <label for="courseFaculty">{{ t('views.courses.faculty') }}</label>
                        <Dropdown
                            id="courseFaculty"
                            v-model="form.faculty"
                            :options="faculties"
                            optionLabel="name"
                            v-if="faculties"
                        />
                        <ErrorMessage :field="v$.faculty" />
                    </div>

                    <!-- Submit button -->
                    <div class="flex justify-end">
                        <Button
                            :label="t('views.courses.create')"
                            type="submit"
                            icon="pi pi-check"
                            iconPos="right"
                            rounded
                        />
                    </div>
                </form>
            </div>
        </div>
    </BaseLayout>
</template>

<style scoped>
/* Flex column layout for label and input */
.mb-4 {
    display: flex;
    flex-direction: column;
}

/* Add margin between label and input */
label {
    margin-bottom: 0.5rem;
}
</style>
