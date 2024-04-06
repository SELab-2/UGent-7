<script setup lang="ts">
import DataTable, {
    DataTableFilterEvent,
    DataTableSelectAllChangeEvent, DataTableSortEvent,
} from 'primevue/datatable';
import Column from 'primevue/column';
import Dialog from 'primevue/dialog';
import InputSwitch from 'primevue/inputswitch';
import Button from 'primevue/button';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import InputText from 'primevue/inputtext';
import AdminLayout from '@/components/layout/admin/AdminLayout.vue';
import Title from '@/components/layout/Title.vue';
import { ref, onMounted, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useUser } from '@/composables/services/users.service.ts';
import { useFilter } from '@/composables/filters/filter.ts';
import { usePaginator } from '@/composables/filters/paginator.ts';

import { roles, Role, User } from '@/types/users/User.ts';
import { USER_FILTER } from '@/types/filter/Filter.ts';

/* Composable injections */
const { t } = useI18n();
const { pagination, users, getUsers, searchUsers } = useUser();
const { filter } = useFilter(USER_FILTER);
const { paginate, page, first, pageSize } = usePaginator();

onMounted(async () => {
    await loadLazyData();

    watch(
        filter,
        async () => {
            await paginate(0).then(() => {
                pagination.value = null;
            });
            await loadLazyData();
        },
        { deep: true },
    );

    watch(
        page,
        async () => {
            await loadLazyData();
        }
    )
});

const dt = ref();
const loading = ref(false);
const totalRecords = ref(0);
const selectedStudents = ref();
const selectAll = ref(false);
const editItem = ref<User>(User.blankUser());
const popupEdit = ref<boolean>(false);


const columns = ref([
    {field: 'id', header: 'ID', width: '5rem'},
    {field: 'username', header: 'Username', width: '6rem'},
    {field: 'email', header: 'Email', width: '10rem'},
    {field: 'roles', header: 'Roles', width: '5rem'},
]);

const loadLazyData = async () => {
    loading.value = true;

    setTimeout(async () => {
        await searchUsers(filter.value, page.value, pageSize.value).then(() => {
            loading.value = false;
        })
    },
        500
    )
};
const onFilter = async (event: DataTableFilterEvent) => {
    await paginate(event.first);
    await loadLazyData();
};
const onSort = async (event: DataTableSortEvent) => {
    await paginate(event.first);
    await loadLazyData();
}
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
    popupEdit.value = true;
};

const updateRole = (role: Role) => {
    const index = editItem.value.roles.findIndex((role2: string) => role == role2);
    if (index != -1) { // if role is in role list of user
        editItem.value.roles.splice(index, 1);
    } else { // role is NOT in role list of user
        editItem.value.roles.push(role);
    }
};

const saveItem = () => {
    if (pagination.value != null) {
        if (editItem.value.roles.includes("student") && editItem.value.roles.includes("teacher")) {
            // this is not allowed TODO
        } else {
            // update locally
            const index = pagination.value.results.findIndex((row: User) => row.id == editItem.value.id);
            pagination.value.results.splice(index, 1, {...editItem.value});
            // update remotely TODO
        }
    } else {
        // raise error TODO
    }
    popupEdit.value = false;
};

const searchText = (header: string) => {
    return `${header} search`
}

</script>

<template>
    <AdminLayout>
        <Title>
            <div class="gap-3 mb-3">{{ t('admin.users.title') }}</div>
            <div class="card p-fluid">
                <DataTable :value="pagination?.results" lazy paginator v-model:first="first" :rows="pageSize" ref="dt" dataKey="id" auto-layout
                    :totalRecords="pagination?.count" :loading="loading" @page="loadLazyData"
                           @sort="onSort($event)" @filter="onFilter($event)" filterDisplay="row"
                    :globalFilterFields="['name','country.name', 'company', 'representative.name']"
                    v-model:selection="selectedStudents" :selectAll="selectAll" @select-all-change="onSelectAllChange" @row-select="onRowSelect" @row-unselect="onRowUnselect" tableStyle="min-width: 75rem">
                    <template #header>
                        <div class="flex justify-content-end">
                            <IconField iconPosition="left">
                                <InputIcon>
                                    <i class="pi pi-search" />
                                </InputIcon>
                                <InputText v-model="filter['search']"
                                           placeholder="Keyword Search" />
                            </IconField>
                        </div>
                    </template>
                    <template #empty>No matching data.</template>
                    <template #loading>Loading data. Please wait.</template>
                    <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
                    <Column v-for="column in columns" :field="column.field" :header="column.header"
                            :show-filter-menu="false" :style="{ minWidth: '14rem' }">
                        <template #filter>
                            <IconField v-if="column.field != 'roles'"
                                       iconPosition="left" class="flex align-items-center">
                                <InputIcon>
                                    <i class="pi pi-search" />
                                </InputIcon>
                                <InputText v-model="filter[column.field]"
                                           :placeholder="searchText(column.header)" />
                            </IconField>
                        </template>
                        <template #body="{ data }" v-if="column.field == 'roles'">
                            {{ data.roles.join(', ') }}
                        </template>
                    </Column>
                    <Column>
                        <template #body="{ data }">
                            <Button @click="() => showPopup(data)">Edit</Button>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </Title>
    </AdminLayout>
    <Dialog v-model:visible="popupEdit" header="Edit user" :style="{ width: '25rem' }" class="flex" id="editDialog">
        <div class="flex align-items-center gap-3 mb-3">
            <label class="font-semibold w-6rem">{{ columns[0].header }}</label>
            <span>{{ editItem.id }}</span>
        </div>
        <div v-for="data in columns.toSpliced(columns.length - 1, 1).toSpliced(0, 1)"
             class="flex align-items-center gap-3 mb-3">
            <label class="font-semibold w-6rem">{{ data.header }}</label>
            <span>{{ editItem[data.field] }}</span>
        </div>
        <div v-for="role in roles.toSpliced(0, 1)" class="flex align-items-center gap-3 mb-3">
            <label class="font-semibold w-6rem">{{ role }}</label>
            <InputSwitch :model-value="editItem.roles.includes(role)" @click="() => updateRole(role)"/>
        </div>
        <div class="flex justify-content-end gap-2">
            <Button type="button" label="Cancel" severity="secondary" @click="popupEdit = false"></Button>
            <Button type="button" label="Save" @click="saveItem"></Button>
        </div>
    </Dialog>
</template>

<style scoped lang="scss">

</style>
