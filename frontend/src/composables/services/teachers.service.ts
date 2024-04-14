/* eslint-disable @typescript-eslint/no-unused-vars */
import { Teacher } from '@/types/users/Teacher.ts';
import { Response } from '@/types/Response';
import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { get, getList, create, deleteId, deleteIdWithData } from '@/composables/services/helpers.ts';
import { useCourses } from '@/composables/services/courses.service.ts';

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

    /* Nested state */
    const { courses, getCoursesByTeacher } = useCourses();

    async function getTeacherByID(id: string, init: boolean = false): Promise<void> {
        const endpoint = endpoints.teachers.retrieve.replace('{id}', id);
        await get<Teacher>(endpoint, teacher, Teacher.fromJSON);

        if (init) {
            await initTeacher(teacher.value);
        }
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

    async function createTeacher(teacherData: Teacher): Promise<void> {
        const endpoint = endpoints.teachers.index;
        await create<Teacher>(
            endpoint,
            {
                email: teacherData.email,
                first_name: teacherData.first_name,
                last_name: teacherData.last_name,
            },
            teacher,
            Teacher.fromJSON,
        );
    }

    async function deleteTeacher(id: string): Promise<void> {
        const endpoint = endpoints.students.retrieve.replace('{id}', id);
        await deleteId<Teacher>(endpoint, teacher, Teacher.fromJSON);
    }

    async function initTeacher(teacher: Teacher | null): Promise<void> {
        if (teacher !== null) {
            await getCoursesByTeacher(teacher.id);
            teacher.courses = courses.value ?? [];
        }
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
