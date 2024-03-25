import {Course} from '@/types/Course.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';

export function useCourses() {
    const courses = ref<Course[]|null>(null);
    const course = ref<Course|null>(null);
    const toast = useToast();

    async function getCourseByID(id: string) {
        const endpoint = endpoints.courses.retrieve.replace('{id}', id);
        get<Course>(endpoint, course, Course.fromJSON, toast);
    }

    async function getCourses() {
        const endpoint = endpoints.courses.index;
        getList<Course>(endpoint, courses, Course.fromJSON, toast);
    }

    async function createCourse(course_data: any) {
        const endpoint = endpoints.courses.index;
        create<Course>(endpoint, course_data, course, Course.fromJSON, toast);
    }

    async function cloneCourse(data: any, course_id: string) {
        const endpoint = endpoints.courses.clone.replace('{course_id}', course_id);
        create<Course>(endpoint, data, course, Course.fromJSON, toast);
    }

    async function deleteCourse(id: string) {
        const endpoint = endpoints.courses.retrieve.replace('{id}', id);
        delete_id<Course>(endpoint, course, Course.fromJSON, toast);
    }

    async function getCoursesByStudent(student_id: string) {
        const endpoint = endpoints.courses.byStudent.replace('{student_id}', student_id);
        getList<Course>(endpoint, courses, Course.fromJSON, toast);
    }



    return {
        courses,
        course,

        getCourseByID,
        getCourses,
        getCoursesByStudent,

        createCourse,
        cloneCourse,
        deleteCourse
    };
}