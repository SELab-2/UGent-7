import { afterAll, afterEach, beforeAll } from 'vitest'
import { setupServer } from 'msw/node'
import { HttpResponse, http } from 'msw'

import { endpoints } from '@/config/endpoints.ts'

const baseUrl = 'http://localhost'

const groups = [
    {
        id: '0',
        score: 20,
        project: '0',
        students: ['1', '2', '3', '000201247011']
    },
    {
        id: '1',
        score: 18,
        project: '0',
        students: ['1', '2', '3', '000201247011']
    }
]

const projects = [
    {
        id: '0',
        course: '1',
        name: 'sel2',
        description: 'this is a test',
        visible: true,
        archived: false,
        locked_groups: false,
        start_date: new Date('July 21, 2024 01:15:00'),
        deadline: new Date('July 23, 2024 01:15:00'),
        max_score: 100,
        score_visible: true,
        group_size: 8,
        submissions: ['1', '2'],
        groups: ['0', '1']
    },
    {
        id: 1,
        course: '1',
        name: 'sel3',
        description: 'make a project',
        visible: true,
        archived: false,
        locked_groups: false,
        start_date: new Date('July 21, 2024 01:15:00'),
        deadline: new Date('July 23, 2024 01:15:00'),
        max_score: 20,
        score_visible: false,
        group_size: 3,
        submissions: [],
        groups: ['0', '1']
    }
]

const courses = [
    {
        id: '1',
        teachers: ['123', '124'],
        assistants: ['235', '236'],
        students: ['1', '2', '3', '000201247011'],
        projects: ['0', '1'],
        parent_course: null,
        name: 'Math',
        academic_startyear: 2023,
        description: 'Math course'
    },
    {
        id: '2',
        teachers: [],
        assistants: [],
        students: [],
        projects: [],
        parent_course: '3',
        name: 'Sel2',
        academic_startyear: 2023,
        description: 'Software course'
    },
    {
        id: '3',
        teachers: [],
        assistants: [],
        students: [],
        projects: [],
        parent_course: null,
        name: 'Sel1',
        academic_startyear: 2022,
        description: 'Software course'
    },
    {
        id: '12',
        teachers: [],
        assistants: [],
        students: [],
        projects: [],
        parent_course: '1',
        name: 'Math',
        academic_startyear: 2024,
        description: 'Math course'
    },
    {
        id: '13',
        teachers: [],
        assistants: [],
        students: [],
        projects: [],
        parent_course: '12',
        name: 'Math',
        academic_startyear: 2025,
        description: 'Math course'
    },
    {
        id: '14',
        teachers: [],
        assistants: [],
        students: [],
        projects: [],
        parent_course: null,
        name: 'Club brugge',
        academic_startyear: 2023,
        description: null
    },
    {
        id: '15',
        teachers: [],
        assistants: [],
        students: [],
        projects: [],
        parent_course: null,
        name: 'vergeet barbara',
        academic_startyear: 2023,
        description: null
    }
]

const faculties = [{ name: 'wetenschappen' }, { name: 'voetbal' }]

const students = [
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
        courses: ['1', '2', '3'],
        groups: ['0']
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
        courses: [],
        groups: []
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
        courses: [],
        groups: []
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
        courses: [],
        groups: []
    }
]

const teachers = [
    {
        id: '123',
        last_login: null,
        username: 'tboonen',
        is_staff: false,
        email: 'Tom.Boonen@gmail.be',
        first_name: 'Tom',
        last_name: 'Boonen',
        last_enrolled: 2023,
        create_time: new Date('July 21, 2024 01:15:00')
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
        create_time: new Date('July 21, 2024 01:15:00')
    }
]

const assistants = [
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
        create_time: new Date('July 21, 2024 01:15:00')
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
        create_time: new Date('July 21, 2024 01:15:00')
    }
]

const admins = [
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
        create_time: new Date('July 21, 2024 01:15:00')
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
        create_time: new Date('July 21, 2024 01:15:00')
    }
]

const structure_checks = [
    {
        id: '1',
        project: '123456',
        obligated_extensions: [],
        blocked_extensions: [],
        name: '.'
    },
    {
        id: '2',
        project: '123456',
        obligated_extensions: [
            {
                extension: 'pdf'
            }
        ],
        blocked_extensions: [],
        name: 'folder1'
    },
    {
        id: '3',
        project: '123456',
        obligated_extensions: [],
        blocked_extensions: [],
        name: 'folder3'
    },
    {
        id: '4',
        project: '123456',
        obligated_extensions: [
            {
                extension: 'gif'
            }
        ],
        blocked_extensions: [],
        name: 'folder3/folder3-1'
    }
]

