export interface Filters {
    search: string;
    years?: number[];
    faculties?: string[];
    pagination?: PaginationRequest;
}

export interface PaginationRequest {
    page: number;
    page_size: number;
}

export interface PaginationResponse<T> {
    count: number;
    next: string | null;
    previous: string | null;
    results: T[];
}
