<script setup lang="ts">
import Skeleton from 'primevue/skeleton';
import { type User } from '@/types/users/User.ts';
import { type Course } from '@/types/Course.ts';
import TeacherAssistantCard from './TeacherAssistantCard.vue';

/* Props */
interface Props {
    users: User[] | null;
    course: Course;
    cols?: number;
    detail?: boolean;
}

withDefaults(defineProps<Props>(), {
    cols: 4,
    detail: true,
});

</script>

<template>
    <div class="grid align-items-stretch">
        <template v-if="users !== null">
            <template v-if="users.length > 0">
                <div
                    class="col-12 md:col-6 lg:col-4"
                    :class="'xl:col-' + 12 / cols"
                    v-for="user in users"
                    :key="user.id"
                >
                    <TeacherAssistantCard class="h-full" :userValue="user" :course="course" :detail="detail" />
                </div>
            </template>
        </template>
        <template v-else>
            <div class="col-12 md:col-6 lg:col-4" :class="'xl:col-' + 12 / cols" v-for="index in cols" :key="index">
                <Skeleton :height="'10rem'" />
            </div>
        </template>
    </div>
</template>

<style scoped lang="scss"></style>
