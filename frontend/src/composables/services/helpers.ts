import axios from 'axios';
import {Ref} from 'vue';

export function get<T>(endpoint: string, ref: Ref<T|null>, fromJson: (data: any) => T): void {
    axios.get(endpoint).then(response =>
        ref.value = fromJson(response.data)
    ).catch(error => {
        console.log(error.data);
    });
}

export function getList<T>(endpoint: string, ref: Ref<T[]|null>, fromJson: (data: any) => T): void {
    axios.get(endpoint).then(response =>
        ref.value = response.data.map((data: T) => fromJson(data))
    ).catch(error => {
        console.log(error.data);
    });
}