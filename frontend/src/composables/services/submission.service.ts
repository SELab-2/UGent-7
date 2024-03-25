import {Submission} from '@/types/Submission.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';
import {ComposerTranslation} from "vue-i18n";

export function useSubmission() {
    const submissions = ref<Submission[]|null>(null);
    const submission = ref<Submission|null>(null);
    const toast = useToast();

    async function getSubmissionByID(id: number, t: ComposerTranslation) {
        const endpoint = endpoints.submissions.retrieve.replace('{id}', id.toString());
        get<Submission>(endpoint, submission, Submission.fromJSON, toast, t);
        console.log(submission)
    }

    async function getSubmissionByProject(project_id: number, t: ComposerTranslation) {
        const endpoint = endpoints.submissions.byProject.replace('{project_id}', project_id.toString());
        getList<Submission>(endpoint, submissions, Submission.fromJSON, toast, t);
        console.log(submissions.value ? submissions.value.map((submission, index) => `Submission ${index + 1}: ${JSON.stringify(submission)}`) : 'Submission is null');
    }

    async function getSubmissionByGroup(group_id: number, t: ComposerTranslation) {
        const endpoint = endpoints.submissions.byGroup.replace('{group_id}', group_id.toString());
        getList<Submission>(endpoint, submissions, Submission.fromJSON, toast, t);
        console.log(submissions.value ? submissions.value.map((submission, index) => `Submission ${index + 1}: ${JSON.stringify(submission)}`) : 'Submission is null');
    }

    return {
        submissions,
        submission,
        getSubmissionByID,
        getSubmissionByProject,
        getSubmissionByGroup
    };
}