<script setup lang="ts">
import Button from 'primevue/button';
import { useI18n } from 'vue-i18n';
import { useStudents } from '@/composables/services/student.service.ts';
import { type Project } from '@/types/Project.ts';
import { type Group } from '@/types/Group.ts';
import { type Student } from '@/types/users/Student.ts';

/* Props */
const props = defineProps<{
    project: Project;
    groups: Group[];
}>();

/* Injections */
const { t } = useI18n();
const { students, getStudentsByGroup } = useStudents();

/* Constants */
const header = 'OrgDefinedId,Last Name,First Name,Email,Grade,End-of-Line Indicator\n';

/**
 * generateCSVAndDownload generates a csv combining all the scores for all students in all groups associated
 * with the projectId in this component's props.
 * After generating a csv, a download link is created and clicked.
 */
const generateCSVAndDownload = async (): Promise<void> => {
    // construct for every group's student a csv line according to Ufora grade csv standard
    // and concatenate them all into one csv
    const csvPromises = props.groups.map(async (group: Group) => {
        await getStudentsByGroup(group.id);

        if (students.value !== null) {
            return students.value
                .map((student: Student) => {
                    return `#${student.student_id},${student.last_name},${student.first_name},${student.email},${((group.score ?? 0) * 10) / props.project.max_score},#`;
                })
                .join('\n');
        }

        return [];
    });

    const csvList = await Promise.all(csvPromises);
    const csvContent = header + csvList.join('\n');

    // create a blob from the csv content
    const blob = new Blob([csvContent], { type: 'text/plain' });

    // create a download url for this blob
    const url = URL.createObjectURL(blob);

    // create an anchor element for downloading the file
    const a = document.createElement('a');
    a.href = url;
    a.download = props.project.name + '.csv';

    // click anchor element
    a.click();

    // clean up URL
    URL.revokeObjectURL(url);
};
</script>

<template>
    <Button @click="generateCSVAndDownload" :label="t('components.button.csv')" />
</template>

<style scoped lang="scss"></style>
