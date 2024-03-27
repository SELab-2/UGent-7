import axios, { AxiosError, AxiosResponse } from 'axios';
// import { useI18n } from 'vue-i18n';
import {Ref} from 'vue';
import {ComposerTranslation} from "vue-i18n";
const lifeTime = 3000;

// const { t } = useI18n();

export async function get<T>(endpoint: string, ref: Ref<T|null>, fromJson: (data: any) => T, toast:any, t: ComposerTranslation): Promise<void> {
    await axios.get(endpoint).then((response: AxiosResponse) => {
        ref.value = fromJson(response.data);
        //toast.add({severity: "success", summary: "Success Message", detail: "Order submitted", life: lifeTime});
    }).catch((error: AxiosError) => {
        processError(error, toast, t);
        console.error(error); // Log the error for debugging
    });
}

export async function create<T>(endpoint: string, data:any, ref: Ref<T|null>, fromJson: (data: any) => T, toast:any,  t: ComposerTranslation): Promise<void> {
    const headers = {
        // TODO change this to your token
        Authorization: "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyODQwMjY1LCJpYXQiOjE3MTEzMDQyNjUsImp0aSI6ImQwYTgxY2YxMzU5NTQ4OWQ4OGNiZDFmZmZiMGI0MmJhIiwidXNlcl9pZCI6IjAwMDIwMTI0NzAxMSJ9.izGK0MStcMiPkOAWs0wgWsYEs0_5S1WvsleWaIcttnk"
    };
    await axios.post(endpoint, data, { headers }).then((response: AxiosResponse) => {
        ref.value = fromJson(response.data);
        //toast.add({severity: "success", summary: "Success Message", detail: "Order submitted", life: lifeTime});
    }).catch((error: AxiosError) => {
        processError(error, toast, t);
        console.error(error); // Log the error for debugging
    });
}

export async function delete_id<T>(endpoint: string, ref: Ref<T|null>, fromJson: (data: any) => T, toast:any, t: ComposerTranslation): Promise<void> {
    const headers = {
        // TODO change this to your token
        Authorization: "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyODQwMjY1LCJpYXQiOjE3MTEzMDQyNjUsImp0aSI6ImQwYTgxY2YxMzU5NTQ4OWQ4OGNiZDFmZmZiMGI0MmJhIiwidXNlcl9pZCI6IjAwMDIwMTI0NzAxMSJ9.izGK0MStcMiPkOAWs0wgWsYEs0_5S1WvsleWaIcttnk"
    };
    await axios.delete(endpoint,{ headers }).then((response: AxiosResponse) => {
        ref.value = fromJson(response.data);
        //toast.add({severity: "success", summary: "Success Message", detail: "Order submitted", life: lifeTime});
    }).catch((error: AxiosError) => {
        processError(error, toast, t);
        console.error(error); // Log the error for debugging
    });
}

export async function delete_id_with_data<T>(endpoint: string, data: any, ref: Ref<T|null>, fromJson: (data: any) => T, toast:any, t: ComposerTranslation): Promise<void> {
    const headers = {
        // TODO change this to your token
        Authorization: "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyODQwMjY1LCJpYXQiOjE3MTEzMDQyNjUsImp0aSI6ImQwYTgxY2YxMzU5NTQ4OWQ4OGNiZDFmZmZiMGI0MmJhIiwidXNlcl9pZCI6IjAwMDIwMTI0NzAxMSJ9.izGK0MStcMiPkOAWs0wgWsYEs0_5S1WvsleWaIcttnk"
    };
    await axios.delete(endpoint,{ headers, data }).then((response: AxiosResponse) => {
        ref.value = fromJson(response.data);
        //toast.add({severity: "success", summary: "Success Message", detail: "Order submitted", life: lifeTime});
    }).catch((error: AxiosError) => {
        processError(error, toast, t);
        console.error(error); // Log the error for debugging
    });
}


export async function getList<T>(endpoint: string, ref: Ref<T[]|null>, fromJson: (data: any) => T, toast:any,  t: ComposerTranslation): Promise<void> {
    await axios.get(endpoint).then(response => {
        ref.value = response.data.map((data: T) => fromJson(data));
        //toast.add({severity: "success", summary: "Success Message", detail: "Order submitted", life: lifeTime});
    }
    ).catch((error: AxiosError) => {
        processError(error, toast, t);
        console.error(error); // Log the error for debugging
    });
}

export async function getListMerged<T>(endpoints: string[], ref: Ref<T[]|null>, fromJson: (data: any) => T, toast:any, t: ComposerTranslation): Promise<void> {

    // Create an array to accumulate all response data
    const allData: T[] = [];

    for (const endpoint of endpoints){
        console.log(endpoint)
        await axios.get(endpoint).then(response => {
            const responseData: T[] = response.data.map((data: T) => fromJson(data));
            allData.push(...responseData); // Merge into the allData array
            // toast.add({severity: "success", summary: "Success Message", detail: "Order submitted", life: lifeTime});
        }
        ).catch((error: AxiosError) => {
            processError(error, toast, t);
            console.error(error); // Log the error for debugging
        });
    }
    ref.value = allData;
}

export function processError(error: AxiosError, toast:any, t: ComposerTranslation){
    if (error.response) {
        console.log(error.response.status);
        // The request was made and the server responded with a status code
        if (error.response.status === 404) {
            toast.add({ severity: 'error', summary: t('composables.helpers.errors.notFound'), detail: t('composables.helpers.errors.notFoundDetail'), life: lifeTime });
        } else if (error.response.status === 401) {
            toast.add({ severity: 'error', summary: t('composables.helpers.errors.unauthorized'), detail: t('composables.helpers.errors.unauthorizedDetail'), life: lifeTime });
        } else {
            toast.add({ severity: 'error', summary: t('composables.helpers.errors.server'), detail: t('composables.helpers.errors.serverDetail'), life: lifeTime });
        }
    } else if (error.request) {
        // The request was made but no response was received
        toast.add({ severity: 'error', summary: t('composables.helpers.errors.network'), detail: t('composables.helpers.errors.networkDetail'), life: lifeTime });
    } else {
        // Something happened in setting up the request that triggered an error
        toast.add({ severity: 'error', summary: t('composables.helpers.errors.request'), detail: t('composables.helpers.errors.requestDetail'), life: lifeTime });
    }
}