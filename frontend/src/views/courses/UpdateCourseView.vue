<script setup lang="ts">
import BaseLayout from '@/components/layout/base/BaseLayout.vue';
import Title from '@/components/layout/Title.vue';
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';
import Editor from '@/components/forms/Editor.vue';
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';
import InputSwitch from 'primevue/inputswitch';
import { reactive, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useCourses } from '@/composables/services/course.service';
import { useFaculty } from '@/composables/services/faculty.service.ts';
import { Faculty } from '@/types/Faculty';
import { required, helpers } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import ErrorMessage from '@/components/forms/ErrorMessage.vue';
import { Course } from '@/types/Course';

/* Composable injections */
const { params } = useRoute();
const { t } = useI18n();
const { push } = useRouter();
const { course, getCourseByID, updateCourse } = useCourses();
const { faculties, getFaculties } = useFaculty();

/* Load course data */
onMounted(async () => {
    await getFaculties();
    await getCourseByID(params.courseId as string);

    /* Set the form values */
    if (course.value !== null) {
        form.name = course.value.name;
        form.description = course.value.description ?? '';
        form.excerpt = course.value.excerpt ?? '';
        form.faculty = course.value.faculty ?? new Faculty('', '');
        form.private = course.value.private_course;
        form.year = `${course.value.academic_startyear} - ${course.value.academic_startyear + 1}`;
    }
});

/* Form content */
const form = reactive({
    name: '',
    description: '',
    excerpt: '',
    faculty: new Faculty('', ''), // Default value for the dropdown
    private: false,
    year: '',
});

// Define validation rules for each form field
const rules = computed(() => {
    return {
        name: { required: helpers.withMessage(t('validations.required'), required) },
        faculty: { required: helpers.withMessage(t('validations.required'), required) },
        excerpt: { required: helpers.withMessage(t('validations.required'), required) },
    };
});

// useVuelidate function to perform form validation
const v$ = useVuelidate(rules, form);

const submitCourse = async (): Promise<void> => {
    // Validate the form
    const result = await v$.value.$validate();

    // Only submit the form if the validation was successful
    if (result && course.value !== null) {
        // Pass the course data to the service
        await updateCourse(
            new Course(
                course.value.id,
                form.name,
                form.description,
                form.excerpt,
                course.value.academic_startyear,
                form.private,
                course.value.parent_course,
                form.faculty,
            ),
        );

        // Redirect to the course overview
        await push({ name: 'course', params: { courseId: params.courseId as string } });
    }
};
</script>

<template>
    <BaseLayout>
        <div class="grid fadein">
            <div class="col-12 md:col-6">
                <!-- Create course heading -->
                <Title class="mb-6">{{ t('views.courses.edit') }}</Title>

                <!-- Course form -->
                <form @submit.prevent="submitCourse">
                    <!-- Course name -->
                    <div class="mb-4">
                        <label for="courseName">{{ t('views.courses.name') }}</label>
                        <InputText id="courseName" v-model="form.name" />
                        <ErrorMessage :field="v$.name" />
                    </div>

                    <!-- Course excerpt -->
                    <div class="mb-4">
                        <label for="courseExcerpt">{{ t('views.courses.excerpt') }}</label>
                        <Textarea id="courseExcerpt" v-model="form.excerpt" autoResize rows="5" cols="30" />
                        <ErrorMessage :field="v$.excerpt" />
                    </div>

                    <!-- Course description -->
                    <div class="mb-4">
                        <label for="courseDescription">{{ t('views.courses.description') }}</label>
                        <Editor v-model="form.description" />
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

                    <!-- Course academic year, not editable -->
                    <div class="mb-4">
                        <label for="courseYear">{{ t('views.courses.year') }}</label>
                        <InputText id="courseYear" v-model="form.year" readonly class="readonly-input" />
                    </div>

                    <!-- Course visibility -->
                    <div class="grid">
                        <div class="flex align-items-center field-checkbox col-12">
                            <InputSwitch id="private" v-model="form.private" />
                            <label for="private">{{ t('views.courses.private') }}</label>
                        </div>
                    </div>

                    <!-- Submit button -->
                    <div class="flex justify-end">
                        <Button
                            :label="t('views.courses.edit')"
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

/* Style for read-only fields */
.readonly-input {
    background-color: #f0f0f0; /* Light grey background */
    color: #666; /* Darker text color */
    border: 1px solid #ccc; /* Lighter border */
}
</style>
