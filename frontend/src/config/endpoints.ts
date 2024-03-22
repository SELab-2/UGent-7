export const endpoints = {
    auth: {
        login: '/api/auth/cas/login/',
        logout: '/api/auth/cas/logout/'
    },
    courses: {
        index: '/api/courses/',
        retrieve: '/api/courses/{id}/',
        byStudent: 'api/students/{student_id}/courses/'
    },
    students: {
        index: '/api/students/',
        retrieve: '/api/students/{id}/'
    },
    teachers: {
        index: '/api/teachers/',
        retrieve: '/api/teachers/{id}/'
    },
    assistants: {
        index: '/api/assistant/',
        retrieve: '/api/assistant/{id}/'
    },
    admins: {
        index: '/api/admins/',
        retrieve: '/api/admins/{id}/'
    },
    faculties: {
        index: '/api/faculties/',
        retrieve: '/api/faculties/{name}'
    },
    groups: {
        retrieve: '/api/groups/{id}/',
        byProject: '/api/projects/{project_id}/groups/'
    },
    projects: {
        retrieve: '/api/projects/{id}',
        byCourse : '/api/courses/{course_id}/projects/'
    },
    submissions: {
        retrieve: '/api/submissions/{id}',
        byProject: '/api/projects/{project_id}/submissions/',
        byGroup: '/api/groups/{group_id}/submissions/'
    },
    structure_checks: {
        retrieve: '/api/structure_checks/{id}',
        byProject: '/api/projects/{project_id}/structure_checks/'
    }
};