import { type Ref, ref } from 'vue';
import { type Filter } from '@/types/filter/Filter.ts';
import { watchDebounced } from '@vueuse/core';
import { useRoute, useRouter } from 'vue-router';

export interface FilterState {
    filter: Ref<Filter>;
    onFilter: (callback: () => Promise<void>, debounce?: number, immediate?: boolean) => void;
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
     * @param debounce
     * @param immediate
     */
    function onFilter(callback: () => Promise<void>, debounce: number = 500, immediate: boolean = true): void {
        watchDebounced(
            filter,
            async () => {
                await push({
                    query: {
                        ...query,
                        ...filter.value,
                    },
                });

                await callback();
            },
            { debounce, immediate, deep: true },
        );
    }

    return {
        filter,
        onFilter,
    };
}
