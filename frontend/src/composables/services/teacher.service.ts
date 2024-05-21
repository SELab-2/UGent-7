/* eslint-disable @typescript-eslint/no-unused-vars */
import { type User } from '@/types/users/User.ts';
import { Teacher } from '@/types/users/Teacher.ts';
import { Response } from '@/types/Response';
import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { get, getList, create, deleteId, deleteIdWithData, getPaginatedList } from '@/composables/services/helpers.ts';
import { type PaginatorResponse } from '@/types/filter/Paginator.ts';
import { type Filter } from '@/types/filter/Filter.ts';

interface TeacherState {
    teachers: Ref<Teacher[] | null>;
    teacher: Ref<Teacher | null>;
    response: Ref<Response | null>;
    teacherPagination: Ref<PaginatorResponse<Teacher> | null>;
    getTeacherByID: (id: string, init?: boolean) => Promise<void>;
    getTeachersByCourse: (courseId: string) => Promise<void>;
    getTeachers: () => Promise<void>;
    searchTeachers: (filters: Filter, page: number, pageSize: number) => Promise<void>;
    teacherJoinCourse: (courseId: string, teacherId: string) => Promise<void>;
    teacherLeaveCourse: (courseId: string, teacherId: string) => Promise<void>;
    createTeacher: (teacherData: Teacher) => Promise<void>;
    deleteTeacher: (id: string) => Promise<void>;
}

export function useTeacher(): TeacherState {
    /* State */
    const teachers = ref<Teacher[] | null>(null);
    const teacher = ref<Teacher | null>(null);
    const response = ref<Response | null>(null);
    const teacherPagination = ref<PaginatorResponse<Teacher> | null>(null);

    async function getTeacherByID(id: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.teachers.retrieve.replace('{id}', id);
        await get<Teacher>(endpoint, teacher, Teacher.fromJSON, selfprocessError);
    }

    async function getTeachersByCourse(courseId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.teachers.byCourse.replace('{courseId}', courseId);
        await getList<Teacher>(endpoint, teachers, Teacher.fromJSON, selfprocessError);
    }

    async function getTeachers(selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.teachers.index;
        await getList<Teacher>(endpoint, teachers, Teacher.fromJSON, selfprocessError);
    }

    async function searchTeachers(filters: Filter, page: number, pageSize: number, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.teachers.search;
        await getPaginatedList<Teacher>(endpoint, filters, page, pageSize, teacherPagination, Teacher.fromJSON, selfprocessError);
    }

    async function teacherJoinCourse(courseId: string, teacherId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.teachers.byCourse.replace('{courseId}', courseId);
        await create<Response>(endpoint, { teacher: teacherId }, response, Response.fromJSON, undefined, selfprocessError);
    }

    async function teacherLeaveCourse(courseId: string, teacherId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.teachers.byCourse.replace('{courseId}', courseId);
        await deleteIdWithData<Response>(endpoint, { teacher: teacherId }, response, Response.fromJSON, selfprocessError);
    }

    async function createTeacher(user: User, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.teachers.index;
        await create<Teacher>(
            endpoint,
            {
                user: user.id,
            },
            teacher,
            Teacher.fromJSON,
            undefined,
            selfprocessError
        );
    }

    async function deleteTeacher(id: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.teachers.retrieve.replace('{id}', id);
        await deleteId<Teacher>(endpoint, teacher, Teacher.fromJSON, selfprocessError);
    }

    return {
        teachers,
        teacher,
        response,
        teacherPagination,

        getTeacherByID,
        getTeachersByCourse,
        getTeachers,
        searchTeachers,

        createTeacher,
        deleteTeacher,

        teacherJoinCourse,
        teacherLeaveCourse,
    };
}
