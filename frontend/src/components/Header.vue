<script setup lang="ts">
import enLogo from '@/assets/img/logo-en.png';
import nlLogo from '@/assets/img/logo-nl.png';
import nlFlag from '@/assets/img/flags/nl-flag.svg'
import enFlag from '@/assets/img/flags/en-flag.svg'
import Dropdown from 'primevue/dropdown';
import {useI18n} from 'vue-i18n';
import {watch, computed, onMounted} from 'vue';
import { usePrimeVue } from "primevue/config";
import nl from '@/assets/lang/nl.json';
import en from '@/assets/lang/en.json';

/* Translation composable */
const { t, locale, availableLocales } = useI18n();
const { config } = usePrimeVue();

const localeFiles : {[key: string]: any} = { "nl": nl, "en": en };

/* Set the primevue locale when the locale changes */
watch(locale, (newVal) => {
    config.locale = localeFiles[newVal].primevue;
});

/* Available localized images */
const logo: {[key: string]: string} = { nl: nlLogo, en: enLogo };
const flags: {[key: string]: string} = { nl: nlFlag, en: enFlag };

/* Navigation items */
const items = computed(() => [
    {icon: 'home', label: t('layout.header.navigation.dashboard'), route: 'dashboard'},
    {icon: 'calendar', label: t('layout.header.navigation.calendar'), route: 'calendar'},
    {icon: 'book', label: t('layout.header.navigation.courses'), route: ''}
]);

/* Set the primevue locale on mounted */
onMounted(() => {
    config.locale = localeFiles[locale.value].primevue;
});

</script>

<template>
    <div class="flex w-full">
        <div class="w-full lg:w-2 flex align-items-center p-3 lg:pl-0">
            <img class="w-full max-w-9rem" :src="logo[locale]" :alt="t('layout.header.logo')">
        </div>
        <div class="flex flex-column w-full lg:w-10">
            <div id="header" class="w-full flex text-white p-4">
                <div class="flex align-items-end">
                    <h1 class="text-white m-0">Ypovoli</h1>
                </div>
                <div class="text-right w-12rem ml-auto text-sm flex flex-column align-items-end gap-3">
                    <!-- Language selector -->
                    <Dropdown id="language" v-model="locale" class="w-auto" :options="availableLocales" variant="outlined">
                        <template #option="{ option }">
                            <div class="flex align-items-center">
                                <img :alt="t('layout.header.language.' + option)" :src="flags[option]" class="h-1rem mr-3"/>
                                <div>
                                    {{ t('layout.header.language.' + option) }}
                                </div>
                            </div>
                        </template>
                        <template #value="{ value }" class="pr-0">
                            <div class="uppercase text-sm">{{ value }}</div>
                        </template>
                    </Dropdown>
                    <!-- User information -->
                    <span>
                        Ingelogd als Lander Maes
                    </span>
                </div>
            </div>
            <!-- Navigation -->
            <div id="navigation" class="w-full h-full flex">
                <RouterLink :to="{ name: item.route }" v-for="item in items">
                    <div class="flex align-items-center uppercase flex justify-content-center p-3 pl-0 cursor-pointer text-primary font-medium nav-item">
                        <span class="mr-2" :class="'pi pi-' + item.icon"/> {{ item.label }}
                    </div>
                </RouterLink>
            </div>
        </div>
    </div>
</template>

<style lang="scss">
#header {
    background: var(--primary-color);

    #language {
        background: transparent;
        color: var(--primary-color-text);
        border: none;
        padding: .25rem;

        .p-inputtext {
            padding: 0;
            color: var(--primary-color-text);
        }

        .p-dropdown-trigger {
            width: auto;
            color: var(--primary-color-text);
            margin-left: 0.5rem;
        }
    }
}

.nav-item {
    position: relative;
    z-index: 1;

    &::after {
        content: '';
        display: block;
        position: absolute;
        bottom: .2rem;
        left: 0;
        width: 0;
        height: 2px;
        background: var(--primary-color);
        transition: width .3s;
    }

    &:hover::after, &.active::after {
        width: calc(100% - 1rem);
    }
}
</style>