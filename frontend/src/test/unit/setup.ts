import { afterAll, afterEach, beforeAll } from 'vitest'
import { setupServer } from 'msw/node'
import { HttpResponse, http } from 'msw'

import { endpoints } from '@/config/endpoints.ts'

const baseUrl = "http://localhost"

const groups = [
    {
        id: "0",
        score: 20
    },
    {
        id: "1",
        score: 18
    }
]

export const restHandlers = [
    http.get(baseUrl + endpoints.groups.retrieve.replace('{id}', ':id'),
        ({ params }) => {
            return HttpResponse.json(groups.filter(x => x.id == params.id))
        }
    )
]

const server = setupServer(...restHandlers)

beforeAll(() => server.listen({ onUnhandledRequest: "error" }))

afterAll(() => server.close())

afterEach(() => server.resetHandlers())