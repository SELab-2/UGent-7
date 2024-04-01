import { Submission } from '@/types/Submission.ts'
import { ref } from 'vue'
import { endpoints } from '@/config/endpoints.ts'
import {
    get,
    getList,
    create,
    deleteId
} from '@/composables/services/helpers.ts'

export function useSubmission() {
    const submissions = ref<Submission[] | null>(null)
    const submission = ref<Submission | null>(null)

    async function getSubmissionByID(id: string) {
        const endpoint = endpoints.submissions.retrieve.replace('{id}', id)
        await get<Submission>(endpoint, submission, Submission.fromJSON)
    }

    async function getSubmissionByProject(projectId: string) {
        const endpoint = endpoints.submissions.byProject.replace(
            '{projectId}',
            projectId
        )
        await getList<Submission>(endpoint, submissions, Submission.fromJSON)
    }

    async function getSubmissionByGroup(groupId: string) {
        const endpoint = endpoints.submissions.byGroup.replace(
            '{groupId}',
            groupId
        )
        await getList<Submission>(endpoint, submissions, Submission.fromJSON)
    }

    async function createSubmission(
        submissionData: Submission,
        groupId: string
    ) {
        const endpoint = endpoints.submissions.byGroup.replace(
            '{groupId}',
            groupId
        )
        await create<Submission>(
            endpoint,
            {
                files: submissionData.files // TODO look how this will need to be given
            },
            submission,
            Submission.fromJSON
        )
    }

    async function deleteSubmission(id: string) {
        const endpoint = endpoints.submissions.retrieve.replace('{id}', id)
        await deleteId<Submission>(endpoint, submission, Submission.fromJSON)
    }

    return {
        submissions,
        submission,
        getSubmissionByID,
        getSubmissionByProject,
        getSubmissionByGroup,

        createSubmission,
        deleteSubmission
    }
}
