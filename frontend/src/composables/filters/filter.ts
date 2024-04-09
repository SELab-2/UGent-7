import { type Ref, ref } from 'vue';
import { type Filter } from '@/types/filter/Filter.ts';

export interface FilterState {
    filter: Ref<Filter>;
}

export function useFilter(initial: Filter): FilterState {
    /* State */
    const filter = ref<Filter>(initial);

    return {
        filter,
    };
}
