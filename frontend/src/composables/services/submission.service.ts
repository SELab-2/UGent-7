import {Submission} from '@/types/Submission.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList } from '@/composables/services/helpers.ts';

export function useSubmission() {
    const submissions = ref<Submission[]|null>(null);
    const submission = ref<Submission|null>(null);

    async function getSubmissionByID(id: number) {
        const endpoint = endpoints.submissions.retrieve.replace('{id}', id.toString());
        get<Submission>(endpoint, submission, Submission.fromJSON);
        console.log(submission)
    }

    async function getSubmissionByProject(project_id: number) {
        const endpoint = endpoints.submissions.byProject.replace('{project_id}', project_id.toString());
        getList<Submission>(endpoint, submissions, Submission.fromJSON);
        console.log(submissions.value ? submissions.value.map((submission, index) => `Submission ${index + 1}: ${JSON.stringify(submission)}`) : 'Submission is null');
    }

    async function getSubmissionByGroup(group_id: number) {
        const endpoint = endpoints.submissions.byGroup.replace('{group_id}', group_id.toString());
        getList<Submission>(endpoint, submissions, Submission.fromJSON);
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