import {Student} from '@/types/Student';
import { Response } from '@/types/Response';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id, delete_id_with_data } from '@/composables/services/helpers.ts';

export function useStudents() {
    const students = ref<Student[]|null>(null);
    const student = ref<Student|null>(null);
    const response = ref<Response|null>(null);

    async function getStudentByID(id: string) {
        const endpoint = endpoints.students.retrieve.replace('{id}', id);
        await get<Student>(endpoint, student, Student.fromJSON);
    }

    async function getStudents() {
        const endpoint = endpoints.students.index;
        await getList<Student>(endpoint, students, Student.fromJSON);
    }

    async function getStudentsbyCourse(course_id: string) {
        const endpoint = endpoints.students.byCourse.replace('{course_id}', course_id);
        await getList<Student>(endpoint, students, Student.fromJSON);
    }

    async function getStudentsbyGroup(group_id: string) {
        const endpoint = endpoints.students.byGroup.replace('{group_id}', group_id);
        await getList<Student>(endpoint, students, Student.fromJSON);
    }

    async function studentJoinCourse(course_id: string, student_id: string) {
        const endpoint = endpoints.students.byCourse.replace('{course_id}', course_id);
        await create<Response>(endpoint, {student_id: student_id}, response, Response.fromJSON);
    }

    async function studentLeaveCourse(course_id: string, student_id: string) {
        const endpoint = endpoints.students.byCourse.replace('{course_id}', course_id);
        await delete_id_with_data<Response>(endpoint, {student_id: student_id}, response, Response.fromJSON);
    }

    async function studentJoinGroup(group_id: string, student_id: string) {
        const endpoint = endpoints.students.byGroup.replace('{group_id}', group_id);
        await create<Response>(endpoint, {student_id: student_id}, response, Response.fromJSON);
    }

    async function studentLeaveGroup(group_id: string, student_id: string) {
        const endpoint = endpoints.students.byGroup.replace('{group_id}', group_id);
        await delete_id_with_data<Response>(endpoint, {student_id: student_id}, response, Response.fromJSON);
    }

    async function createStudent(student_data: Student) {
        const endpoint = endpoints.students.index;
        await create<Student>(endpoint, 
            {
                email:student_data.email,
                first_name:student_data.first_name,
                last_name: student_data.last_name
            },
         student, Student.fromJSON);
    }

    async function deleteStudent(id: string) {
        const endpoint = endpoints.students.retrieve.replace('{id}', id);
        await delete_id<Student>(endpoint, student, Student.fromJSON);
    }

    return {
        students,
        student,

        response,

        getStudentByID,
        getStudents,
        getStudentsbyCourse,
        getStudentsbyGroup,

        createStudent,
        deleteStudent,

        studentJoinCourse,
        studentLeaveCourse,
        studentJoinGroup,
        studentLeaveGroup
    };
}