import {Submission} from '@/types/Submission.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';
import {ComposerTranslation} from "vue-i18n";

export function useSubmission() {
    const submissions = ref<Submission[]|null>(null);
    const submission = ref<Submission|null>(null);
    const toast = useToast();

    async function getSubmissionByID(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.submissions.retrieve.replace('{id}', id);
        get<Submission>(endpoint, submission, Submission.fromJSON, toast, t);
    }

    async function getSubmissionByProject(project_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.submissions.byProject.replace('{project_id}', project_id);
        getList<Submission>(endpoint, submissions, Submission.fromJSON, toast, t);
    }

    async function getSubmissionByGroup(group_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.submissions.byGroup.replace('{group_id}', group_id);
        getList<Submission>(endpoint, submissions, Submission.fromJSON, toast, t);
    }

    async function createSubmission(submission_data: any, group_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.submissions.byGroup.replace('{group_id}', group_id);
        create<Submission>(endpoint, submission_data, submission, Submission.fromJSON, toast, t);
    }

    async function deleteSubmission(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.submissions.retrieve.replace('{id}', id);
        delete_id<Submission>(endpoint, submission, Submission.fromJSON, toast, t);
    }

    return {
        submissions,
        submission,
        getSubmissionByID,
        getSubmissionByProject,
        getSubmissionByGroup,

        createSubmission,
        deleteSubmission
    };
}