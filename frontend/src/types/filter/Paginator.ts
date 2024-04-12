import { type Course } from '@/types/Course.ts';

export interface PaginatorResponse<T> {
    count: number;
    next: string | null;
    previous: string | null;
    results: T[] | null;
}

export interface CoursePaginatorResponse extends PaginatorResponse<Course> {
    min_year: number;
    max_year: number;
}
