import { type LocationQuery } from 'vue-router';

export type UserFilter = {
    id: string;
    name: string;
    username: string;
    email: string;
    roles: string[];
    faculties: string[];
} & Filter;

export type CourseFilter = {
    faculties: string[];
    years: string[];
} & Filter;

export type DockerImageFilter = {
    id: string;
    name: string;
    owner: string;
} & Filter;

export interface Filter {
    search: string;
    [key: string]: string | string[];
}

/**
 * Get the user filters from the query.
 *
 * @param query
 */
export function getUserFilters(query: LocationQuery): UserFilter {
    const filters: UserFilter = {
        search: query.search?.toString() ?? '',
        id: query.id?.toString() ?? '',
        name: query.name?.toString() ?? '',
        username: query.username?.toString() ?? '',
        email: query.email?.toString() ?? '',
        roles: [],
        faculties: [],
    };

    if (query.roles !== undefined) {
        filters.roles = getQueryList(query.roles as string | string[]);
    }

    if (query.faculties !== undefined) {
        filters.faculties = getQueryList(query.faculties as string | string[]);
    }

    return filters;
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
 * Get the docker image filters from the query.
 *
 * @param query
 */
export function getDockerImageFilters(query: LocationQuery): DockerImageFilter {
    return {
        search: query.search?.toString() ?? '',
        id: query.id?.toString() ?? '',
        name: query.id?.toString() ?? '',
        owner: query.id?.toString() ?? '',
    };
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
