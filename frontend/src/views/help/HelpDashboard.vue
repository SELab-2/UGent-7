<script setup lang="ts">
import HelpBaseLayout from '@/components/help/HelpBaseLayout.vue';
import Menu from 'primevue/menu';
import { RouterLink } from 'vue-router';
// TODO add menu

const itemsStudent = [
    { label: 'login-logout', route: '/help/student/login-out' },
    { label: 'verander taal', route: '/help/student/change-lang' },
    // Add more sidebar items as needed
];

const items = itemsStudent;
</script>

<template>
    <HelpBaseLayout>
        <div>
            <Menu :model="items" class="w-full md:w-15rem">
                <template #start>
                    <span class="inline-flex align-items-center gap-1 px-2 py-2">
                        <svg
                            width="35"
                            height="40"
                            viewBox="0 0 35 40"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                            class="h-2rem"
                        >
                            <path d="..." fill="var(--primary-color)" />
                            <path d="..." fill="var(--text-color)" />
                        </svg>
                        <span class="font-medium text-xl font-semibold"><span class="text-primary">YPOVOLI</span></span>
                    </span>
                </template>
                <template #submenuheader="{ item }">
                    <span class="text-primary font-bold">{{ item.label }}</span>
                </template>
                <template #item="{ item, props }">
                    <router-link v-if="item.route" v-slot="{ href, navigate }" :to="item.route" custom>
                        <a v-ripple :href="href" v-bind="props.action" @click="navigate">
                            <span :class="item.icon" />
                            <span class="ml-2">{{ item.label }}</span>
                            <Badge v-if="item.badge" class="ml-auto" :value="item.badge" />
                            <span
                                v-if="item.shortcut"
                                class="ml-auto border-1 surface-border border-round surface-100 text-xs p-1"
                                >{{ item.shortcut }}</span
                            >
                        </a>
                    </router-link>
                </template>
            </Menu>
        </div>
    </HelpBaseLayout>
</template>

<style scoped></style>
