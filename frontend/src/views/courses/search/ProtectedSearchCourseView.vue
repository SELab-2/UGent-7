<script setup lang="ts">
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import ProtectedSearchStepper from '@/components/courses/search/ProtectedSearchStepper.vue';
import Title from '@/components/layout/Title.vue';
import BaseLayout from '@/components/layout/base/BaseLayout.vue';
import { useI18n } from 'vue-i18n';
import { ref } from 'vue';

/* Composable injections */
const { t } = useI18n();

/* State */
const searchQuery = ref('');

/**
 * Fetch the courses based on the filter.
 */
async function searchCourses(): Promise<void> {
    console.log('Searching courses...');
}


</script>

<template>
    <BaseLayout>
        <div class="grid">
            <div class="col-12 xl:col-3">
                <ProtectedSearchStepper />
            </div>
            <div class="col-12 xl:col-9 mt-4 xl:mt-0">
                <div class="flex justify-content-between align-items-center">
                    <Title>
                        {{ t('views.courses.search.title') }}
                    </Title>
                    <slot name="publicButton" />
                </div>

                <div class="flex gap-2 mt-4">
                    <InputText v-model="searchQuery" :placeholder="t('views.courses.search.placeholderByLink')" style="width: 80%;" />                    
                    <Button label="Search" @click="searchCourses" />
                </div>                
            </div>
        </div>
    </BaseLayout>
</template>

<style scoped lang="scss">
</style>