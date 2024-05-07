<script setup lang="ts">
import Button from 'primevue/button';
import { useI18n } from 'vue-i18n';
import { useGroup } from '@/composables/services/group.service.ts';
import { useStudents } from '@/composables/services/student.service.ts';
import { type Project } from '@/types/Project.ts';

/* Props */
const props = defineProps<{
    project: Project;
}>();

/* Injections */
const { t } = useI18n();
const { groups, getGroupsByProject } = useGroup();
const { students, getStudentsByGroup } = useStudents();

/* Constants */
const header = 'OrgDefinedId,Last Name,First Name,Email,Grade,End-of-Line Indicator\n';

/* Functions */
/**
 * generateCSVAndDownload generates a csv combining all the scores for all students in all groups associated
 * with the projectId in this component's props.
 * After generating a csv, a download link is created and clicked.
 */
const generateCSVAndDownload = async (): Promise<void> => {
    // retrieve all the groups associated with a given project
    await getGroupsByProject(props.project.id);
    // construct for every group's student a csv line according to ufora grade csv standard
    // and concatenate them all into one csv
    const csvPromises =
        groups.value?.map(async (group) => {
            await getStudentsByGroup(group.id);
            return (
                students.value
                    ?.map((student) => {
                        // single csv line
                        return `#${student.student_id},${student.last_name},${student.first_name},${student.email},${(group.score * 10) / props.project.max_score},#`;
                    })
                    .join('\n') ?? ''
            );
        }) ?? [];

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
    <Button @click="generateCSVAndDownload">
        {{ t('components.button.csv') }}
    </Button>
</template>

<style scoped lang="scss"></style>
