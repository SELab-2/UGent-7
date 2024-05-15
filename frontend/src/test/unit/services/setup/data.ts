import { SubmissionStatus } from "@/types/SubmisionStatus";

export const groups = [
    {
        id: '0',
        score: 20,
        project: '0',
        students: ['1', '2', '3', '000201247011'],
    },
    {
        id: '1',
        score: 18,
        project: '0',
        students: ['1', '2', '3', '000201247011'],
    },
];

export const courses = [
    {
        id: '1',
        excerpt: 'excerpt1',
        teachers: ['123', '124'],
        assistants: ['235', '236'],
        students: ['1', '2', '3', '000201247011'],
        projects: ['0', '1'],
        parent_course: null,
        faculty: null,
        name: 'Math',
        academic_startyear: 2023,
        description: 'Math course',
    },
    {
        id: '2',
        excerpt: 'excerpt2',
        teachers: [],
        assistants: [],
        students: [],
        projects: [],
        parent_course: '3',
        faculty: null,
        name: 'Sel2',
        academic_startyear: 2023,
        description: 'Software course',
    },
    {
        id: '3',
        excerpt: 'excerpt3',
        teachers: [],
        assistants: [],
        students: [],
        projects: [],
        parent_course: null,
        faculty: null,
        name: 'Sel1',
        academic_startyear: 2022,
        description: 'Software course',
    },
    {
        id: '12',
        excerpt: 'excerpt12',
        teachers: [],
        assistants: [],
        students: [],
        projects: [],
        parent_course: '1',
        faculty: null,
        name: 'Math',
        academic_startyear: 2024,
        description: 'Math course',
    },
    {
        id: '13',
        excerpt: 'excerpt13',
        teachers: [],
        assistants: [],
        students: [],
        projects: [],
        parent_course: '12',
        faculty: null,
        name: 'Math',
        academic_startyear: 2025,
        description: 'Math course',
    },
    {
        id: '14',
        excerpt: 'excerpt14',
        teachers: [],
        assistants: [],
        students: [],
        projects: [],
        parent_course: null,
        faculty: null,
        name: 'Club brugge',
        academic_startyear: 2023,
        description: null,
    },
    {
        id: '15',
        excerpt: 'excerpt15',
        teachers: [],
        assistants: [],
        students: [],
        projects: [],
        parent_course: null,
        faculty: null,
        name: 'vergeet barbara',
        academic_startyear: 2023,
        description: null,
    },
];

export const submissionStatuses = [
    {
        non_empty_groups: 5,
        groups_submitted: 4,
        structure_checks_passed: 3,
        extra_checks_passed: 1,
    },
    {
        non_empty_groups: 6,
        groups_submitted: 5,
        structure_checks_passed: 4,
        extra_checks_passed: 2,
    },
];

export const projects = [
    {
        id: '0',
        name: 'course0',
        description: 'course0 description',
        visible: true,
        archived: false,
        locked_groups: false,
        start_date: new Date('November 11, 2024 01:15:00'),
        deadline: new Date('November 11, 2025 01:15:00'),
        max_score: 100,
        score_visible: true,
        group_size: 5,
        course: courses[0],
        status: submissionStatuses[0],
        structure_file: new File(['byte1', 'byte2', 'byte3'], 'submission.zip', { type: 'application/zip' }),
        structureChecks: null,
        extra_checks: null,
        groups: [groups[0], groups[1]],
        submissions: null,
    },
    {
        id: '1',
        name: 'course1',
        description: 'course1 description',
        visible: true,
        archived: false,
        locked_groups: false,
        start_date: new Date('December 11, 2024 01:15:00'),
        deadline: new Date('December 11, 2025 01:15:00'),
        max_score: 50,
        score_visible: false,
        group_size: 8,
        course: courses[1],
        status: submissionStatuses[1],
        structure_file: new File(['byte1', 'byte2'], 'submission.zip', { type: 'application/zip' }),
        structureChecks: null,
        extra_checks: null,
        groups: [groups[0], groups[1]],
        submissions: null,
    },
];

export const faculties = [
    { id: 'sciences', name: 'wetenschappen' },
    { id: 'football', name: 'voetbal' },
];

