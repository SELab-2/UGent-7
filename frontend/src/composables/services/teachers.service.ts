import {Teacher} from '@/types/Teacher.ts';
import { Response } from '@/types/Response';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id, delete_id_with_data } from '@/composables/services/helpers.ts';

export function useTeacher() {
    const teachers = ref<Teacher[]|null>(null);
    const teacher = ref<Teacher|null>(null);
    const response = ref<Response|null>(null);

    async function getTeacherByID(id: string) {
        const endpoint = endpoints.teachers.retrieve.replace('{id}', id);
        await get<Teacher>(endpoint, teacher, Teacher.fromJSON);
    }

    async function getTeacherByCourse(course_id: string) {
        const endpoint = endpoints.teachers.byCourse.replace('{course_id}', course_id);
        await get<Teacher>(endpoint, teacher, Teacher.fromJSON);
    }

    async function getTeachers() {
        const endpoint = endpoints.teachers.index;
        await getList<Teacher>(endpoint, teachers, Teacher.fromJSON);
    }

    async function teacherJoinCourse(course_id: string, teacher_id: string) {
        const endpoint = endpoints.teachers.byCourse.replace('{course_id}', course_id);
        await create<Response>(endpoint, {teacher_id: teacher_id}, response, Response.fromJSON);
    }

    async function teacherLeaveCourse(course_id: string, teacher_id: string) {
        const endpoint = endpoints.teachers.byCourse.replace('{course_id}', course_id);
        await delete_id_with_data<Response>(endpoint, {teacher_id: teacher_id}, response, Response.fromJSON);
    }

    async function createTeacher(teacher_data: any) {
        const endpoint = endpoints.teachers.index;
        await create<Teacher>(endpoint, teacher_data, teacher, Teacher.fromJSON);
    }

    async function deleteTeacher(id: string) {
        const endpoint = endpoints.students.retrieve.replace('{id}', id);
        await delete_id<Teacher>(endpoint, teacher, Teacher.fromJSON);
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

        teacherJoinCourse,
        teacherLeaveCourse
    };
}