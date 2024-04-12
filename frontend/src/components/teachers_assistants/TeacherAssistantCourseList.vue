<script setup lang="ts">
import TeacherAssistantList from './TeacherAssistantList.vue';
import { type Course } from '@/types/Course';
import { type User } from '@/types/users/User.ts';
import { useTeacher } from '@/composables/services/teachers.service';
import { useAssistant } from '@/composables/services/assistant.service';
import { onMounted, ref } from 'vue';

/* Props */
interface Props {
    course: Course | null;
    cols?: number;
}

const props = withDefaults(defineProps<Props>(), {
    cols: 4,
    course: null,
});

/* Composable injections */
const { teachers, getTeacherByCourse } = useTeacher();
const { assistants, getAssistantByCourse } = useAssistant();
const allUsers = ref<User[]>([]);

/* Methods */
onMounted(async () => {
    if (props.course !== null) {
        await getTeacherByCourse(props.course.id);
        await getAssistantByCourse(props.course.id);

        if (teachers.value !== null){
            allUsers.value.push(...teachers.value);
        }
        if (assistants.value !== null){
            allUsers.value.push(...assistants.value);
        }
    }
});
</script>

<template>
    <TeacherAssistantList :users="allUsers" :cols="props.cols" />
</template>

<style scoped lang="scss"></style>
