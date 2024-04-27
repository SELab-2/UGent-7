<script setup lang="ts">
import Stepper from 'primevue/stepper';
import StepperPanel from 'primevue/stepperpanel';
import Button from 'primevue/button';
</script>

<template>
    <Stepper orientation="vertical">
        <StepperPanel header="Bemachtigen link">
            <template #content="{ nextCallback }">
                <div class="flex flex-column h-12rem">
                    <div class="border-4 surface-border border-round flex-auto flex justify-content-center align-items-center">
                        Professoren kunnen kiezen om hun vakken niet publiek te maken. Vraag de prof om de link van het vak te delen, om te kunnen toetreden tot het vak.
                    </div>
                </div>
                <div class="flex py-4 justify-content-end">
                    <Button icon="pi pi-arrow-right" iconPos="right" @click="nextCallback" text class="p-button-rounded" />
                </div>
            </template>
        </StepperPanel>
        <StepperPanel header="Vak zoeken">
            <template #content="{ prevCallback, nextCallback }">
                <div class="flex flex-column h-12rem">
                    <div class="border-4 surface-border border-round flex-auto flex justify-content-center align-items-center">
                        Gebruik de link om het vak te zoeken. Als je het vak niet kan vinden, kan je de prof vragen om de link opnieuw te delen.
                    </div>
                </div>
                <div class="flex py-4 gap-2">
                    <Button icon="pi pi-arrow-left" @click="prevCallback" text class="p-button-rounded" />
                    <Button icon="pi pi-arrow-right" iconPos="right" @click="nextCallback" text class="p-button-rounded" />
                </div>
            </template>
        </StepperPanel>
        <StepperPanel header="Inschrijven">
            <template #content="{ prevCallback }">
                <div class="flex flex-column h-12rem">
                    <div class="border-4 surface-border border-round flex-auto flex justify-content-center align-items-center">
                        Schrijf je in voor het vak. Je kan nu de lopende projecten raadplegen.
                    </div>
                </div>
                <div class="flex py-4 justify-content-start">
                    <Button icon="pi pi-arrow-left" @click="prevCallback" text class="p-button-rounded" />
                </div>
            </template>
        </StepperPanel>
    </Stepper>
</template>

<style scoped lang="scss">
/* Custom styles for text display */
.font-medium {
    font-size: 1.2rem; /* Adjust font size as needed */
    font-weight: 500; /* Adjust font weight for emphasis */
    color: #333; /* Adjust text color */
}
</style>