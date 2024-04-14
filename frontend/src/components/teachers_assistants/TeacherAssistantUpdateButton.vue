<script setup lang="ts">
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import { useI18n } from 'vue-i18n';
import { type Course } from '@/types/Course.ts';
import { PrimeIcons } from 'primevue/api';
import TeacherAssistantSearch from './TeacherAssistantSearch.vue';
import { ref } from 'vue';
import { h } from 'vue';

/* Composable injections */
const { t } = useI18n();

/* Props */
const props = defineProps<{ course: Course }>();

/* Dialog state to select the course you want to create a project for */
const displayEdit = ref(false);

</script>

<template>
    <div>
        <!-- Button to edit the teachers/assistants of a course -->
        <Button
            :icon="PrimeIcons.PENCIL"
            icon-pos="right"
            class="custom-button"
            @click="displayEdit = true"
        />
        <!-- Dialog to display the teacher/assistant search -->
        <Dialog
            v-model:visible="displayEdit"
            class="m-3"
            :draggable="false"
            :contentStyle="{ 'width': '90vw', height: '90vh'}"
            modal
        >
            <template #header>
                <h2 class="my-3 text-primary">
                    {{ t('views.courses.teachers_and_assistants.search.title') }}
                </h2>
            </template>
            <template #default>
                <TeacherAssistantSearch :course="props.course" />
            </template>
        </Dialog>
    </div>
</template>

<style scoped lang="scss"></style>
