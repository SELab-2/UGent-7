import { afterAll, afterEach, beforeAll } from 'vitest'
import { setupServer } from 'msw/node'
import { HttpResponse, http } from 'msw'

import { endpoints } from '@/config/endpoints.ts'

const baseUrl = "http://localhost"

const groups = [
    {
        id: "0",
        score: 20,
        project:"0",
    },
    {
        id: "1",
        score: 18,
        project:"0"
    }
]

const projects = [
    {
        id: "0",
        name: "sel2",
        description: "this is a test",
        visible: true,
        archived: false,
        locked_groups: false,
        start_date: new Date(),
        deadline: new Date(),
        max_score: 100,
        score_visible: true,
        group_size: 8
    }
]

const faculties = [
    {name: "wetenschappen"},
    {name: "voetbal"}
]

export const restHandlers = [
    http.get(baseUrl + endpoints.groups.retrieve.replace('{id}', ':id'),
        ({ params }) => {
            return HttpResponse.json(groups.find(x => x.id == params.id))
        }
    ),
    http.get(baseUrl + endpoints.groups.byProject.replace('{project_id}', ':id'),
        ({ params }) => {
            return HttpResponse.json(groups.filter(x => x.project == params.id))
        }
    ),
    http.get(baseUrl + endpoints.faculties.retrieve.replace('{name}', ':name'),
        ({ params }) => {
            return HttpResponse.json(faculties.find(x => x.name == params.name))
        }
    ),
    http.get(baseUrl + endpoints.faculties.index,
        ({}) => {
            return HttpResponse.json(faculties)
        }
    )

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

beforeAll(() => server.listen({ onUnhandledRequest: "error" }))

afterAll(() => server.close())

afterEach(() => server.resetHandlers())