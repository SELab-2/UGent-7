<script setup lang="ts">
import Calendar from 'primevue/calendar';
import ProgressSpinner from 'primevue/progressspinner';
import BaseLayout from '@/components/layout/BaseLayout.vue';
import Title from '@/components/Title.vue';
import {Course} from '@/types/Course.ts';
import {onMounted, Ref, ref} from 'vue';

const course: Ref<Course|null> = ref(null);

onMounted(() => {
    // Set a timeout to simulate a network fetch.
    setTimeout(() => {
        course.value = new Course(1, 'Information Security Yippee', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In purus arcu, pharetra sit amet purus posuere, laoreet ullamcorper mi. Vivamus vitae egestas nibh. Proin id enim condimentum, egestas nisl in, vehicula nunc. Fusce ornare mattis dolor finibus dictum.', 2023)
    }, 1000);
});
</script>

<template>
    <BaseLayout>
        <template v-if="course">
            <div class="grid">
                <div class="col-12 md:col-6">
                    <Title>
                        {{ course.name }}
                    </Title>
                    <p>{{ course.description }}</p>
                </div>
                <div class="col-12 md:col-6">
                    <Calendar class="w-full" inline/>
                </div>
            </div>
        </template>
        <template v-else>
            <!-- Course is still loading -->
            <div class="flex align-items-center justify-content-center p-4 w-full">
                <ProgressSpinner/>
            </div>
        </template>
    </BaseLayout>
</template>

<style scoped lang="scss">

</style>