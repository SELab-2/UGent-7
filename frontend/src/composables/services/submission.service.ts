import {Submission} from '@/types/Submission.ts';
import {ref} from 'vue';
import axios from 'axios';
import {endpoints} from '@/config/endpoints.ts';

export function useSubmission() {
    const submissions = ref<Submission[]|null>(null);
    const submission = ref<Submission|null>(null);

    async function getSubmissionByID(id: number) {
        const endpoint = endpoints.submissions.retrieve.replace('{id}', id.toString());

        axios.get(endpoint).then(response => {
            submission.value = Submission.fromJSON(response.data);
        }).catch(error => {
            console.log(error.data);
        });

        console.log(submission)
    }

    async function getSubmissionByProject(project_id: number) {
        const endpoint = endpoints.submissions.byProject.replace('{project_id}', project_id.toString());

        axios.get(endpoint).then(response => {
            submissions.value = response.data.map((submissionData: Submission) => Submission.fromJSON(submissionData));
        }).catch(error => {
            console.log(error.data);
        });

        console.log(submissions.value ? submissions.value.map((submission, index) => `Submission ${index + 1}: ${JSON.stringify(submission)}`) : 'Submission is null');
    }

    async function getSubmissionByGroup(group_id: number) {
        const endpoint = endpoints.submissions.byGroup.replace('{group_id}', group_id.toString());

        axios.get(endpoint).then(response => {
            submissions.value = response.data.map((submissionData: Submission) => Submission.fromJSON(submissionData));
        }).catch(error => {
            console.log(error.data);
        });

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