
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
    submissions
} from './data';

const baseUrl = 'http://localhost';

export const getHandlers = [
    http.get(baseUrl + endpoints.groups.retrieve.replace('{id}', ':id'), ({ params }) => {
        return HttpResponse.json(groups.find((x) => x.id === params.id));
    }),
    http.get(baseUrl + endpoints.submissions.retrieve.replace('{id}', ':id'), ({ params }) => {
        return HttpResponse.json(submissions.find((x) => x.id === params.id));
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
        return HttpResponse.json(groups.filter((x) => x.project === params.id));
    }),
    http.get(baseUrl + endpoints.submissions.byProject.replace('{projectId}', ':id'), ({ params }) => {
        const project = projects.find((x) => x.id === params.id);
        const submittedSubmissions = project !== null && project !== undefined ? project.submissions : [];
        return HttpResponse.json(submissions.filter((x) => submittedSubmissions.includes(x.id)));
    }),
    http.get(baseUrl + endpoints.teachers.byCourse.replace('{courseId}', ':id'), ({ params }) => {
        const course = courses.find((x) => x.id === params.id);
        const teacherIds = course !== null && course !== undefined ? course.teachers : [];
        return HttpResponse.json(submissions.filter((x) => teacherIds.includes(x.id)));
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
        const groupIds = project !== null && project !== undefined ? project.groups : [];
        const submissionIds = project !== null && project !== undefined ? project.submissions : [];
        const subGroupIds = Array.from(
            new Set(submissions.filter((x) => submissionIds.includes(x.id)).map((x) => x.group)),
        );

        // Filter submissions for each subgroup and get the submission with the highest number
        const subgroupSubmissions = subGroupIds.map((groupId) => {
            const submissionsForGroup = submissions.filter((submission) => submission.group === groupId);
            if (submissionsForGroup.length > 0) {
                return submissionsForGroup.reduce((maxSubmission, currentSubmission) => {
                    return currentSubmission.submission_number > maxSubmission.submission_number
                        ? currentSubmission
                        : maxSubmission;
                });
            } else {
                return null;
            }
        });
        return HttpResponse.json({
            groups_submitted: new Set(submissions.filter((x) => submissionIds.includes(x.id)).map((x) => x.group)).size,
            non_empty_groups: groups.filter((x) => groupIds.includes(x.id) && x.students.length > 0).length,
            submissions_passed: subgroupSubmissions.filter((x) => x?.structureChecks_passed).length,
        });
    }),
    http.get(baseUrl + endpoints.structureChecks.byProject.replace('{projectId}', ':id'), ({ params }) => {
        return HttpResponse.json(structureChecks.filter((x) => x.project === params.id));
    }),
    http.get(baseUrl + endpoints.projects.byCourse.replace('{courseId}', ':id'), ({ params }) => {
        return HttpResponse.json(projects.filter((x) => x.course === params.id));
    }),
    http.get(baseUrl + endpoints.submissions.byGroup.replace('{groupId}', ':id'), ({ params }) => {
        return HttpResponse.json(submissions.filter((x) => x.group === params.id));
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
]

