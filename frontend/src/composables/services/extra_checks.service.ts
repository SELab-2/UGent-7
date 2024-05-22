import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { create, deleteId, getList } from '@/composables/services/helpers.ts';
import { ExtraCheck } from '@/types/ExtraCheck';
import { Response } from '@/types/Response';

interface ExtraCheckState {
    extraCheck: Ref<ExtraCheck | null>;
    extraChecks: Ref<ExtraCheck[] | null>;
    getExtraChecksByProject: (projectId: string, selfprocessError?: boolean) => Promise<void>;
    addExtraCheck: (extraCheckData: ExtraCheck, projectId: string, selfprocessError?: boolean) => Promise<void>;
    setExtraChecks: (extraChecks: ExtraCheck[], projectId: string, selfprocessError?: boolean) => Promise<void>;
    deleteExtraCheck: (extraCheckId: string, selfprocessError?: boolean) => Promise<void>;
}

export function useExtraCheck(): ExtraCheckState {
    const extraCheck = ref<ExtraCheck | null>(null);
    const extraChecks = ref<ExtraCheck[] | null>(null);
    const response = ref<Response | null>(null);

    async function getExtraChecksByProject(projectId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.extraChecks.byProject.replace('{projectId}', projectId);
        await getList<ExtraCheck>(endpoint, extraChecks, ExtraCheck.fromJSON, selfprocessError);
    }

    async function addExtraCheck(
        extraCheckData: ExtraCheck,
        projectId: string,
        selfprocessError: boolean = true,
    ): Promise<void> {
        const endpoint = endpoints.extraChecks.byProject.replace('{projectId}', projectId);
        await create<ExtraCheck>(
            endpoint,
            {
                name: extraCheckData.name,
                docker_image: extraCheckData.docker_image?.id,
                file: extraCheckData.file,
                time_limit: extraCheckData.time_limit,
                memory_limit: extraCheckData.memory_limit,
                show_log: extraCheckData.show_log,
            },
            extraCheck,
            ExtraCheck.fromJSON,
            'multipart/form-data',
            selfprocessError,
        );
    }

    async function setExtraChecks(extraChecks: ExtraCheck[], projectId: string, selfprocessError: boolean = true): Promise<void> {
        for (const extraCheck of extraChecks) {
            if (extraCheck.id === '') {
                await addExtraCheck(extraCheck, projectId, selfprocessError);
            }
        }
    }

    async function deleteExtraCheck(extraCheckId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.extraChecks.retrieve.replace('{id}', extraCheckId);
        await deleteId(endpoint, response, Response.fromJSON, selfprocessError);
    }

    return {
        extraCheck,
        extraChecks,

        getExtraChecksByProject,
        addExtraCheck,
        setExtraChecks,
        deleteExtraCheck,
    };
}
