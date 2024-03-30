<script setup lang="ts">
import Calendar from 'primevue/calendar';
import BaseLayout from '@/components/layout/BaseLayout.vue';
import Title from '@/components/layout/Title.vue';
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';

const { t } = useI18n();

const courseName = ref('');
const courseDescription = ref('');
const courseYear = ref(null);

function createCourse() {
  console.log('Creating course');
}
</script>

<template>
    <BaseLayout>
        <div class="grid fadein">
            <div class="col-12 md:col-6">
                <!-- Create course heading -->
                <Title class="mb-6">{{ t('views.courses.create') }}</Title>

                <!-- Course form -->
                <form @submit.prevent="createCourse">
                    <!-- Course name -->
                    <div class="mb-4">
                        <label for="courseName">{{ t('views.courses.name') }}</label>
                        <InputText id="courseName" v-model="courseName" required/>
                    </div>

                    <!-- Course description -->
                    <div class="mb-4">
                        <label for="courseDescription">{{ t('views.courses.description') }}</label>
                        <Textarea id="courseDescription" v-model="courseDescription" rows="5" cols="30" />
                    </div>

                    <!-- Course academic year -->
                    <div class="mb-4">
                        <label for="courseYear">{{ t('views.courses.year') }}</label>
                        <Calendar id="courseYear" v-model="courseYear" view="year" dateFormat="yy" />
                    </div>
                    
                    <!-- Submit button -->
                    <div class="flex justify-end">
                        <button type="submit" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                            {{ t('views.courses.create') }}
                        </button>
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
