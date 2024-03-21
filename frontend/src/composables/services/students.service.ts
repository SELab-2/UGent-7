import {Student} from '@/types/Students.ts';
import {ref} from 'vue';
import axios from 'axios';
import {endpoints} from '@/config/endpoints.ts';

export function useStudents() {
    const students = ref<Student[]|null>(null);
    const student = ref<Student|null>(null);

    async function getStudentByID(id: number) {
        const endpoint = endpoints.students.retrieve.replace('{id}', id.toString());

        axios.get(endpoint).then(response => {
            student.value = Student.fromJSON(response.data);
        }).catch(error => {
            console.log(error.data);
        });

        console.log(Student)
    }

    return {
        students,
        student,
        getStudentByID
    };
}