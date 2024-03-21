/*
import axios from 'axios';

export function get<T extends Model>(path: string, ref: Ref<T>): void {
    axios.get(path).then(response =>
        ref.value = ref.fromJSON(response.data)
    ).catch(error => {
        console.log(error.data);
    });
}
*/