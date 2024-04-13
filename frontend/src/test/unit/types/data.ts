export const assistantData = {
    id: 'assistant1_id',
    username: 'assistant1',
    email: 'assistant1@ugent.be',
    first_name: 'assistant1_first_name',
    last_name: 'assistant1_last_name',
    last_enrolled: 2024,
    is_staff: true,
    roles: [],
    faculties: [],
    courses: [],
    create_time: new Date(),
    last_login: null,
};

export const studentData = {
    id: 'student1_id',
    username: 'student1',
    email: 'student1@ugent.be',
    first_name: 'student1_first_name',
    last_name: 'student1_last_name',
    last_enrolled: 2024,
    is_staff: true,
    roles: [],
    faculties: [],
    courses: [],
    create_time: new Date(),
    last_login: null,
    studentId: '1',
    groups: [],
};

export const teacherData = {
    id: 'teacher1_id',
    username: 'teacher1_username',
    email: 'teacher1@ugent.be',
    first_name: 'teacher1_first_name',
    last_name: 'teacher1_last_name',
    last_enrolled: 2022,
    is_staff: true,
    roles: [],
    faculties: [],
    courses: [],
    create_time: new Date(),
    last_login: null,
};

export const userData = {
    id: 'user1_id',
    username: 'user1_username',
    email: 'user1@ugent.be',
    first_name: 'user1_first_name',
    last_name: 'user1_last_name',
    last_enrolled: 2021,
    is_staff: false,
    roles: [],
    faculties: [],
    create_time: new Date(),
    last_login: null,
};

export const courseData = {
    id: 'course1_id',
    name: 'course1_name',
    description: 'course1_description',
    academic_startyear: 2024,
    parent_course: null,
    faculty: null,
    teachers: [],
    assistants: [],
    students: [],
    projects: [],
};

export const facultyData = {
    id: 'faculty1_id',
    name: 'faculty1_name',
};

export const groupData = {
    id: 'group1_id',
    score: 10,
    project: null,
    students: [],
    submissions: [],
};

export const projectData = {
    id: 'project1_id',
    name: 'project1_name',
    description: 'project1_description',
    visible: true,
    archived: false,
    locked_groups: false,
    start_date: new Date('November 1, 2024 04:20:00'),
    deadline: new Date('November 2, 2024 04:20:00'),
    max_score: 10,
    score_visible: true,
    group_size: 3,
    structure_file: null,
    course: null,
    structureChecks: [],
    extra_checks: [],
    groups: [],
    submissions: [],
};

export const responseData = {
    message: 'response message',
}
