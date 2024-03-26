import {Submission} from '@/types/Submission.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';

export function useSubmission() {
    const submissions = ref<Submission[]|null>(null);
    const submission = ref<Submission|null>(null);
    const toast = useToast();

    async function getSubmissionByID(id: string) {
        const endpoint = endpoints.submissions.retrieve.replace('{id}', id);
        get<Submission>(endpoint, submission, Submission.fromJSON, toast);
    }

    async function getSubmissionByProject(project_id: string) {
        const endpoint = endpoints.submissions.byProject.replace('{project_id}', project_id);
        getList<Submission>(endpoint, submissions, Submission.fromJSON, toast);
    }

    async function getSubmissionByGroup(group_id: string) {
        const endpoint = endpoints.submissions.byGroup.replace('{group_id}', group_id);
        getList<Submission>(endpoint, submissions, Submission.fromJSON, toast);
    }

    async function createSubmission(submission_data: any, group_id: string) {
        const endpoint = endpoints.submissions.byGroup.replace('{group_id}', group_id);
        create<Submission>(endpoint, submission_data, submission, Submission.fromJSON, toast);
    }

    async function deleteSubmission(id: string) {
        const endpoint = endpoints.submissions.retrieve.replace('{id}', id);
        delete_id<Submission>(endpoint, submission, Submission.fromJSON, toast);
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