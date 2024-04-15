<script lang="ts" setup>
import { ref } from 'vue';
import Menu from 'primevue/menu';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const items = ref([
    {
        label: 'admin.users.title',
        items: [
            {
                label: 'admin.users.title',
                route: 'admin-users',
            },
            {
                label: 'admin.assistants.title',
            },
            {
                label: 'admin.students.title',
            },
            {
                label: 'admin.teachers.title',
            },
        ],
    },
]);
</script>

<template>
    <div class="card flex">
        <Menu :model="items" class="w-full md:w-15rem">
            <template #item="{ item, props }">
                <RouterLink :to="{ name: item.route }">
                    <a v-ripple class="flex align-items-center" v-bind="props.action">
                        <span class="ml-2">{{ t(item.label) }}</span>
                        <span
                            v-if="item.shortcut"
                            class="ml-auto border-1 surface-border border-round surface-100 text-xs p-1"
                            >{{ item.shortcut }}</span
                        >
                    </a>
                </RouterLink>
            </template>
        </Menu>
    </div>
</template>
