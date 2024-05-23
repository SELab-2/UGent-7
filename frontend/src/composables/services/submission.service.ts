import { Submission } from '@/types/submission/Submission.ts';
import { type Ref, ref, type UnwrapRef } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { get, getList, deleteId, create } from '@/composables/services/helpers.ts';

interface SubmissionState {
    submissions: Ref<Submission[] | null>;
    submission: Ref<Submission | null>;
    getSubmissionByID: (id: string, selfProcessError?: boolean) => Promise<void>;
    getSubmissionByProject: (projectId: string, selfProcessError?: boolean) => Promise<void>;
    getSubmissionByGroup: (groupId: string, selfProcessError?: boolean) => Promise<void>;
    createSubmission: (submissionData: UnwrapRef<File[]>, groupId: string, selfProcessError?: boolean) => Promise<void>;
    deleteSubmission: (id: string, selfProcessError?: boolean) => Promise<void>;
}

export function useSubmission(): SubmissionState {
    const submissions = ref<Submission[] | null>(null);
    const submission = ref<Submission | null>(null);

    async function getSubmissionByID(id: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.submissions.retrieve.replace('{id}', id);
        await get<Submission>(endpoint, submission, Submission.fromJSON, selfProcessError);
    }

    async function getSubmissionByProject(projectId: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.submissions.byProject.replace('{projectId}', projectId);
        await getList<Submission>(endpoint, submissions, Submission.fromJSON, selfProcessError);
    }

    async function getSubmissionByGroup(groupId: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.submissions.byGroup.replace('{groupId}', groupId);
        await getList<Submission>(endpoint, submissions, Submission.fromJSON, selfProcessError);
    }

    async function createSubmission(
        uploadedFiles: File[],
        groupId: string,
        selfProcessError: boolean = true,
    ): Promise<void> {
        const endpoint = endpoints.submissions.byGroup.replace('{groupId}', groupId);

        // formData is necessary with multiform data (otherwise files value is changed to files[] by axios)
        const formData = new FormData();
        uploadedFiles.forEach((file: File) => {
            formData.append('files', file);
        });

        await create(endpoint, formData, submission, Submission.fromJSON, 'multipart/form-data', selfProcessError);
    }

    async function deleteSubmission(id: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.submissions.retrieve.replace('{id}', id);
        await deleteId<Submission>(endpoint, submission, Submission.fromJSON, selfProcessError);
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
