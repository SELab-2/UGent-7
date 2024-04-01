import { Student } from '@/types/Student'
import { Response } from '@/types/Response'
import { type Ref, ref } from 'vue'
import { endpoints } from '@/config/endpoints.ts'
import {
    get,
    getList,
    create,
    deleteId,
    deleteIdWithData
} from '@/composables/services/helpers.ts'

interface StudentsState {
    students: Ref<Student[] | null>
    student: Ref<Student | null>
    response: Ref<Response | null>
    getStudentByID: (id: string) => Promise<void>
    getStudents: () => Promise<void>
    getStudentsByCourse: (courseId: string) => Promise<void>
    getStudentsByGroup: (groupId: string) => Promise<void>
    createStudent: (studentData: Student) => Promise<void>
    deleteStudent: (id: string) => Promise<void>
    studentJoinCourse: (courseId: string, studentId: string) => Promise<void>
    studentLeaveCourse: (courseId: string, studentId: string) => Promise<void>
    studentJoinGroup: (groupId: string, studentId: string) => Promise<void>
    studentLeaveGroup: (groupId: string, studentId: string) => Promise<void>
}

export function useStudents(): StudentsState {
    const students = ref<Student[] | null>(null)
    const student = ref<Student | null>(null)
    const response = ref<Response | null>(null)

    async function getStudentByID(id: string): Promise<void> {
        const endpoint = endpoints.students.retrieve.replace('{id}', id)
        await get<Student>(endpoint, student, Student.fromJSON)
    }

    async function getStudents(): Promise<void> {
        const endpoint = endpoints.students.index
        await getList<Student>(endpoint, students, Student.fromJSON)
    }

    async function getStudentsByCourse(courseId: string): Promise<void> {
        const endpoint = endpoints.students.byCourse.replace(
            '{courseId}',
            courseId
        )
        await getList<Student>(endpoint, students, Student.fromJSON)
    }

    async function getStudentsByGroup(groupId: string): Promise<void> {
        const endpoint = endpoints.students.byGroup.replace(
            '{groupId}',
            groupId
        )
        await getList<Student>(endpoint, students, Student.fromJSON)
    }

    async function studentJoinCourse(
        courseId: string,
        studentId: string
    ): Promise<void> {
        const endpoint = endpoints.students.byCourse.replace(
            '{courseId}',
            courseId
        )
        await create<Response>(
            endpoint,
            { studentId },
            response,
            Response.fromJSON
        )
    }

    async function studentLeaveCourse(
        courseId: string,
        studentId: string
    ): Promise<void> {
        const endpoint = endpoints.students.byCourse.replace(
            '{courseId}',
            courseId
        )
        await deleteIdWithData<Response>(
            endpoint,
            { studentId },
            response,
            Response.fromJSON
        )
    }

    async function studentJoinGroup(
        groupId: string,
        studentId: string
    ): Promise<void> {
        const endpoint = endpoints.students.byGroup.replace(
            '{groupId}',
            groupId
        )
        await create<Response>(
            endpoint,
            { studentId },
            response,
            Response.fromJSON
        )
    }

    async function studentLeaveGroup(
        groupId: string,
        studentId: string
    ): Promise<void> {
        const endpoint = endpoints.students.byGroup.replace(
            '{groupId}',
            groupId
        )
        await deleteIdWithData<Response>(
            endpoint,
            { studentId },
            response,
            Response.fromJSON
        )
    }

    async function createStudent(studentData: Student): Promise<void> {
        const endpoint = endpoints.students.index
        await create<Student>(
            endpoint,
            {
                email: studentData.email,
                first_name: studentData.first_name,
                last_name: studentData.last_name
            },
            student,
            Student.fromJSON
        )
    }

    async function deleteStudent(id: string): Promise<void> {
        const endpoint = endpoints.students.retrieve.replace('{id}', id)
        await deleteId<Student>(endpoint, student, Student.fromJSON)
    }

    return {
        students,
        student,

        response,

        getStudentByID,
        getStudents,
        getStudentsByCourse,
        getStudentsByGroup,

        createStudent,
        deleteStudent,

        studentJoinCourse,
        studentLeaveCourse,
        studentJoinGroup,
        studentLeaveGroup
    }
}
