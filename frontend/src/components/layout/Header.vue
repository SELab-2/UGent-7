<script setup lang="ts">
import en from '@/assets/img/logo-en.png';
import nl from '@/assets/img/logo-nl.png';
import Button from 'primevue/button';
import LanguageSelector from '@/components/LanguageSelector.vue';
import { useI18n } from 'vue-i18n';
import { computed } from 'vue';
import { useAuthStore } from '@/store/authentication.store.ts';
import { storeToRefs } from 'pinia';
import RoleSelector from '@/components/RoleSelector.vue';

/* Composables */
const { user, isAuthenticated } = storeToRefs(useAuthStore());
const { t, locale } = useI18n();

/* Localization variables */
const logo = computed(() => {
    if (locale.value === 'nl') {
        return nl;
    }

    return en;
});

/* Navigation items */
const items = computed(() => [
    {
        icon: 'home',
        label: t('layout.header.navigation.dashboard'),
        route: 'dashboard',
    },
    {
        icon: 'calendar',
        label: t('layout.header.navigation.calendar'),
        route: 'calendar',
    },
    {
        icon: 'book',
        label: t('layout.header.navigation.courses'),
        route: 'courses',
    },
    {
        icon: 'bookmark',
        label: t('layout.header.navigation.projects'),
        route: 'projects',
    },
]);
</script>

<template>
    <div class="flex w-full">
        <div class="w-full lg:w-2 flex align-items-center p-3 lg:pl-0">
            <img class="w-full max-w-9rem" :src="logo" :alt="t('layout.header.logo')" />
        </div>
        <div class="flex flex-column w-full lg:w-10">
            <div id="header" class="w-full flex text-white p-4">
                <div class="flex align-items-end">
                    <h1 class="text-white m-0">Ypovoli</h1>
                </div>
                <div class="text-right ml-auto text-sm flex flex-column align-items-end gap-3">
                    <div class="flex align-items-center gap-3">
                        <template v-if="user !== null && user.hasMultipleRoles()">
                            <!-- Role selector -->
                            <RoleSelector />
                        </template>
                        <!-- Language selector -->
                        <LanguageSelector />
                    </div>
                    <div>
                        <!-- User information -->
                        <template v-if="user !== null">
                            <RouterLink :to="{ name: 'logout' }" class="text-white">
                                {{ t('layout.header.user', [user.getFullName()]) }}
                            </RouterLink>
                        </template>
                        <!-- Login button -->
                        <template v-else>
                            <RouterLink :to="{ name: 'login' }">
                                <Button
                                    icon="pi pi-unlock"
                                    :label="t('layout.header.login')"
                                    severity="secondary"
                                    class="text-sm"
                                />
                            </RouterLink>
                        </template>
                    </div>
                </div>
            </div>
            <!-- Navigation -->
            <div id="navigation" class="w-full h-full flex">
                <template v-if="isAuthenticated">
                    <RouterLink :to="{ name: item.route }" v-for="item in items" :key="item.route" class="nav-item">
                        <div
                            class="flex align-items-center uppercase flex justify-content-center p-3 pl-0 cursor-pointer text-primary font-medium"
                        >
                            <span class="mr-2" :class="'pi pi-' + item.icon" />
                            {{ item.label }}
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

    #language,
    #view {
        background: transparent;
        color: var(--primary-color-text);
        border: none;
        padding: 0.25rem;

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
        bottom: 0.2rem;
        left: 0;
        width: 0;
        height: 2px;
        background: var(--primary-color);
        transition: width 0.3s;
    }

    &:hover::after,
    &.active::after {
        width: calc(100% - 1rem);
    }
}
</style>
