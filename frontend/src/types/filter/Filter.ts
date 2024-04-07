export const USER_FILTER = {
    search: '',
    id: '',
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
