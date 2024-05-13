/* eslint-disable @typescript-eslint/no-unused-vars */
/* eslint-disable @typescript-eslint/no-unsafe-argument */
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

export const postHandlers = [
    http.post(baseUrl + endpoints.admins.index, async ({ request }) => {
        const buffer = await request.arrayBuffer();
        const requestBody = new TextDecoder().decode(buffer);
        const newAdmin = JSON.parse(requestBody);
        admins.push(newAdmin);
        return HttpResponse.json(admins);
    }),
    http.post(baseUrl + endpoints.assistants.index, async ({ request }) => {
        const buffer = await request.arrayBuffer();
        const requestBody = new TextDecoder().decode(buffer);
        const newAssistant = JSON.parse(requestBody);
        assistants.push({ id: newAssistant.user, ...newAssistant });
        return HttpResponse.json(assistants);
    }),
    http.post(baseUrl + endpoints.students.index, async ({ request }) => {
        const buffer = await request.arrayBuffer();
        const requestBody = new TextDecoder().decode(buffer);
        const newStudent = JSON.parse(requestBody);
        students.push({ id: newStudent.user, student_id: newStudent.student_id, ...newStudent });
        return HttpResponse.json(students);
    }),
    http.post(baseUrl + endpoints.courses.index, async ({ request }) => {
        const buffer = await request.arrayBuffer();
        const requestBody = new TextDecoder().decode(buffer);
        const newCourse = JSON.parse(requestBody);
        courses.push(newCourse);
        return HttpResponse.json(courses);
    }),
    http.post(baseUrl + endpoints.faculties.index, async ({ request }) => {
        const buffer = await request.arrayBuffer();
        const requestBody = new TextDecoder().decode(buffer);
        const newFaculty = JSON.parse(requestBody);
        faculties.push(newFaculty);
        return HttpResponse.json(faculties);
    }),
    http.post(baseUrl + endpoints.groups.byProject.replace('{projectId}', ':id'), async ({ request, params }) => {
        const buffer = await request.arrayBuffer();
        const requestBody = new TextDecoder().decode(buffer);
        const newGroup = JSON.parse(requestBody);
        groups.push(newGroup);
        return HttpResponse.json(groups);
    }),
    http.post(baseUrl + endpoints.projects.byCourse.replace('{courseId}', ':id'), async ({ request, params }) => {
        const buffer = await request.arrayBuffer();
        const requestBody = new TextDecoder().decode(buffer);
        const newProject = JSON.parse(requestBody);
        projects.push(newProject);
        return HttpResponse.json(projects);
    }),
];
