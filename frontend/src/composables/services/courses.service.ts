import { Course } from '@/types/Course.ts'
import { type Ref, ref } from 'vue'
import { endpoints } from '@/config/endpoints.ts'
import {
    get,
    getList,
    create,
    deleteId
} from '@/composables/services/helpers.ts'

interface CoursesState {
    courses: Ref<Course[] | null>
    course: Ref<Course | null>
    getCourseByID: (id: string) => Promise<void>
    getCourses: () => Promise<void>
    getCoursesByStudent: (studentId: string) => Promise<void>
    getCoursesByTeacher: (teacherId: string) => Promise<void>
    getCourseByAssistant: (assistantId: string) => Promise<void>
    createCourse: (courseData: Course) => Promise<void>
    cloneCourse: (courseId: string, cloneAssistants: boolean) => Promise<void>
    deleteCourse: (id: string) => Promise<void>
}

export function useCourses(): CoursesState {
    const courses = ref<Course[] | null>(null)
    const course = ref<Course | null>(null)

    async function getCourseByID(id: string): Promise<void> {
        const endpoint = endpoints.courses.retrieve.replace('{id}', id)
        await get<Course>(endpoint, course, Course.fromJSON)
    }

    async function getCourses(): Promise<void> {
        const endpoint = endpoints.courses.index
        await getList<Course>(endpoint, courses, Course.fromJSON)
    }

    async function getCoursesByStudent(studentId: string): Promise<void> {
        const endpoint = endpoints.courses.byStudent.replace(
            '{studentId}',
            studentId
        )
        await getList<Course>(endpoint, courses, Course.fromJSON)
    }

    async function getCoursesByTeacher(teacherId: string): Promise<void> {
        const endpoint = endpoints.courses.byTeacher.replace(
            '{teacherId}',
            teacherId
        )
        await getList<Course>(endpoint, courses, Course.fromJSON)
    }

    async function getCourseByAssistant(assistantId: string): Promise<void> {
        const endpoint = endpoints.courses.byAssistant.replace(
            '{assistantId}',
            assistantId
        )
        await getList<Course>(endpoint, courses, Course.fromJSON)
    }

    async function createCourse(courseData: Course): Promise<void> {
        const endpoint = endpoints.courses.index
        await create<Course>(
            endpoint,
            {
                name: courseData.name,
                description: courseData.description,
                academic_startyear: courseData.academic_startyear
            },
            course,
            Course.fromJSON
        )
    }

    async function cloneCourse(
        courseId: string,
        cloneAssistants: boolean
    ): Promise<void> {
        const endpoint = endpoints.courses.clone.replace('{courseId}', courseId)
        await create<Course>(
            endpoint,
            { cloneAssistants: cloneAssistants.toString() },
            course,
            Course.fromJSON
        )
    }

    async function deleteCourse(id: string): Promise<void> {
        const endpoint = endpoints.courses.retrieve.replace('{id}', id)
        await deleteId<Course>(endpoint, course, Course.fromJSON)
    }

    return {
        courses,
        course,

        getCourseByID,
        getCourses,
        getCoursesByStudent,
        getCoursesByTeacher,
        getCourseByAssistant,

        createCourse,
        cloneCourse,
        deleteCourse
    }
}
