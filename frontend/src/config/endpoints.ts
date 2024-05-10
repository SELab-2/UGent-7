export const endpoints = {
    auth: {
        whoami: '/api/auth/cas/whoami/',
        login: '/api/auth/cas/login/',
        logout: '/api/auth/cas/logout/',
        token: {
            refresh: '/api/auth/token/refresh/',
            verify: '/api/auth/token/verify/',
            obtain: '/api/auth/token/',
        },
    },
    courses: {
        index: '/api/courses/',
        search: '/api/courses/search/',
        retrieve: '/api/courses/{id}/',
        clone: '/api/courses/{courseId}/clone/',
        invitationLink: '/api/courses/{courseId}/invitation_link/',
        byStudent: '/api/students/{studentId}/courses/',
        byTeacher: '/api/teachers/{teacherId}/courses/',
        byAssistant: '/api/assistants/{assistantId}/courses/',
    },
    dockerImages: {
        index: '/api/docker-images/',
        search: '/api/docker-images/search/',
        patch: '/api/docker-images/{id}/public/',
    },
    students: {
        index: '/api/students/',
        retrieve: '/api/students/{id}/',
        byCourse: '/api/courses/{courseId}/students/',
        byGroup: '/api/groups/{groupId}/students/',
    },
    teachers: {
        index: '/api/teachers/',
        search: '/api/teachers/search/',
        retrieve: '/api/teachers/{id}/',
        byCourse: '/api/courses/{courseId}/teachers/',
    },
    assistants: {
        index: '/api/assistants/',
        search: '/api/assistants/search/',
        retrieve: '/api/assistants/{id}/',
        byCourse: '/api/courses/{courseId}/assistants/',
    },
    admins: {
        index: '/api/admins/',
        retrieve: '/api/admins/{id}/',
    },
    users: {
        index: '/api/users/',
        search: '/api/users/search/',
        retrieve: '/api/users/{id}/',
        admin: '/api/users/{id}/admin/',
    },
    faculties: {
        index: '/api/faculties/',
        retrieve: '/api/faculties/{id}',
    },
    groups: {
        retrieve: '/api/groups/{id}/',
        byProject: '/api/projects/{projectId}/groups/',
        byStudent: '/api/students/{studentId}/groups/',
    },
    projects: {
        retrieve: '/api/projects/{id}/',
        byCourse: '/api/courses/{courseId}/projects/',
        byStudent: '/api/students/{studentId}/projects/',
        byTeacher: '/api/teachers/{teacherId}/projects/',
        byAssistant: '/api/assistants/{assistantId}/projects/',
        extraChecks: '/api/projects/{projectId}/extra_checks/',
    },
    submissions: {
        retrieve: '/api/submissions/{id}',
        byProject: '/api/projects/{projectId}/submissions/',
        byGroup: '/api/groups/{groupId}/submissions/',
        status: '/api/projects/{projectId}/submission_status/',
    },
    structureChecks: {
        retrieve: '/api/structureChecks/{id}',
        byProject: '/api/projects/{projectId}/structureChecks/',
    },
};
