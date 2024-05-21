import { HttpResponse, http } from 'msw';

import { endpoints } from '@/config/endpoints.ts';
import {
    groups,
    projects,
    courses,
    faculties,
    students,
    teachers,
    assistants,
    admins,
    structureChecks,
    submissions,
} from './data';

const baseUrl = 'http://localhost';

export const getHandlers = [
    http.get(baseUrl + endpoints.groups.retrieve.replace('{id}', ':id'), ({ params }) => {
        return HttpResponse.json(groups.find((x) => x.id === params.id));
    }),
    http.get(baseUrl + endpoints.submissions.retrieve.replace('{id}', ':id'), ({ params }) => {
        const submission = submissions.find((x) => x.id === params.id)
        // Convert to a ResponseSubmission object
        const response_submission = {
            id: submission?.id,
            submission_number: submission?.submission_number,
            submission_time: submission?.submission_time,
            zip: submission?.zip,
            results: [], // We can leave this empty since the conversion to a valid results array is not the purpose of these tests
            is_valid: submission?.is_valid
        }
        return HttpResponse.json(response_submission);
    }),
    http.get(baseUrl + endpoints.structureChecks.retrieve.replace('{id}', ':id'), ({ params }) => {
        return HttpResponse.json(structureChecks.find((x) => x.id === params.id));
    }),
    http.get(baseUrl + endpoints.admins.retrieve.replace('{id}', ':id'), ({ params }) => {
        return HttpResponse.json(admins.find((x) => x.id === params.id));
    }),
    http.get(baseUrl + endpoints.teachers.retrieve.replace('{id}', ':id'), ({ params }) => {
        return HttpResponse.json(teachers.find((x) => x.id === params.id));
    }),
    http.get(baseUrl + endpoints.assistants.retrieve.replace('{id}', ':id'), ({ params }) => {
        return HttpResponse.json(assistants.find((x) => x.id === params.id));
    }),
    http.get(baseUrl + endpoints.students.retrieve.replace('{id}', ':id'), ({ params }) => {
        return HttpResponse.json(students.find((x) => x.id === params.id));
    }),
    http.get(baseUrl + endpoints.projects.retrieve.replace('{id}', ':id'), ({ params }) => {
        return HttpResponse.json(projects.find((x) => x.id === params.id));
    }),
    http.get(baseUrl + endpoints.courses.retrieve.replace('{id}', ':id'), ({ params }) => {
        return HttpResponse.json(courses.find((x) => x.id === params.id));
    }),
    http.get(baseUrl + endpoints.groups.byProject.replace('{projectId}', ':id'), ({ params }) => {
        return HttpResponse.json(groups.filter((x) => x.project.id === params.id));
    }),
    http.get(baseUrl + endpoints.submissions.byProject.replace('{projectId}', ':id'), ({ params }) => {
        const project = projects.find((x) => x.id === params.id);
        const submittedSubmissions = project !== null && project !== undefined ? project.submissions : [];

        // Convert to a ResponseSubmission object
        const projectSubmissions = submissions.filter((x) => submittedSubmissions.map(y => y.id).includes(x.id))
        const responseSubmissions = projectSubmissions.map(x => ({ id: x?.id, submission_number: x?.submission_number,submission_time: x?.submission_time,zip: x?.zip,results: [], is_valid: x?.is_valid }) )
        return HttpResponse.json(responseSubmissions);
    }),
    http.get(baseUrl + endpoints.teachers.byCourse.replace('{courseId}', ':id'), ({ params }) => {
        const course = courses.find((x) => x.id === params.id);
        const teacherIds = course !== null && course !== undefined ? course.teachers : [];
        return HttpResponse.json(teachers.filter((x) => teacherIds.includes(x.id)));
    }),
    http.get(baseUrl + endpoints.assistants.byCourse.replace('{courseId}', ':id'), ({ params }) => {
        const course = courses.find((x) => x.id === params.id);
        const assistantIds = course !== null && course !== undefined ? course.assistants : [];
        return HttpResponse.json(assistants.filter((x) => assistantIds.includes(x.id)));
    }),
    http.get(baseUrl + endpoints.courses.byStudent.replace('{studentId}', ':id'), ({ params }) => {
        const student = students.find((x) => x.id === params.id);
        const courseIds = student !== null && student !== undefined ? student.courses : [];
        return HttpResponse.json(courses.filter((x) => courseIds.includes(x.id)));
    }),
    http.get(baseUrl + endpoints.groups.byStudent.replace('{studentId}', ':id'), ({ params }) => {
        const student = students.find((x) => x.id === params.id);
        const groupIds = student !== null && student !== undefined ? student.groups : [];
        return HttpResponse.json(groups.filter((x) => groupIds.includes(x.id)));
    }),
    http.get(baseUrl + endpoints.students.byCourse.replace('{courseId}', ':id'), ({ params }) => {
        const course = courses.find((x) => x.id === params.id);
        const studentIds = course !== null && course !== undefined ? course.students : [];
        return HttpResponse.json(students.filter((x) => studentIds.includes(x.id)));
    }),
    http.get(baseUrl + endpoints.students.byGroup.replace('{groupId}', ':id'), ({ params }) => {
        const group = groups.find((x) => x.id === params.id);
        const studentIds = group !== null && group !== undefined ? group.students : [];
        return HttpResponse.json(students.filter((x) => studentIds.includes(x.id)));
    }),
    http.get(baseUrl + endpoints.submissions.status.replace('{projectId}', ':id'), ({ params }) => {
        const project = projects.find((x) => x.id === params.id);
        const groups = project !== null && project !== undefined ? project.groups : [];
        const groupIds = groups.map(group => group.id);
        const submissions = project !== null && project !== undefined ? project.submissions : [];
        const submissionIds = submissions.map(submission => submission.id);

        return HttpResponse.json({
            groups_submitted: new Set(submissions.filter((x) => submissionIds.includes(x.id)).map((x) => x.group)).size,
            non_empty_groups: groups.filter((x) => groupIds.includes(x.id) && x.students.length > 0).length,
        });
    }),
    http.get(baseUrl + endpoints.structureChecks.byProject.replace('{projectId}', ':id'), ({ params }) => {
        return HttpResponse.json(structureChecks.filter((x) => x.project === params.id));
    }),
    http.get(baseUrl + endpoints.projects.byCourse.replace('{courseId}', ':id'), ({ params }) => {
        return HttpResponse.json(projects.filter((x) => x.course.id === params.id));
    }),
    http.get(baseUrl + endpoints.projects.byStudent.replace('{studentId}', ':id'), ({ params }) => {
        return HttpResponse.json(
            projects.filter(
                (project) => project.course.id in students.find((student) => student.id === params.id).courses,
            ),
        );
    }),
    http.get(baseUrl + endpoints.submissions.byGroup.replace('{groupId}', ':id'), ({ params }) => {
        const group = groups.find((x) => x.id = params.id)
        const groupSubmissions = submissions.filter(x => group?.submissions.includes(x))
        
        // Convert to a ResponseSubmission object
        const responseSubmissions = groupSubmissions.map(x => ({ id: x?.id, submission_number: x?.submission_number,submission_time: x?.submission_time,zip: x?.zip,results: [], is_valid: x?.is_valid }) )
        return HttpResponse.json(responseSubmissions);
    }),
    http.get(baseUrl + endpoints.faculties.retrieve.replace('{id}', ':id'), ({ params }) => {
        return HttpResponse.json(faculties.find((x) => x.id === params.id));
    }),
    http.get(baseUrl + endpoints.faculties.index, () => {
        return HttpResponse.json(faculties);
    }),
    http.get(baseUrl + endpoints.courses.index, () => {
        return HttpResponse.json(courses);
    }),
    http.get(baseUrl + endpoints.admins.index, () => {
        return HttpResponse.json(admins);
    }),
    http.get(baseUrl + endpoints.students.index, () => {
        return HttpResponse.json(students);
    }),
    http.get(baseUrl + endpoints.teachers.index, () => {
        return HttpResponse.json(teachers);
    }),
    http.get(baseUrl + endpoints.assistants.index, () => {
        return HttpResponse.json(assistants);
    }),
];
