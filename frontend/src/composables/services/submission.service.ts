import { Submission } from '@/types/submission/Submission.ts';
import { type Ref, ref, type UnwrapRef } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { get, getList, deleteId, create } from '@/composables/services/helpers.ts';

interface SubmissionState {
    submissions: Ref<Submission[] | null>;
    submission: Ref<Submission | null>;
    getSubmissionByID: (id: string) => Promise<void>;
    getSubmissionByProject: (projectId: string) => Promise<void>;
    getSubmissionByGroup: (groupId: string) => Promise<void>;
    createSubmission: (submissionData: UnwrapRef<File[]>, groupId: string) => Promise<void>;
    deleteSubmission: (id: string) => Promise<void>;
}

export function useSubmission(): SubmissionState {
    const submissions = ref<Submission[] | null>(null);
    const submission = ref<Submission | null>(null);

    async function getSubmissionByID(id: string): Promise<void> {
        const endpoint = endpoints.submissions.retrieve.replace('{id}', id);
        await get<Submission>(endpoint, submission, Submission.fromJSON);
    }

    async function getSubmissionByProject(projectId: string): Promise<void> {
        const endpoint = endpoints.submissions.byProject.replace('{projectId}', projectId);
        await getList<Submission>(endpoint, submissions, Submission.fromJSON);
    }

    async function getSubmissionByGroup(groupId: string): Promise<void> {
        const endpoint = endpoints.submissions.byGroup.replace('{groupId}', groupId);
        await getList<Submission>(endpoint, submissions, Submission.fromJSON);
    }

    async function createSubmission(uploadedFiles: File[], groupId: string): Promise<void> {
        const endpoint = endpoints.submissions.byGroup.replace('{groupId}', groupId);
        await create(endpoint, uploadedFiles, submission, Submission.fromJSONCreate, 'multipart/form-data');
    }

    async function deleteSubmission(id: string): Promise<void> {
        const endpoint = endpoints.submissions.retrieve.replace('{id}', id);
        await deleteId<Submission>(endpoint, submission, Submission.fromJSON);
    }

    return {
        submissions,
        submission,
        getSubmissionByID,
        getSubmissionByProject,
        getSubmissionByGroup,

        createSubmission,
        deleteSubmission,
    };
}