const submissions = [
    {
        id: '1',
        group: '1',
        files: [],
        extra_checks_results: [],
        submission_number: 1,
        submission_time: new Date('July 21, 2024 01:15:00'),
        structure_checks_passed: true
    },
    {
        id: '2',
        group: '1',
        files: [],
        extra_checks_results: [],
        submission_number: 2,
        submission_time: new Date('July 21, 2024 01:15:00'),
        structure_checks_passed: true
    }
]

export const restHandlers = [
    http.get(
        baseUrl + endpoints.groups.retrieve.replace('{id}', ':id'),
        ({ params }) => {
            return HttpResponse.json(groups.find((x) => x.id === params.id))
        }
    ),
    http.get(
        baseUrl + endpoints.submissions.retrieve.replace('{id}', ':id'),
        ({ params }) => {
            return HttpResponse.json(
                submissions.find((x) => x.id === params.id)
            )
        }
    ),
    http.get(
        baseUrl + endpoints.structure_checks.retrieve.replace('{id}', ':id'),
        ({ params }) => {
            return HttpResponse.json(
                structure_checks.find((x) => x.id === params.id)
            )
        }
    ),
    http.get(
        baseUrl + endpoints.admins.retrieve.replace('{id}', ':id'),
        ({ params }) => {
            return HttpResponse.json(admins.find((x) => x.id === params.id))
        }
    ),
    http.get(
        baseUrl + endpoints.teachers.retrieve.replace('{id}', ':id'),
        ({ params }) => {
            return HttpResponse.json(teachers.find((x) => x.id === params.id))
        }
    ),
    http.get(
        baseUrl + endpoints.assistants.retrieve.replace('{id}', ':id'),
        ({ params }) => {
            return HttpResponse.json(assistants.find((x) => x.id === params.id))
        }
    ),
    http.get(
        baseUrl + endpoints.students.retrieve.replace('{id}', ':id'),
        ({ params }) => {
            return HttpResponse.json(students.find((x) => x.id === params.id))
        }
    ),
    http.get(
        baseUrl + endpoints.projects.retrieve.replace('{id}', ':id'),
        ({ params }) => {
            return HttpResponse.json(projects.find((x) => x.id === params.id))
        }
    ),
    http.get(
        baseUrl + endpoints.courses.retrieve.replace('{id}', ':id'),
        ({ params }) => {
            return HttpResponse.json(courses.find((x) => x.id === params.id))
        }
    ),
    http.get(
        baseUrl + endpoints.groups.byProject.replace('{project_id}', ':id'),
        ({ params }) => {
            return HttpResponse.json(
                groups.filter((x) => x.project === params.id)
            )
        }
    ),
    http.get(
        baseUrl +
            endpoints.submissions.byProject.replace('{project_id}', ':id'),
        ({ params }) => {
            const project = projects.find((x) => x.id === params.id)
            const submited_submissions =
                project !== null && project !== undefined
                    ? project.submissions
                    : []
            return HttpResponse.json(
                submissions.filter((x) => submited_submissions.includes(x.id))
            )
        }
    ),
    http.get(
        baseUrl + endpoints.teachers.byCourse.replace('{course_id}', ':id'),
        ({ params }) => {
            const course = courses.find((x) => x.id === params.id)
            const teacher_ids =
                course !== null && course !== undefined ? course.teachers : []
            return HttpResponse.json(
                submissions.filter((x) => teacher_ids.includes(x.id))
            )
        }
    ),
    http.get(
        baseUrl + endpoints.assistants.byCourse.replace('{course_id}', ':id'),
        ({ params }) => {
            const course = courses.find((x) => x.id === params.id)
            const assistant_ids =
                course !== null && course !== undefined ? course.assistants : []
            return HttpResponse.json(
                assistants.filter((x) => assistant_ids.includes(x.id))
            )
        }
    ),
    http.get(
        baseUrl + endpoints.courses.byStudent.replace('{student_id}', ':id'),
        ({ params }) => {
            const student = students.find((x) => x.id === params.id)
            const course_ids =
                student !== null && student !== undefined ? student.courses : []
            return HttpResponse.json(
                courses.filter((x) => course_ids.includes(x.id))
            )
        }
    ),
    http.get(
        baseUrl + endpoints.groups.byStudent.replace('{student_id}', ':id'),
        ({ params }) => {
            const student = students.find((x) => x.id === params.id)
            const group_ids =
                student !== null && student !== undefined ? student.groups : []
            return HttpResponse.json(
                groups.filter((x) => group_ids.includes(x.id))
            )
        }
    ),
    http.get(
        baseUrl + endpoints.students.byCourse.replace('{course_id}', ':id'),
        ({ params }) => {
            const course = courses.find((x) => x.id === params.id)
            const student_ids =
                course !== null && course !== undefined ? course.students : []
            return HttpResponse.json(
                students.filter((x) => student_ids.includes(x.id))
            )
        }
    ),
    http.get(
        baseUrl + endpoints.students.byGroup.replace('{group_id}', ':id'),
        ({ params }) => {
            const group = groups.find((x) => x.id === params.id)
            const student_ids =
                group !== null && group !== undefined ? group.students : []
            return HttpResponse.json(
                students.filter((x) => student_ids.includes(x.id))
            )
        }
    ),
    http.get(
        baseUrl + endpoints.submissions.status.replace('{project_id}', ':id'),
        ({ params }) => {
            const project = projects.find((x) => x.id === params.id)
            const group_ids =
                project !== null && project !== undefined ? project.groups : []
            const submission_ids =
                project !== null && project !== undefined
                    ? project.submissions
                    : []
            const subGroups_ids = Array.from(
                new Set(
                    submissions
                        .filter((x) => submission_ids.includes(x.id))
                        .map((x) => x.group)
                )
            )

            // Filter submissions for each subgroup and get the submission with the highest number
            const subgroupSubmissions = subGroups_ids.map((groupId) => {
                const submissionsForGroup = submissions.filter(
                    (submission) => submission.group === groupId
                )
                if (submissionsForGroup.length > 0) {
                    return submissionsForGroup.reduce(
                        (maxSubmission, currentSubmission) => {
                            return currentSubmission.submission_number >
                                maxSubmission.submission_number
                                ? currentSubmission
                                : maxSubmission
                        }
                    )
                } else {
                    return null
                }
            })
            return HttpResponse.json({
                groups_submitted: new Set(
                    submissions
                        .filter((x) => submission_ids.includes(x.id))
                        .map((x) => x.group)
                ).size,
                non_empty_groups: groups.filter(
                    (x) => group_ids.includes(x.id) && x.students.length > 0
                ).length,
                submissions_passed: subgroupSubmissions.filter(
                    (x) => x?.structure_checks_passed
                ).length
            })
        }
    ),
    http.get(
        baseUrl +
            endpoints.structure_checks.byProject.replace('{project_id}', ':id'),
        ({ params }) => {
            return HttpResponse.json(
                structure_checks.filter((x) => x.project === params.id)
            )
        }
    ),
    http.get(
        baseUrl + endpoints.projects.byCourse.replace('{course_id}', ':id'),
        ({ params }) => {
            return HttpResponse.json(
                projects.filter((x) => x.course === params.id)
            )
        }
    ),
    http.get(
        baseUrl + endpoints.submissions.byGroup.replace('{group_id}', ':id'),
        ({ params }) => {
            return HttpResponse.json(
                submissions.filter((x) => x.group === params.id)
            )
        }
    ),
    http.get(
        baseUrl + endpoints.faculties.retrieve.replace('{name}', ':name'),
        ({ params }) => {
            return HttpResponse.json(
                faculties.find((x) => x.name === params.name)
            )
        }
    ),
    http.get(baseUrl + endpoints.faculties.index, () => {
        return HttpResponse.json(faculties)
    }),
    http.get(baseUrl + endpoints.courses.index, () => {
        return HttpResponse.json(courses)
    }),
    http.get(baseUrl + endpoints.admins.index, () => {
        return HttpResponse.json(admins)
    }),
    http.get(baseUrl + endpoints.students.index, () => {
        return HttpResponse.json(students)
    }),
    http.get(baseUrl + endpoints.teachers.index, () => {
        return HttpResponse.json(teachers)
    }),
    http.get(baseUrl + endpoints.assistants.index, () => {
        return HttpResponse.json(assistants)
    })

    /*
    http.post(baseUrl + endpoints.groups.byProject.replace('{project_id}', ':id'),
        ({ params }) => {
            const newGroup = params.body; // Assuming the request body contains the new group data
            groups.push(newGroup);
            return HttpResponse.json(newGroup);
        }
    )
    */
]

const server = setupServer(...restHandlers)

beforeAll(() => {
    server.listen({ onUnhandledRequest: 'error' })
})

afterAll(() => {
    server.close()
})

afterEach(() => {
    server.resetHandlers()
})
