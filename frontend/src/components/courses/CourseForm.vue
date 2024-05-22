<script setup lang="ts">
import { Course } from '@/types/Course.ts';
import { useI18n } from 'vue-i18n';
import { computed, ref, watchEffect } from 'vue';
import { helpers, required } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import Textarea from 'primevue/textarea';
import Dropdown from 'primevue/dropdown';
import InputText from 'primevue/inputtext';
import ErrorMessage from '@/components/forms/ErrorMessage.vue';
import Button from 'primevue/button';
import Editor from '@/components/forms/Editor.vue';
import InputSwitch from 'primevue/inputswitch';
import { type Faculty } from '@/types/Faculty.ts';

/* Props */
const props = defineProps<{
    faculties: Faculty[];
    course?: Course | undefined;
}>();

/* Emits */
const emit = defineEmits(['update:course']);

/* Composable injections */
const { t } = useI18n();

/* State */
const form = ref(new Course());

const rules = computed(() => {
    return {
        name: { required: helpers.withMessage(t('validations.required'), required) },
        faculty: { required: helpers.withMessage(t('validations.required'), required) },
        excerpt: { required: helpers.withMessage(t('validations.required'), required) },
    };
});

const v$ = useVuelidate(rules, form);

/**
 * Save the course form to the API backend.
 */
async function saveCourse(): Promise<void> {
    // Validate the form.
    const result = await v$.value.$validate();

    // Only submit the form if the validation was successful
    if (result) {
        emit('update:course', form.value);
    }
}

/**
 * Watch for changes in the course prop and update the form values.
 */
watchEffect(() => {
    /* Set the form values with the existing project */
    const course = props.course;

    if (course !== undefined) {
        form.value = new Course(
            course.id,
            course.name,
            course.excerpt,
            course.description,
            course.academic_startyear,
            course.private_course,
            course.invitation_link,
            course.invitation_link_expires,
            course.parent_course,
            course.faculty,
        );
    }
});
</script>

<template>
    <!-- Course form -->
    <form @submit.prevent="saveCourse">
        <div class="grid formgrid">
            <!-- Course name -->
            <div class="field col-12">
                <label for="courseName">{{ t('views.courses.name') }}</label>
                <InputText id="courseName" class="w-full" v-model="form.name" />
                <ErrorMessage :field="v$.name" />
            </div>

            <!-- Course excerpt -->
            <div class="field col-12">
                <label for="courseExcerpt">{{ t('views.courses.excerpt') }}</label>
                <Textarea id="courseExcerpt" v-model="form.excerpt" autoResize rows="5" cols="30" />
                <ErrorMessage :field="v$.excerpt" />
            </div>

            <!-- Course description -->
            <div class="field col-12">
                <label for="courseDescription">{{ t('views.courses.description') }}</label>
                <Editor v-model="form.description as string" />
            </div>

            <!-- Course faculty -->
            <div class="field col-12">
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

            <!-- Course visibility -->
            <div class="field col-12 my-3">
                <div class="flex align-items-center field-checkbox">
                    <InputSwitch id="private" v-model="form.private_course" />
                    <label for="private">{{ t('views.courses.private') }}</label>
                </div>
            </div>
        </div>

        <!-- Submit button -->
        <Button id="courseSave" :label="t('views.courses.save')" type="submit" icon="pi pi-check" iconPos="right" rounded />
    </form>
</template>

<style scoped lang="scss"></style>
