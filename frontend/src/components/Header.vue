<script setup lang="ts">
import enLogo from '@/assets/img/logo-en.png';
import nlLogo from '@/assets/img/logo-nl.png';
import nlFlag from '@/assets/img/flags/nl-flag.svg';
import enFlag from '@/assets/img/flags/en-flag.svg';
import Dropdown from 'primevue/dropdown';
import Button from 'primevue/button';
import {useI18n} from 'vue-i18n';
import {computed} from 'vue';
import {useAuthStore} from '@/store/authentication.store.ts';
import {storeToRefs} from 'pinia';

/* Composables */
const { user, isAuthenticated } = storeToRefs(useAuthStore());
const { t, locale, availableLocales } = useI18n();

/* Localization variables */
const logo: {[key: string]: string} = { 'nl': nlLogo, en: enLogo };
const flags: {[key: string]: string} = { nl: nlFlag, en: enFlag };

/* Navigation items */
const items = computed(() => [
    {icon: 'home', label: t('layout.header.navigation.dashboard'), route: 'dashboard'},
    {icon: 'calendar', label: t('layout.header.navigation.calendar'), route: 'calendar'},
    {icon: 'book', label: t('layout.header.navigation.courses'), route: 'courses'}
]);

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
                <div class="text-right w-14rem ml-auto text-sm flex flex-column align-items-end gap-3">
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
                    <div>
                        <template v-if="isAuthenticated && user">
                            <RouterLink :to="{name:'logout'}" class="text-white">
                                Ingelogd als {{ user.getFullName() }}
                            </RouterLink>
                        </template>
                        <template v-else>
                            <RouterLink :to="{ name: 'login' }">
                                <Button icon="pi pi-unlock" :label="t('layout.header.login')" severity="secondary" class="text-sm"/>
                            </RouterLink>
                        </template>
                    </div>
                </div>
            </div>
            <!-- Navigation -->
            <div id="navigation" class="w-full h-full flex">
                <template v-if="isAuthenticated">
                    <RouterLink :to="{ name: item.route }" v-for="item in items" class="nav-item">
                        <div class="flex align-items-center uppercase flex justify-content-center p-3 pl-0 cursor-pointer text-primary font-medium">
                            <span class="mr-2" :class="'pi pi-' + item.icon"/> {{ item.label }}
                        </div>
                    </RouterLink>
                </template>
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