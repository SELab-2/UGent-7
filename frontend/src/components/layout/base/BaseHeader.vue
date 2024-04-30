<script setup lang="ts">
import en from '@/assets/img/logo-en.png';
import nl from '@/assets/img/logo-nl.png';
import tiny from '@/assets/img/logo-tiny.png';
import Button from 'primevue/button';
import LanguageSelector from '@/components/LanguageSelector.vue';
import RoleSelector from '@/components/RoleSelector.vue';
import Sidebar from 'primevue/sidebar';
import { useI18n } from 'vue-i18n';
import { computed, ref } from 'vue';
import { useAuthStore } from '@/store/authentication.store.ts';
import { storeToRefs } from 'pinia';
import { endpoints } from '@/config/endpoints.ts';

/* Composables */
const { user, isAuthenticated } = storeToRefs(useAuthStore());
const { t, locale } = useI18n();

/* State */
const showSidebar = ref(false);
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
        <!-- Logo -->
        <div class="lg:w-2 lg:pl-0 flex align-items-center p-3">
            <RouterLink :to="'/'">
                <img class="w-full max-w-9rem" :src="logo" :alt="t('layout.header.logo')" />
            </RouterLink>
        </div>
        <!-- Content -->
        <div class="flex flex-column w-full lg:w-10">
            <!-- Header -->
            <div id="header" class="w-full flex text-white p-4">
                <!-- Title -->
                <div class="hidden md:flex align-items-end">
                    <h1 class="text-white m-0">Ypovoli</h1>
                </div>
                <!-- User information -->
                <div class="text-right ml-auto text-sm flex flex-column align-items-end gap-3">
                    <div class="flex align-items-center gap-3">
                        <template v-if="user !== null && user.hasMultipleRoles()">
                            <!-- Role selector -->
                            <RoleSelector />
                        </template>
                        <!-- Language selector -->
                        <LanguageSelector />
                        <!-- Menu selector -->
                        <span @click="showSidebar = !showSidebar" class="md:hidden pi pi-bars cursor-pointer" />
                    </div>
                    <div>
                        <!-- User information -->
                        <template v-if="user !== null">
                            <RouterLink :to="{ name: 'logout' }" class="text-white">
                                <span class="hidden md:inline">
                                    {{ t('layout.header.user', [user.getFullName()]) }}
                                </span>
                                <span class="inline md:hidden">
                                    {{ user.getFullName() }}
                                </span>
                            </RouterLink>
                        </template>
                        <!-- Login button -->
                        <template v-else>
                            <a :href="endpoints.auth.login">
                                <Button
                                    icon="pi pi-unlock"
                                    :label="t('layout.header.login')"
                                    severity="secondary"
                                    class="text-sm"
                                />
                            </a>
                        </template>
                    </div>
                </div>
            </div>
            <!-- Navigation -->
            <div id="navigation" class="hidden md:flex w-full h-full">
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
        <Sidebar v-model:visible="showSidebar">
            <template #container="{ closeCallback }">
                <div class="flex flex-column h-full">
                    <div class="flex align-items-center justify-content-between p-4 pb-2 flex-shrink-0">
                        <span class="inline-flex align-items-center gap-2">
                            <img :alt="t('layout.header.logo')" :src="tiny" class="w-2rem mr-2" />
                            <span class="font-bold text-2xl text-primary">Ypovoli</span>
                        </span>
                        <span>
                            <Button
                                type="button"
                                @click="closeCallback"
                                icon="pi pi-times"
                                rounded
                                outlined
                                class="h-2rem w-2rem"
                            />
                        </span>
                    </div>
                    <div class="overflow-y-auto px-2">
                        <ul class="list-none p-0 m-0">
                            <li v-for="item in items" :key="item.route">
                                <RouterLink
                                    :to="{ name: item.route }"
                                    @click="closeCallback"
                                    class="flex align-items-center cursor-pointer p-3 text-black-alpha-90 border-bottom-1 border-300"
                                    v-ripple
                                >
                                    <i class="mr-2" :class="'pi pi-' + item.icon" />
                                    <span class="font-medium">{{ item.label }}</span>
                                </RouterLink>
                            </li>
                        </ul>
                    </div>
                </div>
            </template>
        </Sidebar>
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
