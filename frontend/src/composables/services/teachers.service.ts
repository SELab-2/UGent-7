import {Teacher} from '@/types/Teacher.ts';
import { Response } from '@/types/Response';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';
import {ComposerTranslation} from "vue-i18n";

export function useTeacher() {
    const teachers = ref<Teacher[]|null>(null);
    const teacher = ref<Teacher|null>(null);
    const response = ref<Response|null>(null);
    const toast = useToast();

    async function getTeacherByID(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.teachers.retrieve.replace('{id}', id);
        get<Teacher>(endpoint, teacher, Teacher.fromJSON, toast, t);
    }

    async function getTeacherByCourse(course_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.teachers.byCourse.replace('{course_id}', course_id);
        get<Teacher>(endpoint, teacher, Teacher.fromJSON, toast, t);
    }

    async function getTeachers(t: ComposerTranslation) {
        const endpoint = endpoints.teachers.index;
        getList<Teacher>(endpoint, teachers, Teacher.fromJSON, toast, t);
    }

    async function teacherJoinCourse(course_id: string, teacher_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.teachers.byCourse.replace('{course_id}', course_id);
        create<Response>(endpoint, {teacher_id: teacher_id}, response, Response.fromJSON, toast, t);
    }

    async function createTeacher(teacher_data: any, t: ComposerTranslation) {
        const endpoint = endpoints.teachers.index;
        create<Teacher>(endpoint, teacher_data, teacher, Teacher.fromJSON, toast, t);
    }

    async function deleteTeacher(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.students.retrieve.replace('{id}', id);
        delete_id<Teacher>(endpoint, teacher, Teacher.fromJSON, toast, t);
    }

    return {
        teachers,
        teacher,
        response,

        getTeacherByID,
        getTeacherByCourse,
        getTeachers,

        createTeacher,
        deleteTeacher,

        teacherJoinCourse
    };
}