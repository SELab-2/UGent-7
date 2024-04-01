import { Submission } from '@/types/Submission.ts'
import { ref } from 'vue'
import { endpoints } from '@/config/endpoints.ts'
import {
    get,
    getList,
    create,
    delete_id
} from '@/composables/services/helpers.ts'

export function useSubmission() {
    const submissions = ref<Submission[] | null>(null)
    const submission = ref<Submission | null>(null)

    async function getSubmissionByID(id: string) {
        const endpoint = endpoints.submissions.retrieve.replace('{id}', id)
        await get<Submission>(endpoint, submission, Submission.fromJSON)
    }

    async function getSubmissionByProject(project_id: string) {
        const endpoint = endpoints.submissions.byProject.replace(
            '{project_id}',
            project_id
        )
        await getList<Submission>(endpoint, submissions, Submission.fromJSON)
    }

    async function getSubmissionByGroup(group_id: string) {
        const endpoint = endpoints.submissions.byGroup.replace(
            '{group_id}',
            group_id
        )
        await getList<Submission>(endpoint, submissions, Submission.fromJSON)
    }

    async function createSubmission(
        submission_data: Submission,
        group_id: string
    ) {
        const endpoint = endpoints.submissions.byGroup.replace(
            '{group_id}',
            group_id
        )
        await create<Submission>(
            endpoint,
            {
                files: submission_data.files // TODO look how this will need to be given
            },
            submission,
            Submission.fromJSON
        )
    }

    async function deleteSubmission(id: string) {
        const endpoint = endpoints.submissions.retrieve.replace('{id}', id)
        await delete_id<Submission>(endpoint, submission, Submission.fromJSON)
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
