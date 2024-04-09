import { computed, type Ref, ref, watch } from 'vue';
import { type LocationQuery, useRoute, useRouter } from 'vue-router';

export interface PaginatorState {
    page: Ref<number>;
    pageSize: Ref<number>;
    first: Ref<number>;
    paginate: (newFirst: number) => Promise<void>;
    onPaginate: (callback: () => Promise<void>) => void;
}

export function usePaginator(initialPage: number = 1, initialPageSize: number = 20): PaginatorState {
    /* Composables */
    const { query } = useRoute();
    const { push } = useRouter();

    /* State */
    const page = ref<number>(parseInt(query.page as string) || initialPage);
    const pageSize = ref<number>(parseInt(query.pageSize as string) || initialPageSize);

    /* Watchers */
    watch(
        () => query,
        (query: LocationQuery) => {
            if (query.page !== undefined) {
                page.value = parseInt(query.page as string);
            }

            if (query.pageSize !== undefined) {
                pageSize.value = parseInt(query.pageSize as string);
            }
        },
        { immediate: true },
    );

    /* Computed */
    const first = computed({
        get: () => (page.value - 1) * pageSize.value,
        set: (value: number) => (page.value = Math.floor(value / pageSize.value) + 1),
    });

    /**
     * Paginate using a new first item index.
     *
     * @param newFirst
     */
    async function paginate(newFirst: number): Promise<void> {
        first.value = newFirst;

        await push({
            query: {
                page: page.value,
                pageSize: pageSize.value,
            },
        });
    }

    /**
     * On paginate callback
     *
     * @param callback
     */
    async function onPaginate(callback: () => Promise<void>) {
        watch(page, async () => {
            await callback();
        });
    }

    return {
        page,
        pageSize,
        first,
        paginate,
        onPaginate,
    };
}
