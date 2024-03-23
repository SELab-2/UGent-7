import {Student} from '@/types/Student';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';

export function useStudents() {
    const students = ref<Student[]|null>(null);
    const student = ref<Student|null>(null);
    const toast = useToast();

    async function getStudentByID(id: number) {
        const endpoint = endpoints.students.retrieve.replace('{id}', id.toString());
        get<Student>(endpoint, student, Student.fromJSON, toast);
        console.log(student)
    }

    async function getStudents() {
        const endpoint = endpoints.students.index;
        getList<Student>(endpoint, students, Student.fromJSON, toast);
        console.log(students.value ? students.value.map((student, index) => `Student ${index + 1}: ${JSON.stringify(student)}`) : 'Students is null');
    }

    return {
        students,
        student,
        getStudentByID,
        getStudents
    };
}