export const students = [
    {
        id: '1',
        last_login: null,
        username: 'jdoe',
        is_staff: false,
        email: 'John.Doe@hotmail.com',
        first_name: 'John',
        last_name: 'Doe',
        last_enrolled: 2023,
        create_time: new Date('July 21, 2024 01:15:00'),
        student_id: null,
        roles: ['student'],
        courses: ['1', '2', '3'],
        groups: ['0'],
        faculties: [],
    },
    {
        id: '2',
        last_login: null,
        username: 'bverhae',
        is_staff: false,
        email: 'Bartje.Verhaege@gmail.com',
        first_name: 'Bartje',
        last_name: 'Verhaege',
        last_enrolled: 2023,
        create_time: new Date('July 21, 2024 01:15:00'),
        student_id: null,
        roles: ['student'],
        courses: [],
        groups: [],
        faculties: [],
    },
    {
        id: '000201247011',
        last_login: new Date('July 30, 2024 01:15:00'),
        username: 'tverslyp',
        is_staff: true,
        email: 'Tybo.Verslype@UGent.be',
        first_name: 'Tybo',
        last_name: 'Verslype',
        last_enrolled: 2023,
        create_time: new Date('July 21, 2024 01:15:00'),
        student_id: '02012470',
        roles: ['student'],
        courses: [],
        groups: [],
        faculties: [],
    },
    {
        id: '3',
        last_login: null,
        username: 'somtin',
        is_staff: false,
        email: 'somtin.somtin@gmail.com',
        first_name: 'somtin',
        last_name: 'somtin',
        last_enrolled: 2023,
        create_time: new Date('July 21, 2024 01:15:00'),
        student_id: null,
        roles: ['student'],
        courses: [],
        groups: [],
        faculties: [],
    },
];

export const teachers = [
    {
        id: '123',
        last_login: null,
        username: 'tboonen',
        is_staff: false,
        email: 'Tom.Boonen@gmail.be',
        first_name: 'Tom',
        last_name: 'Boonen',
        last_enrolled: 2023,
        create_time: new Date('July 21, 2024 01:15:00'),
    },
    {
        id: '124',
        last_login: null,
        username: 'psagan',
        is_staff: false,
        email: 'Peter.Sagan@gmail.com',
        first_name: 'Peter',
        last_name: 'Sagan',
        last_enrolled: 2023,
        create_time: new Date('July 21, 2024 01:15:00'),
    },
];

export const assistants = [
    {
        id: '235',
        courses: [],
        faculties: [],
        last_login: null,
        username: 'bsimpson',
        is_staff: false,
        email: 'Bart.Simpson@gmail.be',
        first_name: 'Bart',
        last_name: 'Simpson',
        last_enrolled: 2023,
        create_time: new Date('July 21, 2024 01:15:00'),
    },
    {
        id: '236',
        courses: [],
        faculties: [],
        last_login: null,
        username: 'kclijster',
        is_staff: false,
        email: 'Kim.Clijsters@gmail.be',
        first_name: 'Kim',
        last_name: 'Clijsters',
        last_enrolled: 2023,
        create_time: new Date('July 21, 2024 01:15:00'),
    },
];

export const admins = [
    {
        id: '300201547011',
        faculties: [],
        roles: ['student'],
        last_login: new Date('July 23, 2024 01:15:00'),
        username: 'tverslyp',
        is_staff: true,
        email: 'Tybo.Verslype@UGent.be',
        first_name: 'Tybo',
        last_name: 'Verslype',
        last_enrolled: 2023,
        create_time: new Date('July 21, 2024 01:15:00'),
    },
    {
        id: '400251245031',
        faculties: [],
        roles: ['student'],
        last_login: new Date('July 23, 2024 01:15:00'),
        username: 'simmig',
        is_staff: true,
        email: 'Simon.Mignolet@UGent.be',
        first_name: 'Simon',
        last_name: 'Mignolet',
        last_enrolled: 2023,
        create_time: new Date('July 21, 2024 01:15:00'),
    },
];

export const structureChecks = [
    {
        id: '1',
        project: '123456',
        obligated_extensions: [],
        blocked_extensions: [],
        name: '.',
    },
    {
        id: '2',
        project: '123456',
        obligated_extensions: [
            {
                extension: 'pdf',
            },
        ],
        blocked_extensions: [],
        name: 'folder1',
    },
    {
        id: '3',
        project: '123456',
        obligated_extensions: [],
        blocked_extensions: [],
        name: 'folder3',
    },
    {
        id: '4',
        project: '123456',
        obligated_extensions: [
            {
                extension: 'gif',
            },
        ],
        blocked_extensions: [],
        name: 'folder3/folder3-1',
    },
];

export const submissions = [
    {
        id: '1',
        group: '1',
        files: [],
        extra_checks_results: [],
        submission_number: 1,
        submission_time: new Date('July 21, 2024 01:15:00'),
        structureChecks_passed: true,
    },
    {
        id: '2',
        group: '1',
        files: [],
        extra_checks_results: [],
        submission_number: 2,
        submission_time: new Date('July 21, 2024 01:15:00'),
        structureChecks_passed: true,
    },
];
