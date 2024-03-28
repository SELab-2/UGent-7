import {Student} from '@/types/Student';
import { Response } from '@/types/Response';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id, delete_id_with_data } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';
import {ComposerTranslation} from "vue-i18n";

export function useStudents() {
    const students = ref<Student[]|null>(null);
    const student = ref<Student|null>(null);
    const response = ref<Response|null>(null);
    const toast = useToast();

    async function getStudentByID(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.students.retrieve.replace('{id}', id);
        get<Student>(endpoint, student, Student.fromJSON, toast, t);
    }

    async function getStudents(t: ComposerTranslation) {
        const endpoint = endpoints.students.index;
        getList<Student>(endpoint, students, Student.fromJSON, toast, t);
    }

    async function getStudentsByCourse(course_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.students.byCourse.replace('{course_id}', course_id);
        getList<Student>(endpoint, students, Student.fromJSON, toast, t);
    }

    async function getStudentsByGroup(group_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.students.byGroup.replace('{group_id}', group_id);
        await getList<Student>(endpoint, students, Student.fromJSON, toast, t);
    }

    async function studentJoinCourse(course_id: string, student_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.students.byCourse.replace('{course_id}', course_id);
        create<Response>(endpoint, {student_id: student_id}, response, Response.fromJSON, toast, t);
    }

    async function studentLeaveCourse(course_id: string, student_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.students.byCourse.replace('{course_id}', course_id);
        delete_id_with_data<Response>(endpoint, {student_id: student_id}, response, Response.fromJSON, toast, t);
    }

    async function studentJoinGroup(group_id: string, student_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.students.byGroup.replace('{group_id}', group_id);
        create<Response>(endpoint, {student_id: student_id}, response, Response.fromJSON, toast, t);
    }

    async function studentLeaveGroup(group_id: string, student_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.students.byGroup.replace('{group_id}', group_id);
        delete_id_with_data<Response>(endpoint, {student_id: student_id}, response, Response.fromJSON, toast, t);
    }

    async function createStudent(student_data: any, t: ComposerTranslation) {
        const endpoint = endpoints.students.index;
        create<Student>(endpoint, student_data, student, Student.fromJSON, toast, t);
    }

    async function deleteStudent(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.students.retrieve.replace('{id}', id);
        delete_id<Student>(endpoint, student, Student.fromJSON, toast, t);
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
    };
}