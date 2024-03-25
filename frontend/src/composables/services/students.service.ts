import {Student} from '@/types/Student';
import { Response } from '@/types/Response';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';

export function useStudents() {
    const students = ref<Student[]|null>(null);
    const student = ref<Student|null>(null);
    const response = ref<Response|null>(null);
    const toast = useToast();

    async function getStudentByID(id: number) {
        const endpoint = endpoints.students.retrieve.replace('{id}', id.toString());
        get<Student>(endpoint, student, Student.fromJSON, toast);
    }

    async function getStudents() {
        const endpoint = endpoints.students.index;
        getList<Student>(endpoint, students, Student.fromJSON, toast);
    }

    async function getStudentsbyCourse(course_id: string) {
        const endpoint = endpoints.students.byCourse.replace('{course_id}', course_id);
        getList<Student>(endpoint, students, Student.fromJSON, toast);
    }

    async function getStudentsbyGroup(group_id: string) {
        const endpoint = endpoints.students.byGroup.replace('{group_id}', group_id);
        getList<Student>(endpoint, students, Student.fromJSON, toast);
    }

    async function studentJoinCourse(course_id: string, student_id: string) {
        const endpoint = endpoints.students.byCourse.replace('{course_id}', course_id);
        create<Response>(endpoint, {student_id: student_id}, response, Response.fromJSON, toast);
    }

    async function studentJoinGroup(group_id: string, student_id: string) {
        const endpoint = endpoints.students.byGroup.replace('{group_id}', group_id);
        create<Response>(endpoint, {student_id: student_id}, response, Response.fromJSON, toast);
    }

    async function createStudent(student_data: any) {
        const endpoint = endpoints.students.index;
        create<Student>(endpoint, student_data, student, Student.fromJSON, toast);
    }

    async function deleteStudent(id: string) {
        const endpoint = endpoints.students.retrieve.replace('{id}', id.toString());
        delete_id<Student>(endpoint, student, Student.fromJSON, toast);
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
        studentJoinGroup
    };
}