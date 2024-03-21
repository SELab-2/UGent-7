export const endpoints = {
    auth: {
        login: '/api/auth/cas/login/',
        logout: '/api/auth/cas/logout/'
    },
    courses: {
        index: '/api/courses/',
        retrieve: '/api/courses/{id}/'
    },
    students: {
        index: '/api/students/',
        retrieve: '/api/students/{id}/'
    },
    teachers: {
        index: '/api/teachers/',
        retrieve: '/api/teachers/{id}/'
    },
    admins: {
        index: '/api/admins/',
        retrieve: '/api/admins/{id}/'
    },
    faculties: {
        index: '/api/faculties/',
        retrieve: '/api/faculties/{name}'
    }
};