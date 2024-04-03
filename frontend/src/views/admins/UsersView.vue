<script setup lang="ts">
import AdminLayout from '@/components/layout/admin/AdminLayout.vue';
import Title from '@/components/layout/Title.vue';
import { ref, onMounted } from 'vue';
import { useUser } from '@/composables/services/users.service.ts';
import DataTable, {
    DataTableFilterEvent,
    DataTablePageEvent,
    DataTableSelectAllChangeEvent,
    DataTableSortEvent,
} from "primevue/datatable";
import Column from "primevue/column"

import {useI18n} from 'vue-i18n';

const { users, getUsers } = useUser();
const { t } = useI18n();


onMounted(() => {
    loading.value = true;

    lazyParams.value = {
        first: 0,
        rows: 10,
        sortField: null,
        sortOrder: null,
        filters: filters.value
    };

    loadLazyData();
});

const dt = ref();
const loading = ref(false);
const totalRecords = ref(0);
const selectedStudents = ref();
const selectAll = ref(false);
const first = ref(0);
const filters = ref({
    'name': {value: '', matchMode: 'contains'},
    'country.name': {value: '', matchMode: 'contains'},
    'company': {value: '', matchMode: 'contains'},
    'representative.name': {value: '', matchMode: 'contains'},
});
const lazyParams: {[key: string]: any} = ref({});
const columns = ref([
    {field: 'id', header: 'ID'},
    {field: 'username', header: 'Username'},
    {field: 'email', header: 'Email'},
    {field: 'roles', header: 'Roles'},
]);

const loadLazyData = (event?: DataTablePageEvent | DataTableSortEvent | DataTableFilterEvent) => {
    loading.value = true;
    lazyParams.value = { ...lazyParams.value, first: event?.first || first.value };

    setTimeout(() => {
        getUsers().then(() => {
            loading.value = false;
            totalRecords.value = users.value?.length ?? 0
        });
    }, Math.random() * 1000 + 250);
};
const onPage = (event: DataTablePageEvent) => {
    lazyParams.value = event;
    loadLazyData(event);
};
const onSort = (event: DataTableSortEvent) => {
    lazyParams.value = event;
    loadLazyData(event);
};
const onFilter = (event: DataTableFilterEvent) => {
    lazyParams.value.filters = filters.value ;
    loadLazyData(event);
};
const onSelectAllChange = (event: DataTableSelectAllChangeEvent) => {
    selectAll.value = event.checked;

    if (selectAll.value) {
        getUsers().then(() => {
            selectAll.value = true;
            selectedStudents.value = users.value;
        });
    } else {
        selectAll.value = false;
        selectedStudents.value = [];
    }
};
const onRowSelect = () => {
    selectAll.value = selectedStudents.value.length === totalRecords.value;
};
const onRowUnselect = () => {
    selectAll.value = false;
};

</script>

<template>
    <AdminLayout>
        <Title>
            {{ t('admin.users.title') }}
            <div class="card p-fluid">
                <DataTable :value="users" lazy paginator :first="first" :rows="10" v-model:filters="filters" ref="dt" dataKey="id"
                    :totalRecords="totalRecords" :loading="loading" @page="onPage($event)" @sort="onSort($event)" @filter="onFilter($event)" filterDisplay="row"
                    :globalFilterFields="['name','country.name', 'company', 'representative.name']"
                    v-model:selection="selectedStudents" :selectAll="selectAll" @select-all-change="onSelectAllChange" @row-select="onRowSelect" @row-unselect="onRowUnselect" tableStyle="min-width: 75rem">
                    <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
                    <Column v-for="column in columns" :field="column.field" :header="column.header"></Column>
                </DataTable>
            </div>
        </Title>
    </AdminLayout>
</template>

<style scoped lang="scss">

</style>
