import {Course} from '@/types/Course.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList } from '@/composables/services/helpers.ts';

export function useCourses() {
    const courses = ref<Course[]|null>(null);
    const course = ref<Course|null>(null);

    async function getCourseByID(id: number) {
        const endpoint = endpoints.courses.retrieve.replace('{id}', id.toString());
        get<Course>(endpoint, course, Course.fromJSON);
        console.log(course.value);
    }

    async function getCourses() {
        const endpoint = endpoints.courses.index;
        getList<Course>(endpoint, courses, Course.fromJSON);
        console.log(courses.value ? courses.value.map((course, index) => `Course ${index + 1}: ${JSON.stringify(course)}`) : 'Courses is null');
    }

    async function getCoursesByStudent(student_id: number) {
        const endpoint = endpoints.courses.byStudent.replace('{student_id}', student_id.toString());
        getList<Course>(endpoint, courses, Course.fromJSON);
        console.log(courses.value ? courses.value.map((course, index) => `Course ${index + 1}: ${JSON.stringify(course)}`) : 'Courses is null');
    }

    return {
        courses,
        course,
        getCourseByID,
        getCourses,
        getCoursesByStudent
    };
}