import { Student } from '@/types/users/Student.ts';
import { Response } from '@/types/Response';
import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { get, getList, create, deleteId, deleteIdWithData } from '@/composables/services/helpers.ts';
import { useCourses } from '@/composables/services/courses.service.ts';

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

    /* Nested state */
    const { courses, getCoursesByStudent } = useCourses();

    async function getStudentByID(id: string, init: boolean = false): Promise<void> {
        const endpoint = endpoints.students.retrieve.replace('{id}', id);
        await get<Student>(endpoint, student, Student.fromJSON);

        if (init) {
            await initStudent(student.value);
        }
    }

    async function getStudents(): Promise<void> {
        const endpoint = endpoints.students.index;
        await getList<Student>(endpoint, students, Student.fromJSON);
    }

    async function getStudentsByCourse(courseId: string): Promise<void> {
        const endpoint = endpoints.students.byCourse.replace('{courseId}', courseId);
        await getList<Student>(endpoint, students, Student.fromJSON);
    }

    async function getStudentsByGroup(groupId: string): Promise<void> {
        const endpoint = endpoints.students.byGroup.replace('{groupId}', groupId);
        await getList<Student>(endpoint, students, Student.fromJSON);
    }

    async function studentJoinCourse(courseId: string, studentId: string): Promise<void> {
        const endpoint = endpoints.students.byCourse.replace('{courseId}', courseId);
        await create<Response>(endpoint, { student: studentId }, response, Response.fromJSON);
    }

    async function studentLeaveCourse(courseId: string, studentId: string): Promise<void> {
        const endpoint = endpoints.students.byCourse.replace('{courseId}', courseId);
        await deleteIdWithData<Response>(endpoint, { student: studentId }, response, Response.fromJSON);
    }

    async function studentJoinGroup(groupId: string, studentId: string): Promise<void> {
        const endpoint = endpoints.students.byGroup.replace('{groupId}', groupId);
        await create<Response>(endpoint, { student: studentId }, response, Response.fromJSON);
    }

    async function studentLeaveGroup(groupId: string, studentId: string): Promise<void> {
        const endpoint = endpoints.students.byGroup.replace('{groupId}', groupId);
        await deleteIdWithData<Response>(endpoint, { student: studentId }, response, Response.fromJSON);
    }

    async function createStudent(studentData: Student): Promise<void> {
        const endpoint = endpoints.students.index;

        await create<Student>(
            endpoint,
            {
                email: studentData.email,
                first_name: studentData.first_name,
                last_name: studentData.last_name,
            },
            student,
            Student.fromJSON,
        );
    }

    async function deleteStudent(id: string): Promise<void> {
        const endpoint = endpoints.students.retrieve.replace('{id}', id);
        await deleteId<Student>(endpoint, student, Student.fromJSON);
    }

    async function initStudent(student: Student | null): Promise<void> {
        if (student !== null) {
            await getCoursesByStudent(student.id);
            student.courses = courses.value ?? [];
        }
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
