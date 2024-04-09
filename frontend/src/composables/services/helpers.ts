import { type AxiosError } from 'axios';
import { client } from '@/config/axios.ts';
import { type Ref } from 'vue';
import { useMessagesStore } from '@/store/messages.store.ts';
import { i18n } from '@/config/i18n.ts';
import { type PaginatorResponse } from '@/types/filter/Paginator.ts';
import { type Filter } from '@/types/filter/Filter.ts';

/**
 * Get an item given its ID.
 *
 * @param endpoint
 * @param ref
 * @param fromJson
 */
export async function get<T>(endpoint: string, ref: Ref<T | null>, fromJson: (data: any) => T): Promise<void> {
    try {
        const response = await client.get(endpoint);
        ref.value = fromJson(response.data);
    } catch (error: any) {
        processError(error);
        console.error(error); // Log the error for debugging
        throw error; // Re-throw the error to the caller
    }
}

/**
 * Create an item.
 *
 * @param endpoint
 * @param data
 * @param ref
 * @param fromJson
 */
export async function create<T>(
    endpoint: string,
    data: any,
    ref: Ref<T | null>,
    fromJson: (data: any) => T,
    contentType: string = 'application/json',
): Promise<void> {
    try {
        const response = await client.post(endpoint, data, {
            headers: {
                'Content-Type': contentType,
            },
        });
        ref.value = fromJson(response.data);
    } catch (error: any) {
        processError(error);
        console.error(error); // Log the error for debugging
        throw error; // Re-throw the error to the caller
    }
}

/**
 * Delete an item given its ID.
 *
 * @param endpoint
 * @param ref
 * @param fromJson
 */
export async function deleteId<T>(endpoint: string, ref: Ref<T | null>, fromJson: (data: any) => T): Promise<void> {
    try {
        const response = await client.delete(endpoint);
        ref.value = fromJson(response.data);
    } catch (error: any) {
        processError(error);
        console.error(error); // Log the error for debugging
        throw error; // Re-throw the error to the caller
    }
}

/**
 * Delete an item.
 *
 * @param endpoint
 * @param data
 * @param ref
 * @param fromJson
 */
export async function deleteIdWithData<T>(
    endpoint: string,
    data: any,
    ref: Ref<T | null>,
    fromJson: (data: any) => T,
): Promise<void> {
    try {
        const response = await client.delete(endpoint, { data });
        ref.value = fromJson(response.data);
    } catch (error: any) {
        processError(error);
        console.error(error); // Log the error for debugging
        throw error; // Re-throw the error to the caller
    }
}

/**
 * Get a list of items.
 *
 * @param endpoint
 * @param ref
 * @param fromJson
 */
export async function getList<T>(endpoint: string, ref: Ref<T[] | null>, fromJson: (data: any) => T): Promise<void> {
    try {
        const response = await client.get(endpoint);
        ref.value = response.data.map((data: T) => fromJson(data));
    } catch (error: any) {
        processError(error);
        console.error(error); // Log the error for debugging
        ref.value = []; // Set the ref to an empty array
        throw error; // Re-throw the error to the caller
    }
}

/**
 * Get a paginated list of items.
 *
 * @param endpoint
 * @param filters
 * @param page
 * @param pageSize
 * @param pagination
 * @param fromJson
 */
export async function getPaginatedList<T>(
    endpoint: string,
    filters: Filter,
    page: number,
    pageSize: number,
    pagination: Ref<PaginatorResponse<T> | null>,
    fromJson: (data: any) => T,
): Promise<void> {
    try {
        const response = await client.get(endpoint, {
            params: {
                ...filters,
                page,
                page_size: pageSize,
            },
        });

        pagination.value = {
            ...response.data,
            results: response.data.results.map((data: T) => fromJson(data)),
        };
    } catch (error: any) {
        processError(error);
        console.error(error); // Log the error for debugging

        pagination.value = {
            // Set the ref to an empty array
            ...error.data,
            count: 0,
            results: [],
        };

        throw error; // Re-throw the error to the caller
    }
}

/**
 * Get a list of items from multiple endpoints and merge them into a single list.
 *
 * @param endpoints
 * @param ref
 * @param fromJson
 */
export async function getListMerged<T>(
    endpoints: string[],
    ref: Ref<T[] | null>,
    fromJson: (data: any) => T,
): Promise<void> {
    // Create an array to accumulate all response data
    const allData: T[] = [];

    for (const endpoint of endpoints) {
        try {
            const response = await client.get(endpoint);
            const responseData: T[] = response.data.map((data: T) => fromJson(data));
            allData.push(...responseData); // Merge into the allData array
        } catch (error: any) {
            processError(error);
            console.error(error); // Log the error for debugging
            ref.value = []; // Set the ref to an empty array
            throw error; // Re-throw the error to the caller
        }
    }

    ref.value = allData;
}

/**
 * Process an error and display a message to the user.
 *
 * @param error
 */
export function processError(error: any): void {
    const { t } = i18n.global;
    const { addErrorMessage } = useMessagesStore();

    // Cast the error to an AxiosError
    error = error as AxiosError;

    if (error.response !== undefined && error.response !== null) {
        // The request was made and the server responded with a status code
        const status = error.response.status;

        if (status === 404) {
            addErrorMessage(t('composables.helpers.errors.notFound'), t('composables.helpers.errors.notFoundDetail'));
        } else if (error.response.status === 401 || error.response.status === 403) {
            addErrorMessage(
                t('composables.helpers.errors.unauthorized'),
                t('composables.helpers.errors.unauthorizedDetail'),
            );
        } else {
            const response = error.response.data;

            for (const key in response) {
                let message: string = response[key];

                if (Array.isArray(response[key])) {
                    message = response[key].join(', ');
                }

                addErrorMessage(t('composables.helpers.errors.server'), message);
            }
        }
    } else if (error.request !== undefined && error.request !== null) {
        // The request was made but no response was received
        addErrorMessage(t('composables.helpers.errors.network'), t('composables.helpers.errors.networkDetail'));
    } else {
        // Something happened in setting up the request that triggered an error
        addErrorMessage(t('composables.helpers.errors.request'), t('composables.helpers.errors.requestDetail'));
    }
}
