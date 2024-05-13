import { DockerImage } from '@/types/DockerImage.ts';
import { Response } from '@/types/Response.ts';
import { endpoints } from '@/config/endpoints.ts';
import { type Ref, ref } from 'vue';
import { type Filter } from '@/types/filter/Filter.ts';
import { create, getList, getPaginatedList, patch, deleteId } from '@/composables/services/helpers.ts';
import { type PaginatorResponse } from '@/types/filter/Paginator.ts';

interface DockerImagesState {
    pagination: Ref<PaginatorResponse<DockerImage> | null>;
    dockerImages: Ref<DockerImage[] | null>;
    response: Ref<Response | null>;
    getDockerImages: () => Promise<void>;
    searchDockerImages: (filters: Filter, page: number, pageSize: number) => Promise<void>;
    patchDockerImage: (dockerData: DockerImage) => Promise<void>;
    createDockerImage: (dockerData: DockerImage, file: File) => Promise<void>;
    deleteDockerImage: (id: string) => Promise<void>;
}

export function useDockerImages(): DockerImagesState {
    const pagination = ref<PaginatorResponse<DockerImage> | null>(null);
    const dockerImages = ref<DockerImage[] | null>(null);
    const response = ref<Response | null>(null);

    async function getDockerImages(): Promise<void> {
        const endpoint = endpoints.dockerImages.index;
        await getList<DockerImage>(endpoint, dockerImages, DockerImage.fromJSON);
    }

    async function searchDockerImages(filters: Filter, page: number, pageSize: number): Promise<void> {
        const endpoint = endpoints.dockerImages.search;
        await getPaginatedList<DockerImage>(endpoint, filters, page, pageSize, pagination, DockerImage.fromJSON);
    }

    async function patchDockerImage(dockerData: DockerImage): Promise<void> {
        const endpoint = endpoints.dockerImages.patch.replace('{id}', dockerData.id);
        await patch(endpoint, { public: dockerData.public }, response);
    }

    async function createDockerImage(dockerData: DockerImage, file: File): Promise<void> {
        const endpoint = endpoints.dockerImages.index;
        await create<Response>(
            endpoint,
            {
                file,
                name: dockerData.name,
                public: dockerData.public,
            },
            response,
            Response.fromJSON,
            'multipart/form-data',
        );
    }

    async function deleteDockerImage(id: string): Promise<void> {
        const endpoint = endpoints.dockerImages.retrieve.replace('{id}', id);
        await deleteId<Response>(endpoint, response, Response.fromJSON);
    }

    return {
        pagination,
        dockerImages,
        response,

        getDockerImages,
        searchDockerImages,
        patchDockerImage,
        createDockerImage,
        deleteDockerImage,
    };
}
