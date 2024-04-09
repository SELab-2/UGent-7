import { type Ref, ref } from 'vue';
import { type Filter } from '@/types/filter/Filter.ts';
import { watchDebounced } from '@vueuse/core';
import { useRoute, useRouter } from 'vue-router';

export interface FilterState {
    filter: Ref<Filter>;
    onFilter: (callback: () => Promise<void>) => void;
}

export function useFilter(initial: Filter): FilterState {
    /* State */
    const filter = ref<Filter>(initial);
    const { query } = useRoute();
    const { push } = useRouter();

    /**
     * On filter callback
     *
     * @param callback
     */
    function onFilter(callback: () => Promise<void>) {
        watchDebounced(
            filter,
            async () => {
                await push({
                    query: {
                        ...query,
                        ...filter.value
                    },
                });

                await callback();
            },
            { debounce: 500, immediate: true, deep: true },
        );
    }

    return {
        filter, onFilter
    };
}
