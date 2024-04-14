<script setup lang="ts">
import Dropdown from 'primevue/dropdown';
import { useI18n } from 'vue-i18n';
import { computed } from 'vue';

/* Composable injections */
const { t } = useI18n();

/* Props */
const props = defineProps<{ years: number[] }>();

/* State */
const years = computed(() =>
    props.years.map((year) => ({
        label: `${year} - ${year + 1}`,
        value: year,
    })),
);

/* Models */
const year = defineModel();
</script>

<template>
    <Dropdown v-model="year" :options="years" optionLabel="label" optionValue="value" class="custom-dropdown">
        <template #value="{ value }">
            <span class="text-primary font-semibold"
                >{{ t('components.button.academic_year') }} {{ value }} - {{ value + 1 }}</span
            >
        </template>
        <template #option="{ option }">
            <span class="pi pi-calendar mr-2" />
            <span>{{ t('components.button.academic_year') }} {{ (option as any).label }}</span>
        </template>
        <template #dropdownicon>
            <i class="pi pi-chevron-down pr-1 text-primary"></i>
        </template>
    </Dropdown>
</template>

<style scoped lang="scss">
.custom-dropdown {
    border-radius: 0;
}
</style>
