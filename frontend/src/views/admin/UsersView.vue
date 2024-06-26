<script setup lang="ts">
import Column from 'primevue/column';
import Dialog from 'primevue/dialog';
import InputSwitch from 'primevue/inputswitch';
import Button from 'primevue/button';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import InputText from 'primevue/inputtext';
import MultiSelect from 'primevue/multiselect';
import AdminLayout from '@/views/layout/admin/AdminLayout.vue';
import Title from '@/views/layout/Title.vue';
import Body from '@/views/layout/Body.vue';
import LazyDataTable from '@/components/admin/LazyDataTable.vue';
import { ref, onMounted, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { useUser } from '@/composables/services/users.service.ts';
import { useStudents } from '@/composables/services/student.service.ts';
import { useAssistant } from '@/composables/services/assistant.service.ts';
import { useTeacher } from '@/composables/services/teacher.service.ts';
import { useFilter } from '@/composables/filters/filter.ts';
import { useMessagesStore } from '@/store/messages.store.ts';

import { roles, type Role, User } from '@/types/users/User.ts';
import { getUserFilters } from '@/types/filter/Filter.ts';
import { useRoute } from 'vue-router';

/* Composable injections */
const { t } = useI18n();
const { addErrorMessage, addSuccessMessage } = useMessagesStore();
const { query } = useRoute();
const { pagination, users, getUsers, searchUsers, toggleAdmin } = useUser();
const { createStudent, deleteStudent } = useStudents();
const { createAssistant, deleteAssistant } = useAssistant();
const { createTeacher, deleteTeacher } = useTeacher();
const { filter, onFilter } = useFilter(getUserFilters(query));

/* Initialization */
onMounted(() => {
    fillCreatorsDestroyers();
});

/* State */
const creators = ref<Record<Role, (arg: any) => Promise<void>>>({});
const createFunctions = ref<Array<(arg: any) => Promise<void>>>([createStudent, createAssistant, createTeacher]);
const destroyers = ref<Record<Role, (arg: any) => Promise<void>>>({});
const destroyFunctions = ref<Array<(arg: any) => Promise<void>>>([deleteStudent, deleteAssistant, deleteTeacher]);

const dataTable = ref();
const editItem = ref<User>(User.blankUser());
const popupEdit = ref<boolean>(false);

const columns = ref([
    { field: 'id', header: 'admin.id' },
    { field: 'username', header: 'admin.users.username' },
    { field: 'email', header: 'admin.users.email' },
    { field: 'roles', header: 'admin.users.roles' },
]);

const roleOptions = computed(() => {
    return roles.toSpliced(0, 1);
});

/* Functions */
/**
 * FillCreatorsDestroyers fills 2 dictionaries: a dictionary that links a role to the function that creates an instance
 * of the role in the backend AND a dictionary that links a role to the function that destroys an instance of that role
 * in the backend.
 */
const fillCreatorsDestroyers = (): void => {
    for (let i = 1; i < roles.length; i++) {
        const role: Role = roles[i];
        creators.value[role] = createFunctions.value[i - 1];
        destroyers.value[role] = destroyFunctions.value[i - 1];
    }
};
/**
 * A function to that shows a popup to edit the User item
 * @param data This contains the attributes of the User item to be edited.
 */
const showPopup = (data: any): void => {
    editItem.value = JSON.parse(JSON.stringify(data)); // I do this to get a deep copy of the role array
    popupEdit.value = true;
};
/**
 * Removes or adds role to roles list of User to be edited
 * @param role
 */
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
/**
 * saveItem saves the editItem with its edited values to the backend
 */
const saveItem = async (): Promise<void> => {
    const value = pagination.value;
    if (value?.results !== null) {
        // retrieve the original values of the User we're editing
        const index = value.results.findIndex((row: User) => row.id === editItem.value.id);
        const paginationItem = value.results[index];

        try {
            for (let i = 1; i < roles.length; i++) {
                const role = roles[i];
                // determine whether a role is in our original item and whether it's in our update item
                // knowing this, we know which roles to destroy in the backend and which to create
                const paginationIncludes = paginationItem.roles.includes(role);
                const editIncludes = editItem.value.roles.includes(role);
                if (!paginationIncludes && editIncludes) {
                    // add role in backend
                    const func = creators.value[role];

                    // if the role that needs to be created is a student, a studentId needs to be supplied as well
                    if (role === 'student') {
                        const data: Record<string, any> = {
                            ...editItem.value,
                            student_id: editItem.value.id,
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
            addSuccessMessage(
                t('toasts.messages.success'),
                t('toasts.messages.edit', { type: t('types.article.user') }),
            );
        } catch (e) {
            // TODO error message (failed to edit user)
        }
        // update locally
        await dataTable.value.fetch();
    } else {
        addErrorMessage(t('toasts.messages.admin.save.error.title'), t('toasts.messages.admin.save.error.detail'));
    }
    // stop showing popup
    popupEdit.value = false;
};
</script>

<template>
    <AdminLayout>
        <Title>
            {{ t('admin.users.title') }}
        </Title>
        <Body>
            <LazyDataTable
                :pagination="pagination"
                :entities="users"
                :get="getUsers"
                :search="searchUsers"
                :filter="filter"
                :on-filter="onFilter"
                ref="dataTable"
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
                <Column
                    v-for="column in columns"
                    :key="column.field"
                    :field="column.field"
                    :header="t(column.header)"
                    :show-filter-menu="false"
                    :header-style="{ width: '22%' }"
                    class="p-col"
                >
                    <template #filter>
                        <IconField v-if="column.field != 'roles'" iconPosition="left" class="flex align-items-center">
                            <InputIcon>
                                <i class="pi pi-search flex justify-content-center" />
                            </InputIcon>
                            <InputText
                                v-model="filter[column.field] as string"
                                :placeholder="t('admin.search.search')"
                            />
                        </IconField>
                        <MultiSelect
                            v-else
                            class="flex align-items-center h-3rem"
                            v-model="filter.roles"
                            :options="roleOptions"
                            :option-label="(role: Role) => t('admin.' + role)"
                        />
                    </template>
                    <template #body="{ data }" v-if="column.field == 'roles'">
                        {{ data.roles.map((role: Role) => t('admin.' + role)).join(', ') }}
                    </template>
                </Column>
                <Column :header-style="{ width: '12%' }" class="p-col">
                    <template #body="{ data }">
                        <Button @click="() => showPopup(data)" class="justify-content-center w-auto">
                            {{ t('admin.edit') }}
                        </Button>
                    </template>
                </Column>
            </LazyDataTable>
        </Body>
    </AdminLayout>
    <Dialog v-model:visible="popupEdit" header="Edit user" :style="{ width: '28rem' }" class="flex" id="editDialog">
        <div
            v-for="data in columns.toSpliced(columns.length - 1, 1)"
            :key="data.field"
            class="flex align-items-center gap-3 mb-3"
        >
            <label class="font-semibold w-10rem">{{ t(data.header) }}</label>
            <span>{{ (editItem as any)[data.field] }}</span>
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
