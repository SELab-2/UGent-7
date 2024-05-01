<script setup lang="ts">
import Stepper from 'primevue/stepper';
import StepperPanel from 'primevue/stepperpanel';
import Button from 'primevue/button';
import { useI18n } from 'vue-i18n';

/* Composable injections */
const { t } = useI18n();
</script>

<template>
    <Stepper orientation="vertical">
        <StepperPanel :header="t('protectedCourses.screen1.title')">
            <template #content="{ nextCallback }">
                <div class="flex flex-column h-12rem">
                    <div
                        class="border-4 surface-border border-round flex-auto flex justify-content-center align-items-center"
                    >
                        {{ t('protectedCourses.screen1.content') }}
                    </div>
                </div>
                <div class="flex py-4 justify-content-end">
                    <Button
                        icon="pi pi-arrow-right"
                        iconPos="right"
                        @click="nextCallback"
                        text
                        class="p-button-rounded"
                    />
                </div>
            </template>
        </StepperPanel>
        <StepperPanel :header="t('protectedCourses.screen2.title')">
            <template #content="{ prevCallback, nextCallback }">
                <div class="flex flex-column h-12rem">
                    <div
                        class="border-4 surface-border border-round flex-auto flex justify-content-center align-items-center"
                    >
                        {{ t('protectedCourses.screen2.content') }}
                    </div>
                </div>
                <div class="flex py-4 gap-2 justify-content-between">
                    <Button icon="pi pi-arrow-left" @click="prevCallback" text class="p-button-rounded" />
                    <Button
                        icon="pi pi-arrow-right"
                        iconPos="right"
                        @click="nextCallback"
                        text
                        class="p-button-rounded"
                    />
                </div>
            </template>
        </StepperPanel>
        <StepperPanel :header="t('protectedCourses.screen3.title')">
            <template #content="{ prevCallback }">
                <div class="flex flex-column h-12rem">
                    <div
                        class="border-4 surface-border border-round flex-auto flex justify-content-center align-items-center"
                    >
                        {{ t('protectedCourses.screen3.content') }}
                    </div>
                </div>
                <div class="flex py-4 justify-content-start">
                    <Button icon="pi pi-arrow-left" @click="prevCallback" text class="p-button-rounded" />
                </div>
            </template>
        </StepperPanel>
    </Stepper>
</template>

<style scoped lang="scss"></style>
