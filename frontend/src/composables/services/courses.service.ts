import {Course} from '@/types/Course.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';

export function useCourses() {
    const courses = ref<Course[]|null>(null);
    const course = ref<Course|null>(null);

    async function getCourseByID(id: string) {
        const endpoint = endpoints.courses.retrieve.replace('{id}', id);
        await get<Course>(endpoint, course, Course.fromJSON);
    }

    async function getCourses() {
        const endpoint = endpoints.courses.index;
        await getList<Course>(endpoint, courses, Course.fromJSON);
    }

    async function getCoursesByStudent(student_id: string) {
        const endpoint = endpoints.courses.byStudent.replace('{student_id}', student_id);
        await getList<Course>(endpoint, courses, Course.fromJSON);
    }

    async function createCourse(course_data: Course) {
        const endpoint = endpoints.courses.index;
        await create<Course>(endpoint,
            {
                name: course_data.name,
                description: course_data.description,
                academic_startyear: course_data.academic_startyear
            },
        course, Course.fromJSON);
    }

    async function cloneCourse(course_id: string, clone_assistants: boolean) {
        const endpoint = endpoints.courses.clone.replace('{course_id}', course_id);
        await create<Course>(endpoint, {clone_assistants: clone_assistants.toString() }, course, Course.fromJSON);
    }

    async function deleteCourse(id: string) {
        const endpoint = endpoints.courses.retrieve.replace('{id}', id);
        await delete_id<Course>(endpoint, course, Course.fromJSON);
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