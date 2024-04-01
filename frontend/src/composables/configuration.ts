import { ref } from 'vue'
import { endpoints } from '../config/endpoints.ts'
import { environment } from '../config/environment.ts'

export function useConfig() {
    const config = ref({
        environment,
        endpoints
    })

    return { config }
}
