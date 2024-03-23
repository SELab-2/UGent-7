import axios, { AxiosError, AxiosResponse } from 'axios';
import {Ref} from 'vue';
import { useToast } from 'primevue/usetoast';

const lifeTime = 3000;

export function get<T>(endpoint: string, ref: Ref<T|null>, fromJson: (data: any) => T): void {
    const toast = useToast();

    axios.get(endpoint).then((response: AxiosResponse) => {
        ref.value = fromJson(response.data);
        // toast.add({severity: "success", summary: "Success Message", detail: "Order submitted", life: lifeTime});
    }).catch((error: AxiosError) => {
        processError(error, toast);
        console.error(error); // Log the error for debugging
    });
}

export function getList<T>(endpoint: string, ref: Ref<T[]|null>, fromJson: (data: any) => T): void {
    const toast = useToast();

    axios.get(endpoint).then(response => {
        ref.value = response.data.map((data: T) => fromJson(data));
        // toast.add({severity: "success", summary: "Success Message", detail: "Order submitted", life: lifeTime});
    }
    ).catch((error: AxiosError) => {
        processError(error, toast);
        console.error(error); // Log the error for debugging
    });
}

export function getListMerged<T>(endpoints: string[], ref: Ref<T[]|null>, fromJson: (data: any) => T): void {
    const toast = useToast();

    // Create an array to accumulate all response data
    const allData: T[] = [];

    for (const endpoint of endpoints){

        axios.get(endpoint).then(response => {
            const responseData: T[] = response.data.map((data: T) => fromJson(data));
            allData.push(...responseData); // Merge into the allData array
            // toast.add({severity: "success", summary: "Success Message", detail: "Order submitted", life: lifeTime});
        }
        ).catch((error: AxiosError) => {
            processError(error, toast);
            console.error(error); // Log the error for debugging
        });
    }
    ref.value = allData;
}

function processError(error: AxiosError, toast:any){
    if (error.response) {
        // The request was made and the server responded with a status code
        if (error.response.status === 404) {
            toast.add({ severity: 'error', summary: 'Not Found', detail: 'Resource not found.', life: lifeTime });
        } else if (error.response.status === 401) {
            toast.add({ severity: 'error', summary: 'Unauthorized', detail: 'You are not authorized to access this resource.', life: lifeTime });
        } else {
            toast.add({ severity: 'error', summary: 'Server Error', detail: 'An error occurred on the server.', life: lifeTime });
        }
    } else if (error.request) {
        // The request was made but no response was received
        toast.add({ severity: 'error', summary: 'Network Error', detail: 'Unable to connect to the server.', life: lifeTime });
    } else {
        // Something happened in setting up the request that triggered an error
        toast.add({ severity: 'error', summary: 'Request Error', detail: 'An error occurred while making the request.', life: lifeTime });
    }
}