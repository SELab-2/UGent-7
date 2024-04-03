<script lang="ts" setup>
import { ref } from "vue";
import Menu from 'primevue/menu';
import {useI18n} from "vue-i18n";

const { t } = useI18n()

const items = ref([
    {
        label: t('admin.users.title'),
        items: [
            {
                label: t('admin.users.title')
            },
            {
                label: t('admin.assistants.title')
            },
            {
                label: t('admin.students.title')
            },
            {
                label: t('admin.teachers.title')
            }
        ]
    },
    {
        label: 'Profile',
        items: [
            {
                label: 'Settings',
                icon: 'pi pi-cog',
                shortcut: '⌘+O'
            },
            {
                label: 'Messages',
                icon: 'pi pi-inbox',
                badge: 2
            },
            {
                label: 'Logout',
                icon: 'pi pi-sign-out',
                shortcut: '⌘+Q'
            }
        ]
    },
]);
</script>

<template>
    <div class="card flex">
        <Menu :model="items" class="w-full md:w-15rem">
            <template #item="{ item, props }">
                <a v-ripple class="flex align-items-center" v-bind="props.action">
                    <span class="ml-2">{{ item.label }}</span>
                    <span v-if="item.shortcut" class="ml-auto border-1 surface-border border-round surface-100 text-xs p-1">{{ item.shortcut }}</span>
                </a>
            </template>
        </Menu>
    </div>
</template>