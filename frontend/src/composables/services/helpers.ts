import { type AxiosError, type AxiosResponse } from 'axios';
import { client } from '@/composables/axios.ts';
import { type Ref } from 'vue';
import { useMessagesStore } from '@/store/messages.store.ts';
import { i18n } from '../i18n';

const lifeTime = 3000;

export async function get<T>(endpoint: string, ref: Ref<T | null>, fromJson: (data: any) => T): Promise<void> {
    await client
        .get(endpoint)
        .then((response: AxiosResponse) => {
            ref.value = fromJson(response.data);
        })
        .catch((error: AxiosError) => {
            processError(error);
            console.error(error); // Log the error for debugging
        });
}

export async function create<T>(endpoint: string, data: any, ref: Ref<T | null>, fromJson: (data: any) => T): Promise<void> {
    await client
        .post(endpoint, data)
        .then((response: AxiosResponse) => {
            ref.value = fromJson(response.data);
        })
        .catch((error: AxiosError) => {
            processError(error);
            console.error(error); // Log the error for debugging
        });
}

export async function deleteId<T>(endpoint: string, ref: Ref<T | null>, fromJson: (data: any) => T): Promise<void> {
    await client
        .delete(endpoint)
        .then((response: AxiosResponse) => {
            ref.value = fromJson(response.data);
            // add({severity: "success", summary: "Success Message", detail: "Order submitted", life: lifeTime});
        })
        .catch((error: AxiosError) => {
            processError(error);
            console.error(error); // Log the error for debugging
        });
}

export async function deleteIdWithData<T>(endpoint: string, data: any, ref: Ref<T | null>, fromJson: (data: any) => T): Promise<void> {
    await client
        .delete(endpoint, { data })
        .then((response: AxiosResponse) => {
            ref.value = fromJson(response.data);
            // add({severity: "success", summary: "Success Message", detail: "Order submitted", life: lifeTime});
        })
        .catch((error: AxiosError) => {
            processError(error);
            console.error(error); // Log the error for debugging
        });
}

export async function getList<T>(endpoint: string, ref: Ref<T[] | null>, fromJson: (data: any) => T): Promise<void> {
    await client
        .get(endpoint)
        .then((response) => {
            ref.value = response.data.map((data: T) => fromJson(data));
            // add({severity: "success", summary: "Success Message", detail: "Order submitted", life: lifeTime});
        })
        .catch((error: AxiosError) => {
            processError(error);
            console.error(error); // Log the error for debugging
        });
}

export async function getListMerged<T>(endpoints: string[], ref: Ref<T[] | null>, fromJson: (data: any) => T): Promise<void> {
    // Create an array to accumulate all response data
    const allData: T[] = [];

    for (const endpoint of endpoints) {
        await client
            .get(endpoint)
            .then((response) => {
                const responseData: T[] = response.data.map((data: T) => fromJson(data));
                allData.push(...responseData); // Merge into the allData array
                // add({severity: "success", summary: "Success Message", detail: "Order submitted", life: lifeTime});
            })
            .catch((error: AxiosError) => {
                processError(error);
                console.error(error); // Log the error for debugging
            });
    }
    ref.value = allData;
}

export function processError(error: AxiosError): void {
    const { t } = i18n.global;
    const { add } = useMessagesStore();

    if (error.response !== undefined && error.response !== null) {
        // The request was made and the server responded with a status code
        if (error.response.status === 404) {
            add({
                severity: 'error',
                summary: t('composables.helpers.errors.notFound'),
                detail: t('composables.helpers.errors.notFoundDetail'),
                life: lifeTime,
            });
        } else if (error.response.status === 401) {
            add({
                severity: 'error',
                summary: t('composables.helpers.errors.unauthorized'),
                detail: t('composables.helpers.errors.unauthorizedDetail'),
                life: lifeTime,
            });
        } else {
            add({
                severity: 'error',
                summary: t('composables.helpers.errors.server'),
                detail: t('composables.helpers.errors.serverDetail'),
                life: lifeTime,
            });
        }
    } else if (error.request !== undefined && error.request !== null) {
        // The request was made but no response was received
        add({
            severity: 'error',
            summary: t('composables.helpers.errors.network'),
            detail: t('composables.helpers.errors.networkDetail'),
            life: lifeTime,
        });
    } else {
        // Something happened in setting up the request that triggered an error
        add({
            severity: 'error',
            summary: t('composables.helpers.errors.request'),
            detail: t('composables.helpers.errors.requestDetail'),
            life: lifeTime,
        });
    }
}
