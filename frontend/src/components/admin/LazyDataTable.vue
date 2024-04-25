<script setup lang="ts">
import DataTable from "primevue/datatable";
import { onMounted, watch, ref } from "vue";
import { PaginatorResponse } from '@/types/filter/Paginator.ts'
import { usePaginator } from '@/composables/filters/paginator.ts';
import { Filter } from "@/types/filter/Filter.ts";
import { useFilter} from "@/composables/filters/filter.ts";

/* Properties */
const props = defineProps<{
    pagination: PaginatorResponse<any>
    search: (filters: Filter, page: number, pageSize: number) => Promise<void>
    filterState: Filter // is used to get filter and onFilter out of UseFilter()
}>()

/* Injections */
const { page, first, pageSize, onPaginate, resetPagination } = usePaginator();
const { filter, onFilter } = useFilter(props.filterState);



const loading = ref(false);

onMounted(async () => {
    watch(
        filter,
        () => {
            loading.value = true;
        },
        { deep: true },
    );

    onFilter(fetch);

    onFilter(
        async () => {
            await resetPagination([pagination]);
        },
        0,
        false,
    );
})

const fetch = async (): Promise<void> => {
    loading.value = true;
    props.search(filter.value, page.value, pageSize.value).then(() => {
        loading.value = false;
    })
}
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
            v-model:selection="selectedUsers"
            :selectAll="selectAll"
            @select-all-change="onSelectAllChange"
            @row-select="onRowSelect"
            @row-unselect="onRowUnselect"
            tableStyle="min-width: 75rem"
        >
            <template #header>
                <slot name="header" />
            </template>
            <template #empty>No matching data.</template>
            <template #loading>Loading data. Please wait.</template>
            <slot />

        </DataTable>
    </div>
</template>

<style scoped lang="scss">

</style>