export const endpoints = {
    auth: {
        whoami: '/api/auth/cas/whoami/',
        login: '/api/auth/cas/login/',
        logout: '/api/auth/cas/logout/',
        token: {
            refresh: '/api/auth/token/refresh/',
            verify: '/api/auth/token/verify/',
            obtain: '/api/auth/token/'
        }
    },
    courses: {
        index: '/api/courses/',
        retrieve: '/api/courses/{id}/',
        byStudent: '/api/students/{student_id}/courses/',
        byTeacher: '/api/teachers/{teacher_id}/courses/',
        clone: '/api/courses/{course_id}/clone/'
    },
    students: {
        index: '/api/students/',
        retrieve: '/api/students/{id}/',
        byCourse: '/api/courses/{course_id}/students/',
        byGroup: '/api/groups/{group_id}/students/'
    },
    teachers: {
        index: '/api/teachers/',
        retrieve: '/api/teachers/{id}/',
        byCourse: '/api/courses/{course_id}/teachers/'
    },
    assistants: {
        index: '/api/assistants/',
        retrieve: '/api/assistants/{id}/',
        byCourse: '/api/courses/{course_id}/assistants/'
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
        byProject: '/api/projects/{project_id}/groups/',
        byStudent: '/api/students/{student_id}/groups/'
    },
    projects: {
        retrieve: '/api/projects/{id}',
        byCourse : '/api/courses/{course_id}/projects/'
    },
    submissions: {
        retrieve: '/api/submissions/{id}',
        byProject: '/api/projects/{project_id}/submissions/',
        byGroup: '/api/groups/{group_id}/submissions/',
        status: '/api/projects/{project_id}/submission_status/'
    },
    structure_checks: {
        retrieve: '/api/structure_checks/{id}',
        byProject: '/api/projects/{project_id}/structure_checks/'
    }
};