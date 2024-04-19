<script setup lang="ts">
import DataTable, { type DataTableSelectAllChangeEvent } from 'primevue/datatable';
import Column from 'primevue/column';
import Dialog from 'primevue/dialog';
import InputSwitch from 'primevue/inputswitch';
import Button from 'primevue/button';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import InputText from 'primevue/inputtext';
import MultiSelect from 'primevue/multiselect';
import AdminLayout from '@/components/layout/admin/AdminLayout.vue';
import Title from '@/components/layout/Title.vue';
import { ref, onMounted, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useUser } from '@/composables/services/users.service.ts';
import { useStudents } from '@/composables/services/student.service.ts';
import { useAssistant } from '@/composables/services/assistant.service.ts';
import { useTeacher } from '@/composables/services/teacher.service.ts';
import { useFilter } from '@/composables/filters/filter.ts';
import { usePaginator } from '@/composables/filters/paginator.ts';

import { roles, type Role, User } from '@/types/users/User.ts';
import { getUserFilters } from '@/types/filter/Filter.ts';
import { useRoute } from 'vue-router';

/* Composable injections */
const { t } = useI18n();
const { query } = useRoute();
const { pagination, users, getUsers, searchUsers, toggleAdmin } = useUser();
const { createStudent, deleteStudent } = useStudents();
const { createAssistant, deleteAssistant } = useAssistant();
const { createTeacher, deleteTeacher } = useTeacher();
const { filter, onFilter } = useFilter(getUserFilters(query));
const { page, first, pageSize, onPaginate, resetPagination } = usePaginator();

onMounted(async () => {
    fillCreators();
    fillDestroyers();

    onPaginate(fetchUsers);

    watch(
        filter,
        () => {
            loading.value = true;
        },
        { deep: true },
    );

    onFilter(fetchUsers);

    onFilter(
        async () => {
            await resetPagination([pagination]);
        },
        0,
        false,
    );
});

const creators = ref<Record<Role, (arg: any) => Promise<void>>>({});
const createFunctions = ref<Array<(arg: any) => Promise<void>>>([createStudent, createAssistant, createTeacher]);
const destroyers = ref<Record<Role, (arg: any) => Promise<void>>>({});
const destroyFunctions = ref<Array<(arg: any) => Promise<void>>>([deleteStudent, deleteAssistant, deleteTeacher]);

const loading = ref(false);
const selectedUsers = ref();
const selectAll = ref(false);
const editItem = ref<User>(User.blankUser());
const popupEdit = ref<boolean>(false);

const columns = ref([
    { field: 'id', header: 'admin.users.id' },
    { field: 'username', header: 'admin.users.username' },
    { field: 'email', header: 'admin.users.email' },
    { field: 'roles', header: 'admin.users.roles' },
]);

const fillCreators = (): void => {
    for (let i = 1; i < roles.length; i++) {
        const role: Role = roles[i];
        creators.value[role] = createFunctions.value[i - 1];
    }
};
const fillDestroyers = (): void => {
    for (let i = 1; i < roles.length; i++) {
        const role: Role = roles[i];
        destroyers.value[role] = destroyFunctions.value[i - 1];
    }
};
const fetchUsers = async (): Promise<void> => {
    loading.value = true;
    await searchUsers(filter.value, page.value, pageSize.value).then(() => {
        loading.value = false;
    });
};
const onSelectAllChange = (event: DataTableSelectAllChangeEvent): void => {
    selectAll.value = event.checked;

    if (selectAll.value) {
        getUsers().then(() => {
            selectAll.value = true;
            selectedUsers.value = users.value;
        });
    } else {
        selectAll.value = false;
        selectedUsers.value = [];
    }
};
const onRowSelect = (): void => {
    selectAll.value = selectedUsers.value.length === (pagination.value?.count ?? 0);
};
const onRowUnselect = (): void => {
    selectAll.value = false;
};

const showPopup = (data: any): void => {
    editItem.value = JSON.parse(JSON.stringify(data)); // I do this to get a deep copy of the role array
    popupEdit.value = true;
};

const updateRole = (role: Role): void => {
    const index = editItem.value.roles.findIndex((role2: string) => role === role2);
    if (index !== -1) {
        // if role is in role list of user
        editItem.value.roles.splice(index, 1);
    } else {
        // role is NOT in role list of user
        editItem.value.roles.push(role);
    }
};

