import {Student} from '@/types/Student';
import { Response } from '@/types/Response';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id, delete_id_with_data } from '@/composables/services/helpers.ts';
import {ComposerTranslation} from "vue-i18n";

export function useStudents() {
    const students = ref<Student[]|null>(null);
    const student = ref<Student|null>(null);
    const response = ref<Response|null>(null);

    async function getStudentByID(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.students.retrieve.replace('{id}', id);
        await get<Student>(endpoint, student, Student.fromJSON, t);
    }

    async function getStudents(t: ComposerTranslation) {
        const endpoint = endpoints.students.index;
        await getList<Student>(endpoint, students, Student.fromJSON, t);
    }

    async function getStudentsbyCourse(course_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.students.byCourse.replace('{course_id}', course_id);
        await getList<Student>(endpoint, students, Student.fromJSON, t);
    }

    async function getStudentsbyGroup(group_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.students.byGroup.replace('{group_id}', group_id);
        await getList<Student>(endpoint, students, Student.fromJSON, t);
    }

    async function studentJoinCourse(course_id: string, student_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.students.byCourse.replace('{course_id}', course_id);
        await create<Response>(endpoint, {student_id: student_id}, response, Response.fromJSON, t);
    }

    async function studentLeaveCourse(course_id: string, student_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.students.byCourse.replace('{course_id}', course_id);
        await delete_id_with_data<Response>(endpoint, {student_id: student_id}, response, Response.fromJSON, t);
    }

    async function studentJoinGroup(group_id: string, student_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.students.byGroup.replace('{group_id}', group_id);
        await create<Response>(endpoint, {student_id: student_id}, response, Response.fromJSON, t);
    }

    async function studentLeaveGroup(group_id: string, student_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.students.byGroup.replace('{group_id}', group_id);
        await delete_id_with_data<Response>(endpoint, {student_id: student_id}, response, Response.fromJSON, t);
    }

    async function createStudent(student_data: any, t: ComposerTranslation) {
        const endpoint = endpoints.students.index;
        await create<Student>(endpoint, student_data, student, Student.fromJSON, t);
    }

    async function deleteStudent(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.students.retrieve.replace('{id}', id);
        await delete_id<Student>(endpoint, student, Student.fromJSON, t);
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