import {Teacher} from '@/types/Teacher.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';

export function useTeacher() {
    const teachers = ref<Teacher[]|null>(null);
    const teacher = ref<Teacher|null>(null);
    const toast = useToast();

    async function getTeacherByID(id: number) {
        const endpoint = endpoints.teachers.retrieve.replace('{id}', id.toString());
        get<Teacher>(endpoint, teacher, Teacher.fromJSON, toast);
        console.log(teacher)
    }

    async function getTeachers() {
        const endpoint = endpoints.teachers.index;
        getList<Teacher>(endpoint, teachers, Teacher.fromJSON, toast);
        console.log(teachers.value ? teachers.value.map((teacher, index) => `Teacher ${index + 1}: ${JSON.stringify(teacher)}`) : 'Teachers is null');
    }

    async function createTeacher(teacher_data: any) {
        const endpoint = endpoints.teachers.index;
        create<Teacher>(endpoint, teacher_data, teacher, Teacher.fromJSON, toast);
    }

    async function deleteTeacher(id: string) {
        const endpoint = endpoints.students.retrieve.replace('{id}', id.toString());
        delete_id<Teacher>(endpoint, teacher, Teacher.fromJSON, toast);
    }

    return {
        teachers,
        teacher,
        getTeacherByID,
        getTeachers,

        createTeacher,
        deleteTeacher
    };
}