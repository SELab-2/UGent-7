<script setup lang="ts">
import { useStudents } from '@/composables/services/students.service.ts'
import { onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

/**
 * This card lists all users in the group of a project
 */
const { students, getStudentsByGroup } = useStudents()
const { t } = useI18n()

/* Component props */

const props = defineProps<{
    groupId: string
}>()

onMounted(async () => {
    await getStudentsByGroup(props.groupId)
})
</script>

<template>
    <div>
        <div class="groupcard">
            <h2>{{ t('views.projects.groupMembers') }}</h2>
            <div>
                <p v-for="student in students" :key="student.id">
                    {{ student.first_name }} {{ student.last_name }}
                </p>
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss">
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
            margin-bottom: 0.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #e0e0e0;
        }

        /* Zorgt ervoor dat er geen lijn onder de laatste naam staat */
        p:last-child {
            border-bottom: none;
        }
    }
}
</style>
