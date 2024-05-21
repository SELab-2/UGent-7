import { Student } from '@/types/users/Student.ts';
import { Response } from '@/types/Response';
import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { get, getList, create, deleteId, deleteIdWithData } from '@/composables/services/helpers.ts';

interface StudentsState {
    students: Ref<Student[] | null>;
    student: Ref<Student | null>;
    response: Ref<Response | null>;
    getStudentByID: (id: string, init?: boolean) => Promise<void>;
    getStudents: () => Promise<void>;
    getStudentsByCourse: (courseId: string) => Promise<void>;
    getStudentsByGroup: (groupId: string) => Promise<void>;
    createStudent: (studentData: Student) => Promise<void>;
    deleteStudent: (id: string) => Promise<void>;
    studentJoinCourse: (courseId: string, studentId: string) => Promise<void>;
    studentLeaveCourse: (courseId: string, studentId: string) => Promise<void>;
    studentJoinGroup: (groupId: string, studentId: string) => Promise<void>;
    studentLeaveGroup: (groupId: string, studentId: string) => Promise<void>;
}

export function useStudents(): StudentsState {
    /* State */
    const students = ref<Student[] | null>(null);
    const student = ref<Student | null>(null);
    const response = ref<Response | null>(null);

    async function getStudentByID(id: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.students.retrieve.replace('{id}', id);
        await get<Student>(endpoint, student, Student.fromJSON, selfprocessError);
    }

    async function getStudents(selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.students.index;
        await getList<Student>(endpoint, students, Student.fromJSON, selfprocessError);
    }

    async function getStudentsByCourse(courseId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.students.byCourse.replace('{courseId}', courseId);
        await getList<Student>(endpoint, students, Student.fromJSON, selfprocessError);
    }

    async function getStudentsByGroup(groupId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.students.byGroup.replace('{groupId}', groupId);
        await getList<Student>(endpoint, students, Student.fromJSON, selfprocessError);
    }

    async function studentJoinCourse(courseId: string, studentId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.students.byCourse.replace('{courseId}', courseId);
        await create<Response>(endpoint, { student: studentId }, response, Response.fromJSON, undefined, selfprocessError);
    }

    async function studentLeaveCourse(courseId: string, studentId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.students.byCourse.replace('{courseId}', courseId);
        await deleteIdWithData<Response>(endpoint, { student: studentId }, response, Response.fromJSON, selfprocessError);
    }

    async function studentJoinGroup(groupId: string, studentId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.students.byGroup.replace('{groupId}', groupId);
        await create<Response>(endpoint, { student: studentId }, response, Response.fromJSON, undefined, selfprocessError);
    }

    async function studentLeaveGroup(groupId: string, studentId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.students.byGroup.replace('{groupId}', groupId);
        await deleteIdWithData<Response>(endpoint, { student: studentId }, response, Response.fromJSON, selfprocessError);
    }

    async function createStudent(studentData: Student, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.students.index;

        await create<Student>(
            endpoint,
            {
                user: studentData.id,
                student_id: studentData.student_id,
            },
            student,
            Student.fromJSON,
            undefined,
            selfprocessError
        );
    }

    async function deleteStudent(id: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.students.retrieve.replace('{id}', id);
        await deleteId<Student>(endpoint, student, Student.fromJSON, selfprocessError);
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
        studentLeaveGroup,
    };
}