const saveItem = async (): Promise<void> => {
    const value = pagination.value;
    if (value?.results !== null) {
        const index = value.results.findIndex((row: User) => row.id === editItem.value.id);
        // update remotely TODO
        const paginationItem = value.results[index];

        for (let i = 1; i < roles.length; i++) {
            const role = roles[i];
            const paginationIncludes = paginationItem.roles.includes(role);
            const editIncludes = editItem.value.roles.includes(role);
            if (!paginationIncludes && editIncludes) {
                // add role in backend
                const func = creators.value[role];

                if (role === 'student') {
                    console.log('student reported');
                    const data: Record<string, any> = {
                        ...editItem.value,
                        studentId: editItem.value.id,
                    };
                    await func(data);
                } else {
                    await func(editItem.value);
                }
            } else if (paginationIncludes && !editIncludes) {
                // remove role in backend
                const func = destroyers.value[role];
                await func(editItem.value.id);
            }
        }
        // update admin status
        await toggleAdmin(editItem.value.id, editItem.value.is_staff);
        // update locally
        await fetchUsers();
    } else {
        // raise error TODO
    }
    popupEdit.value = false;
};
</script>

<template>
    <AdminLayout>
        <Title>
            <div class="gap-3 mb-3">{{ t('admin.users.title') }}</div>
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
                        <div class="flex justify-content-end">
                            <IconField iconPosition="left">
                                <InputIcon>
                                    <i class="pi pi-search" />
                                </InputIcon>
                                <InputText v-model="filter['search']" :placeholder="t('admin.search.general')" />
                            </IconField>
                        </div>
                    </template>
                    <template #empty>No matching data.</template>
                    <template #loading>Loading data. Please wait.</template>
                    <Column selectionMode="multiple" headerStyle="width: 3rem" class="justify-content-center"></Column>
                    <Column
                        v-for="column in columns"
                        :key="column.field"
                        :field="column.field"
                        :header="t(column.header)"
                        :show-filter-menu="false"
                        :style="{ minWidth: '14rem' }"
                    >
                        <template #filter>
                            <IconField
                                v-if="column.field != 'roles'"
                                iconPosition="left"
                                class="flex align-items-center"
                            >
                                <InputIcon>
                                    <i class="pi pi-search flex justify-content-center" />
                                </InputIcon>
                                <InputText v-model="filter[column.field]" :placeholder="t('admin.search.search')" />
                            </IconField>
                            <MultiSelect
                                v-else
                                class="flex align-items-center h-3rem"
                                v-model="filter.roles"
                                :options="roles.toSpliced(0, 1)"
                            />
                        </template>
                        <template #body="{ data }" v-if="column.field == 'roles'">
                            {{ data.roles.join(', ') }}
                        </template>
                    </Column>
                    <Column>
                        <template #body="{ data }">
                            <Button @click="() => showPopup(data)">{{ t('admin.edit') }}</Button>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </Title>
    </AdminLayout>
    <Dialog v-model:visible="popupEdit" header="Edit user" :style="{ width: '28rem' }" class="flex" id="editDialog">
        <div
            v-for="data in columns.toSpliced(columns.length - 1, 1)"
            :key="data.field"
            class="flex align-items-center gap-3 mb-3"
        >
            <label class="font-semibold w-10rem">{{ t(data.header) }}</label>
            <span>{{ editItem[data.field] }}</span>
        </div>
        <div v-for="role in roles.toSpliced(0, 1)" :key="role" class="flex align-items-center gap-3 mb-3">
            <label class="font-semibold w-10rem">{{ t('admin.' + role) }}</label>
            <InputSwitch :model-value="editItem.roles.includes(role)" @click="() => updateRole(role)" />
        </div>
        <div class="flex align-items-center gap-3 mb-3">
            <label class="font-semibold w-10rem">{{ t('admin.title') }}</label>
            <InputSwitch :model-value="editItem.is_staff" @click="editItem.is_staff = !editItem.is_staff" />
        </div>
        <div class="flex justify-content-end gap-2">
            <Button type="button" :label="t('admin.cancel')" severity="secondary" @click="popupEdit = false"></Button>
            <Button type="button" :label="t('admin.save')" @click="saveItem"></Button>
        </div>
    </Dialog>
</template>

<style scoped lang="scss"></style>
