import {Course} from '@/types/Course.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';

export function useCourses() {
    const courses = ref<Course[]|null>(null);
    const course = ref<Course|null>(null);
    const toast = useToast();

    async function getCourseByID(id: number) {
        const endpoint = endpoints.courses.retrieve.replace('{id}', id.toString());
        get<Course>(endpoint, course, Course.fromJSON, toast);
        console.log(course.value);
    }

    async function getCourses() {
        const endpoint = endpoints.courses.index;
        getList<Course>(endpoint, courses, Course.fromJSON, toast);
        console.log(courses.value ? courses.value.map((course, index) => `Course ${index + 1}: ${JSON.stringify(course)}`) : 'Courses is null');
    }

    async function createCourse(course_data: any) {
        const endpoint = endpoints.courses.index;
        create<Course>(endpoint, course_data, course, Course.fromJSON, toast);
    }

    async function deleteCourse(id: string) {
        const endpoint = endpoints.courses.retrieve.replace('{id}', id.toString());
        delete_id<Course>(endpoint, course, Course.fromJSON, toast);
    }

    async function getCoursesByStudent(student_id: number) {
        const endpoint = endpoints.courses.byStudent.replace('{student_id}', student_id.toString());
        getList<Course>(endpoint, courses, Course.fromJSON, toast);
        console.log(courses.value ? courses.value.map((course, index) => `Course ${index + 1}: ${JSON.stringify(course)}`) : 'Courses is null');
    }



    return {
        courses,
        course,
        getCourseByID,
        getCourses,
        getCoursesByStudent,
        createCourse,
        deleteCourse
    };
}