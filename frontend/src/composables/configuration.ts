import { type Ref, ref } from 'vue'
import { endpoints } from '../config/endpoints.ts'
import { environment } from '../config/environment.ts'

interface Config {
    environment: any
    endpoints: any
}

export function useConfig(): { config: Ref<Config> } {
    const config = ref<Config>({
        environment,
        endpoints
    })

    return { config }
}
