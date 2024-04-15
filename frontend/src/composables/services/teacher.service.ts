/* eslint-disable @typescript-eslint/no-unused-vars */
import { type User } from '@/types/users/User.ts';
import { Teacher } from '@/types/users/Teacher.ts';
import { Response } from '@/types/Response';
import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { get, getList, create, deleteId, deleteIdWithData } from '@/composables/services/helpers.ts';

interface TeacherState {
    teachers: Ref<Teacher[] | null>;
    teacher: Ref<Teacher | null>;
    response: Ref<Response | null>;
    getTeacherByID: (id: string, init?: boolean) => Promise<void>;
    getTeachersByCourse: (courseId: string) => Promise<void>;
    getTeachers: () => Promise<void>;
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

    async function getTeacherByID(id: string): Promise<void> {
        const endpoint = endpoints.teachers.retrieve.replace('{id}', id);
        await get<Teacher>(endpoint, teacher, Teacher.fromJSON);
    }

    async function getTeachersByCourse(courseId: string): Promise<void> {
        const endpoint = endpoints.teachers.byCourse.replace('{courseId}', courseId);
        await getList<Teacher>(endpoint, teachers, Teacher.fromJSON);
    }

    async function getTeachers(): Promise<void> {
        const endpoint = endpoints.teachers.index;
        await getList<Teacher>(endpoint, teachers, Teacher.fromJSON);
    }

    async function teacherJoinCourse(courseId: string, teacherId: string): Promise<void> {
        const endpoint = endpoints.teachers.byCourse.replace('{courseId}', courseId);
        await create<Response>(endpoint, { teacherId }, response, Response.fromJSON);
    }

    async function teacherLeaveCourse(courseId: string, teacherId: string): Promise<void> {
        const endpoint = endpoints.teachers.byCourse.replace('{courseId}', courseId);
        await deleteIdWithData<Response>(endpoint, { teacherId }, response, Response.fromJSON);
    }

    async function createTeacher(user: User): Promise<void> {
        const endpoint = endpoints.teachers.index;
        await create<Teacher>(
            endpoint,
            {
                id: user.id,
            },
            teacher,
            Teacher.fromJSON,
        );
    }

    async function deleteTeacher(id: string): Promise<void> {
        const endpoint = endpoints.students.retrieve.replace('{id}', id);
        await deleteId<Teacher>(endpoint, teacher, Teacher.fromJSON);
    }

    return {
        teachers,
        teacher,
        response,

        getTeacherByID,
        getTeachersByCourse,
        getTeachers,

        createTeacher,
        deleteTeacher,

        teacherJoinCourse,
        teacherLeaveCourse,
    };
}
