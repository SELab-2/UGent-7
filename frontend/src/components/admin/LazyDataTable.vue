<script setup lang="ts">
import DataTable, { type DataTableSelectAllChangeEvent } from 'primevue/datatable';
import { onMounted, watch, ref, toRef } from 'vue';
import { useI18n } from 'vue-i18n';
import { type PaginatorResponse } from '@/types/filter/Paginator.ts';
import { usePaginator } from '@/composables/filters/paginator.ts';
import { type Filter } from '@/types/filter/Filter.ts';
import Column from 'primevue/column';

/* Properties */
const props = withDefaults(
    defineProps<{
        pagination: PaginatorResponse<any> | null;
        entities: any[] | null; // list containing all the entities displayed by data table after executing get method
        get: () => Promise<void>; // get method for backend
        search: (filters: Filter, page: number, pageSize: number) => Promise<void>;
        filter: Filter;
        onFilter: (
            callback: () => Promise<void>,
            debounce?: number | undefined,
            immediate?: boolean | undefined,
        ) => void;
        select?: boolean;
    }>(),
    {
        select: false,
    },
);

/* Emits */
const emit = defineEmits(['select']);

/* Injections */
const { t } = useI18n();
const { page, first, pageSize, onPaginate, resetPagination } = usePaginator();

const loading = ref(false);
const selected = ref<any[] | null>(null);
const selectAll = ref(false);

onMounted(async () => {
    onPaginate(fetch);

    watch(
        props.filter,
        () => {
            loading.value = true;
        },
        { deep: true },
    );
    props.onFilter(fetch);

    props.onFilter(
        async () => {
            await resetPagination([toRef(props.pagination)]);
        },
        0,
        false,
    );
});

const fetch = async (): Promise<void> => {
    loading.value = true;
    props.search(props.filter, page.value, pageSize.value).then(() => {
        loading.value = false;
    });
};
const onSelectAllChange = (event: DataTableSelectAllChangeEvent): void => {
    selectAll.value = event.checked;

    if (selectAll.value) {
        props.get().then(() => {
            selectAll.value = true;
            selected.value = props.entities;
            emit('select', selected.value);
        });
    } else {
        selectAll.value = false;
        selected.value = [];
        emit('select', selected.value);
    }
};
const onRowSelect = (): void => {
    selectAll.value = selected.value?.length === (props.pagination?.count ?? 0);
    emit('select', selected.value);
};
const onRowUnselect = (): void => {
    selectAll.value = false;
    emit('select', selected.value);
};

defineExpose({ fetch });
</script>

<template>
    <div class="card p-fluid">
        <DataTable
            :value="pagination?.results"
            lazy
            paginator
            v-model:first="first"
            :rows="pageSize"
            dataKey="id"
            auto-layout
            :totalRecords="pagination?.count"
            :loading="loading"
            @page="loading = true"
            filterDisplay="row"
            v-model:selection="selected"
            :selectAll="selectAll"
            @select-all-change="onSelectAllChange"
            @row-select="onRowSelect"
            @row-unselect="onRowUnselect"
            tableStyle="min-width: 75rem"
        >
            <template #header>
                <slot name="header" />
            </template>
            <template #empty>
                <slot name="empty">
                    {{ t('admin.noneFound') }}
                </slot>
            </template>
            <template #loading>
                <slot name="loading">
                    {{ t('admin.loading') }}
                </slot>
            </template>
            <Column v-if="select" selectionMode="multiple" headerStyle="width: 3rem" class="justify-content-center" />
            <slot />
        </DataTable>
    </div>
</template>

<style scoped lang="scss"></style>
