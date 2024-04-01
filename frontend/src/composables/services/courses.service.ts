import { Course } from '@/types/Course.ts'
import { ref } from 'vue'
import { endpoints } from '@/config/endpoints.ts'
import {
    get,
    getList,
    create,
    deleteId
} from '@/composables/services/helpers.ts'

export function useCourses() {
    const courses = ref<Course[] | null>(null)
    const course = ref<Course | null>(null)

    async function getCourseByID(id: string) {
        const endpoint = endpoints.courses.retrieve.replace('{id}', id)
        await get<Course>(endpoint, course, Course.fromJSON)
    }

    async function getCourses() {
        const endpoint = endpoints.courses.index
        await getList<Course>(endpoint, courses, Course.fromJSON)
    }

    async function getCoursesByStudent(studentId: string) {
        const endpoint = endpoints.courses.byStudent.replace(
            '{studentId}',
            studentId
        )
        await getList<Course>(endpoint, courses, Course.fromJSON)
    }

    async function getCoursesByTeacher(teacherId: string) {
        const endpoint = endpoints.courses.byTeacher.replace(
            '{teacherId}',
            teacherId
        )
        await getList<Course>(endpoint, courses, Course.fromJSON)
    }

    async function getCourseByAssistant(assistantId: string) {
        const endpoint = endpoints.courses.byAssistant.replace(
            '{assistantId}',
            assistantId
        )
        await getList<Course>(endpoint, courses, Course.fromJSON)
    }

    async function createCourse(courseData: Course) {
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

    async function cloneCourse(courseId: string, cloneAssistants: boolean) {
        const endpoint = endpoints.courses.clone.replace('{courseId}', courseId)
        await create<Course>(
            endpoint,
            { cloneAssistants: cloneAssistants.toString() },
            course,
            Course.fromJSON
        )
    }

    async function deleteCourse(id: string) {
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
