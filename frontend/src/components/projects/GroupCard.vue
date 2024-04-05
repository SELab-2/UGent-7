<script setup lang="ts">
import {useStudents} from '@/composables/services/students.service.ts';
import {computed, onMounted, watch} from 'vue';
import {useI18n} from 'vue-i18n';
import {type Group} from '@/types/Group.ts';
import {storeToRefs} from "pinia";
import {useAuthStore} from "@/store/authentication.store.ts";

/* Props */
const props = defineProps<{
  group: Group;
}>();

const emit = defineEmits(['group-left']);

/* Composable injections */
const {student} = storeToRefs(useAuthStore());
const {students, getStudentsByGroup, studentLeaveGroup} = useStudents();
const {t} = useI18n();

watch(() => props.group, async (newGroup) => {
  await getStudentsByGroup(newGroup.id);
}, { deep: true });

onMounted(async () => {
  console.log("in groupcard")
  console.log(props.group)
  if (props.group.id !== undefined) {
    await getStudentsByGroup(props.group.id);
  }
});

const leaveSelectedGroup = async () => {
  console.log("leaving group")
  console.log(props.group.id)
  await studentLeaveGroup(props.group.id, student.value?.id as string);
  emit('group-left', null);
};

</script>

<template>
  <div class="groupcard">
    <h2>{{ t('views.projects.groupMembers') }}</h2>
    <div>
      <p class="p-3" v-for="student in students" :key="student.id">{{ student.first_name }} {{ student.last_name }}</p>
    </div>
    <button @click="leaveSelectedGroup">Leave Group</button>
  </div>

</template>

<style lang="scss">
@import '@/assets/scss/theme/theme.scss';

.groupcard {
  background-color: white;
  border-radius: $borderRadius;
  padding: $cardBodyPadding;
  border-style: solid;
  border-color: $primaryLightColor;
  border-width: $borderWidth;
  color: $primaryColor;

  div {
    p {
      color: $textSecondaryColor;
      border-bottom: 1px solid #e0e0e0;
    }

    /* Zorgt ervoor dat er geen lijn onder de laatste naam staat */
    p:last-child {
      border-bottom: none;
    }
  }
}
</style>
