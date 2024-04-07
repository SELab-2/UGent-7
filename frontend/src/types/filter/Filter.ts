import { type LocationQuery } from 'vue-router';

export const USER_FILTER = {
    search: '',
    id: '',
    username: '',
    email: '',
};

export type CourseFilter = {
    faculties: string[];
    years: string[];
} & Filter;

export interface Filter {
    search: string;
    [key: string]: string | string[];
}

/**
 * Get the course filters from the query.
 *
 * @param query
 */
export function getCourseFilters(query: LocationQuery): CourseFilter {
    const filters: CourseFilter = {
        search: query.search?.toString() ?? '',
        faculties: [],
        years: [],
    };

    if (query.faculties !== undefined) {
        filters.faculties = getQueryList(query.faculties as string | string[]);
    }

    if (query.years !== undefined) {
        filters.years = getQueryList(query.years as string | string[]);
    }

    return filters;
}

/**
 * Get the query list.
 *
 * @param query
 */
function getQueryList(query: string | string[] | undefined): string[] {
    if (query === undefined) return [];

    if (Array.isArray(query)) {
        return query;
    }

    return [query?.toString()];
}
