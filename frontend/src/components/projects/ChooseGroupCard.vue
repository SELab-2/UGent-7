<script setup lang="ts">
import {onMounted, ref} from 'vue';
import { useI18n } from 'vue-i18n';
import {useGroup} from "@/composables/services/groups.service.ts";
import {useRoute} from "vue-router";
import Dialog from 'primevue/dialog';
import {useStudents} from "@/composables/services/students.service.ts";
import {storeToRefs} from "pinia";
import {useAuthStore} from "@/store/authentication.store.ts";

/* Composable injections */
  const emit = defineEmits(['group-joined']);
const route = useRoute()
const {group, groups, getGroupsByProject, getGroupByID} = useGroup();
const {student} = storeToRefs(useAuthStore());
const { students, getStudentsByGroup, studentJoinGroup } = useStudents();
const { t } = useI18n();

const dialogVisible = ref<Boolean>(false);
const selectedGroupId = ref<string>('');

const showGroupDialog = async (groupId: string) => {
  selectedGroupId.value = groupId;
  console.log("fetching students");
  await getStudentsByGroup(groupId);
  dialogVisible.value = true;
  console.log(students);
};

const joinSelectedGroup = async () => {
  console.log(`joining group ${selectedGroupId.value}`);
  await studentJoinGroup(selectedGroupId.value, student.value?.id as string);
  dialogVisible.value = false;
  await getGroupByID(selectedGroupId.value);
  emit('group-joined', group);
};

onMounted(async () => {
  const projectId = route.params.projectId as string;
  await getGroupsByProject(projectId);
});

</script>

<template>
  <div>
    <div class="groupcard">
      <h2>{{ t('views.projects.chooseGroup') }}</h2>
      <div v-if="groups">
        <button class="p-3" v-for="group in groups" :key="group.id" @click="showGroupDialog(group.id)">
          {{ t('views.projects.group') }} {{ group.id }}
        </button>
      </div>
      <Dialog v-model:visible="dialogVisible" modal :header="`${t('views.projects.group')} ${selectedGroupId}`" :style="{ width: '25rem' }">
        <ul v-if="students">
          <li v-for="student in students" :key="student.id">
            {{ student.first_name }} {{ student.last_name }}
          </li>
        </ul>
        <button @click="joinSelectedGroup">Join Group</button>
      </Dialog>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import '@/assets/scss/theme/theme.scss';
button {
  display: block;
  background: none;
  border: none;
  text-align: left;
  font-size: $fontSize;
  padding: 0.5rem 1rem;
  cursor: pointer;
  color: $textSecondaryColor;
  margin-bottom: 0.5rem;
  border-bottom: 1px solid #e0e0e0;
}
button:last-child {
  border-bottom: none;
}
</style>
