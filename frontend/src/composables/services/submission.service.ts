import { Submission } from '@/types/submission/Submission.ts';
import { type Ref, ref, type UnwrapRef } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { get, getList, deleteId, create } from '@/composables/services/helpers.ts';

interface SubmissionState {
    submissions: Ref<Submission[] | null>;
    submission: Ref<Submission | null>;
    getSubmissionByID: (id: string, selfprocessError?: boolean) => Promise<void>;
    getSubmissionByProject: (projectId: string, selfprocessError?: boolean) => Promise<void>;
    getSubmissionByGroup: (groupId: string, selfprocessError?: boolean) => Promise<void>;
    createSubmission: (submissionData: UnwrapRef<File[]>, groupId: string, selfprocessError?: boolean) => Promise<void>;
    deleteSubmission: (id: string, selfprocessError?: boolean) => Promise<void>;
}

export function useSubmission(): SubmissionState {
    const submissions = ref<Submission[] | null>(null);
    const submission = ref<Submission | null>(null);

    async function getSubmissionByID(id: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.submissions.retrieve.replace('{id}', id);
        await get<Submission>(endpoint, submission, Submission.fromJSON, selfprocessError);
    }

    async function getSubmissionByProject(projectId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.submissions.byProject.replace('{projectId}', projectId);
        await getList<Submission>(endpoint, submissions, Submission.fromJSON, selfprocessError);
    }

    async function getSubmissionByGroup(groupId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.submissions.byGroup.replace('{groupId}', groupId);
        await getList<Submission>(endpoint, submissions, Submission.fromJSON, selfprocessError);
    }

    async function createSubmission(
        uploadedFiles: File[],
        groupId: string,
        selfprocessError: boolean = true,
    ): Promise<void> {
        const endpoint = endpoints.submissions.byGroup.replace('{groupId}', groupId);
        // formData is necessary with multiform data (otherwise files value is changed to files[] by axios)
        const formData = new FormData();
        uploadedFiles.forEach((file: File) => {
            formData.append('files', file); // Gebruik 'files' in plaats van 'files[]'
        });
        await create(
            endpoint,
            formData,
            submission,
            Submission.fromJSONCreate,
            'multipart/form-data',
            selfprocessError,
        );
    }

    async function deleteSubmission(id: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.submissions.retrieve.replace('{id}', id);
        await deleteId<Submission>(endpoint, submission, Submission.fromJSON, selfprocessError);
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
