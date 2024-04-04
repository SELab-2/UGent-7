<script setup lang="ts">
import AdminLayout from '@/components/layout/admin/AdminLayout.vue';
import Title from '@/components/layout/Title.vue';
import { ref, onMounted, computed } from 'vue';
import { useUser } from '@/composables/services/users.service.ts';
import DataTable, {
    DataTableFilterEvent,
    DataTablePageEvent,
    DataTableSelectAllChangeEvent,
    DataTableSortEvent,
} from "primevue/datatable";
import Column from "primevue/column";
import Dialog from "primevue/dialog";
import InputText from "primevue/inputtext";
import InputSwitch from "primevue/inputswitch";
import Button from "primevue/button";

import User from "@/types/User.ts";

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
const editItem = ref<User|null>(null);
const popup = ref<boolean>(false);
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
const roles = ref([
    "student",
    "assistant",
    "teacher"
])

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
    lazyParams.value.filters = filters.value;
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

const showPopup = (data: any) => {
    editItem.value = JSON.parse(JSON.stringify(data)); // I do this to get a deep copy of the role array
    popup.value = true;
}

const updateRole = (role: string) => {
    const index = editItem.value.roles.findIndex((role2: string) => role == role2);
    if (index != -1) { // if role is in role list of user
        editItem.value.roles.splice(index, 1);
    } else { // role is NOT in role list of user
        editItem.value.roles.push(role);
    }
}

const saveItem = () => {
    if (users.value != null) {
        const index = users.value.findIndex(row => row.id == editItem.value.id);
        users.value.splice(index, 1, { ...editItem.value });
    } else {
        // raise error TODO
    }
    popup.value = false;
}

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
                    <Column>
                        <template #body="{ data }">
                            <Button @click="() => showPopup(data)">Edit</Button>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </Title>
    </AdminLayout>
    <Dialog v-model:visible="popup" header="Edit user" :style="{ width: '25rem' }" class="flex">
        <div class="flex align-items-center gap-3 mb-3">
            <label class="font-semibold w-6rem">{{ columns[0].header }}</label>
            <span>{{ editItem.id }}</span>
        </div>
        <div v-for="data in columns.toSpliced(columns.length - 1, 1).toSpliced(0, 1)"
             class="flex align-items-center gap-3 mb-3">
            <label class="font-semibold w-6rem">{{ data.header }}</label>
            <InputText type="text" class="flex-auto" v-model="editItem[data.field]"/>
        </div>
        <div v-for="role in roles" class="flex align-items-center">
            <label class="font-semibold w-6rem">{{ role }}</label>
            <InputSwitch :model-value="editItem.roles.includes(role)" @click="() => updateRole(role)"/>
        </div>
        <div class="flex justify-content-end gap-2">
            <Button type="button" label="Cancel" severity="secondary" @click="popup = false"></Button>
            <Button type="button" label="Save" @click="saveItem"></Button>
        </div>
    </Dialog>
</template>

<style scoped lang="scss">

</style>
