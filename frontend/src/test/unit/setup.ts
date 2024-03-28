import { afterAll, afterEach, beforeAll } from 'vitest'
import { setupServer } from 'msw/node'
import { HttpResponse, http } from 'msw'

import { endpoints } from '@/config/endpoints.ts'

const baseUrl = "http://localhost"

const groups = [
    {
        id: "0",
        score: 20
    }
]

export const restHandlers = [
    http.get(baseUrl + endpoints.groups.retrieve.replace('{id}', '0'), () => {
        return HttpResponse.json(groups[0])
    })
]

const server = setupServer(...restHandlers)

beforeAll(() => server.listen({ onUnhandledRequest: "error" }))

afterAll(() => server.close())

afterEach(() => server.resetHandlers())