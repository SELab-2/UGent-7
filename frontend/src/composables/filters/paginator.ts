import { computed, type Ref, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { type PaginatorResponse } from '@/types/filter/Paginator.ts';

export interface PaginatorState {
    page: Ref<number>;
    pageSize: Ref<number>;
    first: Ref<number>;
    onPaginate: (callback: () => Promise<void>) => void;
    resetPagination: (pagination: Ref<PaginatorResponse<any> | null>) => Promise<void>;
}

export function usePaginator(initialPage: number = 1, initialPageSize: number = 20): PaginatorState {
    /* Composables */
    const { query } = useRoute();
    const { push } = useRouter();

    /* State */
    const page = ref<number>(parseInt(query.page?.toString() ?? initialPage.toString()));

    const pageSize = ref<number>(parseInt(query.pageSize?.toString() ?? initialPageSize.toString()));

    /* Computed */
    const first = computed({
        get: () => (page.value - 1) * pageSize.value,
        set: (value: number) => (page.value = Math.floor(value / pageSize.value) + 1),
    });

    /**
     * Reset the pagination to the first page.
     *
     * @returns void
     */
    async function resetPagination(pagination: Ref<PaginatorResponse<any> | null>): Promise<void> {
        // Paginate to the first page upon filter change
        first.value = 0;

        if (pagination.value !== null) {
            // Reset the results
            pagination.value.results = null;
        }
    }

    /**
     * On paginate callback
     *
     * @param callback
     */
    function onPaginate(callback: () => Promise<void>): void {
        watch(page, async () => {
            await push({
                query: {
                    page: page.value,
                    pageSize: pageSize.value,
                },
            });

            await callback();
        });
    }

    return {
        page,
        pageSize,
        first,
        onPaginate,
        resetPagination,
    };
}
