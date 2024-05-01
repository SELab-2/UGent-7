<script setup lang="ts">
import SelectButton from 'primevue/selectbutton';
import { computed, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import PublicSearchCourseView from './search/PublicSearchCourseView.vue';
import ProtectedSearchCourseView from './search/ProtectedSearchCourseView.vue';

/* Composable injections */
const { t } = useI18n();

/* State of the public/protected course */
const publicCourses = ref<boolean>(true);

/* Options for the select button */
const options = computed(() => [
    { label: t('components.button.public'), value: true },
    { label: t('components.button.protected'), value: false },
]);
</script>

<template>
    <!-- If the public option is set, display the search option for all the public courses -->
    <PublicSearchCourseView v-if="publicCourses">
        <template #publicButton>
            <SelectButton
                v-model="publicCourses"
                :options="options"
                option-value="value"
                option-label="label"
                :allow-empty="false"
            />
        </template>
    </PublicSearchCourseView>

    <!-- If the protected option is set, display the search option for all the protected courses -->
    <ProtectedSearchCourseView v-else>
        <template #publicButton>
            <SelectButton
                v-model="publicCourses"
                :options="options"
                option-value="value"
                option-label="label"
                :allow-empty="false"
            />
        </template>
    </ProtectedSearchCourseView>
</template>

<style scoped lang="scss"></style>
