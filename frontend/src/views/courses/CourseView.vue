<script setup lang="ts">
import Calendar from 'primevue/calendar';
import Skeleton from 'primevue/skeleton';
import BaseLayout from '@/components/layout/BaseLayout.vue';
import Title from '@/components/Title.vue';
import {onMounted} from 'vue';
import {useCourses} from '@/composables/services/courses.service.ts';
import {useRoute} from 'vue-router';
import {useI18n} from "vue-i18n";

const { params } = useRoute();
const { course, getCourseByID } = useCourses();
const { t } = useI18n()

onMounted(() => {
    getCourseByID(
        params.courseId as string,
        t
    );
});
</script>

<template>
    <BaseLayout>
        <div class="grid">
            <div class="col-12 md:col-6">
                <div>
                    <Title v-if="course">
                        {{ course.name }}
                    </Title>
                    <Skeleton class="mb-4" height="3rem" width="30rem" v-else/>
                </div>

                <div>
                    <p v-if="course">
                        {{ course.description }}
                    </p>
                    <Skeleton height="10rem" v-else/>
                </div>
            </div>
            <div class="col-12 md:col-6">
                <div>
                    <Calendar v-if="course" class="w-full" inline/>
                    <Skeleton height="30rem" v-else/>
                </div>
            </div>
        </div>
    </BaseLayout>
</template>

<style scoped lang="scss">

</style>