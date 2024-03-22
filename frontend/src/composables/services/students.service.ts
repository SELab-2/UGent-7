import {Student} from '@/types/Student';
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

        console.log(student)
    }

    async function getStudents() {
        const endpoint = endpoints.students.index;

        axios.get(endpoint).then(response => {
            students.value = response.data.map((studentData: Student) => Student.fromJSON(studentData));
        }).catch(error => {
            console.log(error.data);
        });

        console.log(students.value ? students.value.map((student, index) => `Student ${index + 1}: ${JSON.stringify(student)}`) : 'Students is null');
    }

    return {
        students,
        student,
        getStudentByID,
        getStudents
    };
}