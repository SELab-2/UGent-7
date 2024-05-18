import { Submission } from '@/types/submission/Submission.ts';
import { type Ref, ref, type UnwrapRef } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { i18n } from '@/config/i18n.ts';
import { get, getList, deleteId, create } from '@/composables/services/helpers.ts';
import { useMessagesStore } from '@/store/messages.store.ts';

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
        const { t } = i18n.global;
        const { addSuccessMessage } = useMessagesStore();

        const endpoint = endpoints.submissions.byGroup.replace('{groupId}', groupId);
        // formData is necessary with multiform data (otherwise files value is changed to files[] by axios)
        const formData = new FormData();
        uploadedFiles.forEach((file: File) => {
            formData.append('files', file); // Gebruik 'files' in plaats van 'files[]'
        });
        try {
            await create(endpoint, formData, submission, Submission.fromJSONCreate, 'multipart/form-data');
            addSuccessMessage(t('toasts.messages.success'), t('toasts.messages.submissions.create.success'));
        } catch {}
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
