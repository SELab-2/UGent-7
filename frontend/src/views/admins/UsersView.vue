<script setup lang="ts">
import DataTable, {
    DataTableFilterEvent,
    DataTablePageEvent,
    DataTableSelectAllChangeEvent,
    DataTableSortEvent,
} from 'primevue/datatable';
import Column from 'primevue/column';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import InputSwitch from 'primevue/inputswitch';
import Button from 'primevue/button';
import AdminLayout from '@/components/layout/admin/AdminLayout.vue';
import Title from '@/components/layout/Title.vue';
import { ref, onMounted, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { watchDebounced } from '@vueuse/core'
import { useUser } from '@/composables/services/users.service.ts';
import { useFilter } from '@/composables/filters/filter.ts';
import { usePaginator } from '@/composables/filters/paginator.ts';

import { roles, Role, User } from '@/types/users/User.ts';
import { USER_FILTER } from '@/types/filter/Filter.ts';

/* Composable injections */
const { t } = useI18n();
const { pagination, users, getUsers, searchUsers, createUser } = useUser();
const { filter } = useFilter(USER_FILTER);
const { paginate, page, first, pageSize } = usePaginator();

onMounted(async () => {
    await getUsers()

    watch(
        filter,
        () => {
            paginate(0);
            pagination.value = null;
        },
        { deep: true },
    );

    watch(
        page,
        async () => {
            await searchUsers(filter.value, page.value, pageSize.value)
        }
    )

    watchDebounced(
        filter,
        async () => {
            await searchUsers(filter.value, page.value, pageSize.value)
        },
        { debounce: 500, immediate: true, deep: true}
    );
});

const dt = ref();
const loading = ref(false);
const totalRecords = ref(0);
const selectedStudents = ref();
const selectAll = ref(false);
const editItem = ref<User>(User.blankUser());
const popupEdit = ref<boolean>(false);
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


const popupAdd = ref<boolean>(false);
const admin = ref<User>(User.blankUser());
const adminColumns = ref([
    {field: 'username', header: 'Username'},
    {field: 'email', header: 'Email'},
    {field: 'first_name', header: 'First name'},
    {field: 'last_name', header: 'Last name'},
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
    if (users.value != null) {
        if (editItem.value.roles.includes("student") && editItem.value.roles.includes("teacher")) {
            // this is not allowed TODO
        } else {
            // update locally
            const index = users.value.findIndex((row: User) => row.id == editItem.value.id);
            users.value.splice(index, 1, {...editItem.value});
            // update remotely TODO
        }
    } else {
        // raise error TODO
    }
    popupEdit.value = false;
};

const showAdminAddPopup = () => {
    admin.value = User.blankUser();
    admin.value.is_staff = true;
    popupAdd.value = true;
}

const addAdmin = () => {
    // local
    loadLazyData();
    // remote
    createUser(admin.value);
    popupAdd.value = false;
};

</script>

<template>
    <AdminLayout>
        <Title>
            <div class="gap-3 mb-3">{{ t('admin.users.title') }}</div>
            <div class="card p-fluid">
                <DataTable :value="users" lazy paginator :first="first" :rows="pageSize" v-model:filters="filters" ref="dt" dataKey="id"
                    :totalRecords="pagination?.count" :loading="loading" @update:first="paginate($event)" @sort="onSort($event)" @filter="onFilter($event)" filterDisplay="row"
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
            <Button @click="showAdminAddPopup">Add admin</Button>
        </Title>
    </AdminLayout>
    <Dialog v-model:visible="popupEdit" header="Edit user" :style="{ width: '25rem' }" class="flex" id="editDialog">
        <div v-for="data in columns.toSpliced(columns.length - 1, 1)"
             class="flex align-items-center gap-3 mb-3">
            <label class="font-semibold w-6rem">{{ data.header }}</label>
            <span>{{ editItem[data.field] }}</span>
        </div>
        <div v-for="role in roles" class="flex align-items-center gap-3 mb-3">
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
