export type Filters = {
    search: string;
    years?: number[];
    faculties?: string[];
    pagination?: PaginationRequest
};

export type PaginationRequest = {
    page: number;
    page_size: number;
};

export type PaginationResponse<T> = {
    count: number;
    next: string | null;
    previous: string | null;
    results: T[];
};