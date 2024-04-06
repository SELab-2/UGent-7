export const USER_FILTER = {
    search: '',
    username: '',
    email: ''
};

export const COURSE_FILTER = {
    search: '',
    faculties: [],
    years: [],
};

export interface Filter {
    search: string;
    [key: string]: any;
}
