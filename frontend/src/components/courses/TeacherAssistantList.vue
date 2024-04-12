<script setup lang="ts">
import Skeleton from 'primevue/skeleton';
import { type Course } from '@/types/Course';
import TeacherAssistantCard from './TeacherAssistantCard.vue';
import { useTeacher } from '@/composables/services/teachers.service';
import { useAssistant } from '@/composables/services/assistant.service';
import { onMounted } from 'vue';

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

/* Methods */
onMounted(async () => {
    if (props.course !== null) {
        await getTeacherByCourse(props.course.id);
        await getAssistantByCourse(props.course.id);
    }
});
</script>

<template>
    <div class="grid align-items-stretch">
        <template v-if="teachers !== null && assistants !== null">
            <template v-if="teachers.length > 0 || assistants.length > 0">
                <div
                    class="col-12 md:col-6 lg:col-4"
                    :class="'xl:col-' + 12 / cols"
                    v-for="teacher in teachers"
                    :key="teacher.id"
                >
                    <TeacherAssistantCard class="h-full" :user="teacher" role="types.roles.teacher" />
                </div>

                <div
                    class="col-12 md:col-6 lg:col-4"
                    :class="'xl:col-' + 12 / cols"
                    v-for="assistant in assistants"
                    :key="assistant.id"
                >
                    <TeacherAssistantCard class="h-full" :user="assistant" role="types.roles.assistant" />
                </div>
            </template>
        </template>
        <template v-else>
            <div class="col-12 md:col-6 lg:col-4" :class="'xl:col-' + 12 / cols" v-for="index in cols" :key="index">
                <Skeleton :height="'25rem'" />
            </div>
        </template>
    </div>
</template>

<style scoped lang="scss"></style>
