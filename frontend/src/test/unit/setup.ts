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
        course:"1",
        name: "sel2",
        description: "this is a test",
        visible: true,
        archived: false,
        locked_groups: false,
        start_date: new Date("July 21, 2024 01:15:00"),
        deadline: new Date("July 23, 2024 01:15:00"),
        max_score: 100,
        score_visible: true,
        group_size: 8
    },
    {
        id: 1,
        course: "1",
        name: "sel3",
        description: "make a project",
        visible: true,
        archived: false,
        locked_groups: false,
        start_date: new Date("July 21, 2024 01:15:00"),
        deadline: new Date("July 23, 2024 01:15:00"),
        max_score: 20,
        score_visible: false,
        group_size: 3
      }
]

const courses = [
    {
    "id": "1",
    "teachers": "https://localhost/api/courses/1/teachers/",
    "assistants": "https://localhost/api/courses/1/assistants/",
    "students": "https://localhost/api/courses/1/students/",
    "projects": "https://localhost/api/courses/1/projects/",
    "parent_course": null,
    "name": "Math",
    "academic_startyear": 2023,
    "description": "Math course"
  },
  {
    "id": "2",
    "teachers": [],
    "assistants": [],
    "students": [],
    "projects": [],
    "parent_course": "3",
    "name": "Sel2",
    "academic_startyear": 2023,
    "description": "Software course"
  },
  {
    "id": "3",
    "teachers": [],
    "assistants": [],
    "students": [],
    "projects": [],
    "parent_course": null,
    "name": "Sel1",
    "academic_startyear": 2022,
    "description": "Software course"
  },
  {
    "id": "12",
    "teachers": [],
    "assistants": [],
    "students": [],
    "projects": [],
    "parent_course": "1",
    "name": "Math",
    "academic_startyear": 2024,
    "description": "Math course"
  },
  {
    "id": "13",
    "teachers": [],
    "assistants": [],
    "students": [],
    "projects": [],
    "parent_course": "12",
    "name": "Math",
    "academic_startyear": 2025,
    "description": "Math course"
  },
  {
    "id": "14",
    "teachers": [],
    "assistants": [],
    "students": [],
    "projects": [],
    "parent_course": null,
    "name": "Club brugge",
    "academic_startyear": 2023,
    "description": null
  },
  {
    "id": "15",
    "teachers": [],
    "assistants": [],
    "students": [],
    "projects": [],
    "parent_course": null,
    "name": "vergeet barbara",
    "academic_startyear": 2023,
    "description": null
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
    http.get(baseUrl + endpoints.projects.retrieve.replace('{id}', ':id'),
        ({ params }) => {
            return HttpResponse.json(projects.find(x => x.id == params.id))
        }
    ),
    http.get(baseUrl + endpoints.courses.retrieve.replace('{id}', ':id'),
    ({ params }) => {
        return HttpResponse.json(courses.find(x => x.id == params.id))
    }
    ),
    http.get(baseUrl + endpoints.groups.byProject.replace('{project_id}', ':id'),
        ({ params }) => {
            return HttpResponse.json(groups.filter(x => x.project == params.id))
        }
    ),
    http.get(baseUrl + endpoints.projects.byCourse.replace('{course_id}', ':id'),
        ({ params }) => {
            return HttpResponse.json(projects.filter(x => x.course == params.id))
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
    ),
    http.get(baseUrl + endpoints.courses.index,
        ({}) => {
            return HttpResponse.json(courses)
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