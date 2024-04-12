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

export const deleteHandlers = [
    http.delete(baseUrl + endpoints.admins.retrieve.replace('{id}', ':id'), async ({ params }) => {
        const index = admins.findIndex(x => x.id === params.id);
        admins.splice(index, 1);
        return HttpResponse.json(admins);
    }),
];
