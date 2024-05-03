<script setup lang="ts">
import Button from 'primevue/button';
import { ref } from "vue";
import { useI18n } from 'vue-i18n';
import { useGroup } from '@/composables/services/group.service.ts';


/* Props */
const props = defineProps<{
    projectId: string
    projectName: string
}>();

/* Injections */
const { t } = useI18n();
const { groups, getGroupsByProject } = useGroup();

/* State */
const csv_content = ref<string|undefined>(undefined);

/* Functions */
/**
 * generateCSVAndDownload generates a csv combining all the scores for all students in all groups associated
 * with the projectId in this component's props.
 * After generating a csv, a download link is created and clicked.
 */
const generateCSVAndDownload = async () => {
    // retrieve all the groups associated with a given project
    await getGroupsByProject(props.projectId);
    // construct for every group's student a csv line according to ufora grade csv standard
    // and concatenate them all into one csv
    csv_content.value = groups.value?.map(group => {
        return group.students?.map(student => {
            return `#${student.studentId},${student.last_name},${student.first_name},${student.email},${group.score},#`
        }).join('\n');
    }).join('\n');

    if (csv_content.value !== undefined) {
        // create a blob from the csv content
        const blob = new Blob([csv_content.value], {type: 'text/plain'})

        // create a download url for this blob
        const url = URL.createObjectURL(blob);

        // create an anchor element for downloading the file
        const a = document.createElement('a');
        a.href = url;
        a.download = (props.projectName ?? props.projectId) + '.scores';

        // click anchor element
        a.click();

        // clean up URL
        URL.revokeObjectURL(url);
    }
};
</script>

<template>
    <Button @click="generateCSVAndDownload">
        {{ t('components.button.csv') }}
    </Button>
</template>

<style scoped lang="scss"></style>
