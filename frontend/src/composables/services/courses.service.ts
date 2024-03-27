import {Course} from '@/types/Course.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';
import {ComposerTranslation} from "vue-i18n";

export function useCourses() {
    const courses = ref<Course[]|null>(null);
    const course = ref<Course|null>(null);

    async function getCourseByID(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.courses.retrieve.replace('{id}', id);
        await get<Course>(endpoint, course, Course.fromJSON, t);
    }

    async function getCourses(t: ComposerTranslation) {
        const endpoint = endpoints.courses.index;
        await getList<Course>(endpoint, courses, Course.fromJSON, t);
    }

    async function getCoursesByStudent(student_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.courses.byStudent.replace('{student_id}', student_id);
        await getList<Course>(endpoint, courses, Course.fromJSON, t);
    }

    async function createCourse(course_data: any, t: ComposerTranslation) {
        const endpoint = endpoints.courses.index;
        await create<Course>(endpoint, course_data, course, Course.fromJSON, t);
    }

    async function cloneCourse(course_id: string, clone_assistants: boolean, t: ComposerTranslation) {
        const endpoint = endpoints.courses.clone.replace('{course_id}', course_id);
        await create<Course>(endpoint, {clone_assistants: clone_assistants.toString() }, course, Course.fromJSON, t);
    }

    async function deleteCourse(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.courses.retrieve.replace('{id}', id);
        await delete_id<Course>(endpoint, course, Course.fromJSON, t);
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