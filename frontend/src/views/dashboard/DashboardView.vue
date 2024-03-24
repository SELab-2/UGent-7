<script setup lang="ts">
import ButtonGroup from 'primevue/buttongroup';
import Button from 'primevue/button';
import CourseCard from '@/components/courses/CourseCard.vue';
import BaseLayout from '@/components/layout/BaseLayout.vue';
import Title from '@/components/Title.vue';
import { useI18n } from 'vue-i18n';
import { PrimeIcons } from 'primevue/api';
import { onMounted } from 'vue';
import { useCourses } from '@/composables/services/courses.service.ts';
import { useStudents } from '@/composables/services/students.service.ts';
import { Course } from '@/types/Course.ts';
import {ref} from 'vue';

/* Composable injections */
const { t } = useI18n();

/* Service injection */
const { courses, getCoursesByStudent, createCourse, deleteCourse } = useCourses();
const { studentJoinCourse } = useStudents();


onMounted(async () => {
  console.log("fetching courses");
  await getCoursesByStudent(1);  // TODO make this the id of the logged in user
});

// test code vvvv

const idValue = ref('');
const vaknaam = ref('');

// Method to execute when the button is clicked
const executeCode = () => {
  // Put your code here that you want to execute
  console.log('Button clicked! Code executed.');
  createCourse({name: vaknaam.value, academic_startyear:2023});
};

// Function to handle form submission
const handleSubmit = () => {
  // Perform actions here, such as sending the input value to a backend API
  console.log('Submitted value:', idValue.value);
  studentJoinCourse(idValue.value, "1");
};

// Function to handle form submission
const handleDelete = () => {
  // Perform actions here, such as sending the input value to a backend API
  console.log('Submitted value:', idValue.value);
  deleteCourse(idValue.value);
};

// test code ^^^^

</script>

<template>
    <BaseLayout>
        <!-- Course heading -->
        <div class="flex justify-content-between align-items-center mb-6">
            <!-- Course list title -->
            <Title class="m-0">{{ t('views.dashboard.courses') }}</Title>
            <!-- Course list controls -->
            <ButtonGroup>
                <Button :label="t('components.buttons.academic_year', ['2023-2024'])" :icon="PrimeIcons.CHEVRON_DOWN" icon-pos="right" outlined/>
                <Button :icon="PrimeIcons.PLUS" icon-pos="right"/>
            </ButtonGroup>
        </div>
        <!--extra code to test -->
        <input type="text" v-model="vaknaam" placeholder="vaknaam" />
        <button @click="executeCode">create course with vaknaam</button>
        <input type="text" v-model="idValue" placeholder="ID" />
        <button @click="handleSubmit">join course with id</button>
        <button @click="handleDelete">delete course with id</button>
        <!--extra code to test -->

        <!-- Course list body -->
        <div class="grid align-items-stretch">
            <div class="col-12 md:col-6 lg:col-4 xl:col-3" v-for="course in courses">
                <CourseCard class="h-100" :course="course"/>
            </div>
        </div>
        <!-- Project heading -->
        <div class="flex justify-content-between align-items-center my-6">
            <!-- Project list title -->
            <Title class="m-0">{{ t('views.dashboard.projects') }}</Title>
            <!-- Project list controls -->
            <ButtonGroup>
                <Button :label="t('components.buttons.academic_year', ['2023-2024'])" :icon="PrimeIcons.CHEVRON_DOWN" icon-pos="right" outlined/>
                <Button :icon="PrimeIcons.PLUS" icon-pos="right"/>
            </ButtonGroup>
        </div>
        <!-- Project list body -->
        <div class="grid align-items-stretch">

        </div>
    </BaseLayout>
</template>

<style scoped>

</style>