import {Course} from '@/types/Course.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import { get, getList, create, delete_id } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';
import {ComposerTranslation} from "vue-i18n";

export function useCourses() {
    const courses = ref<Course[]|null>(null);
    const course = ref<Course|null>(null);
    const toast = useToast();

    async function getCourseByID(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.courses.retrieve.replace('{id}', id);
        get<Course>(endpoint, course, Course.fromJSON, toast, t);
    }

    async function getCourses(t: ComposerTranslation) {
        const endpoint = endpoints.courses.index;
        getList<Course>(endpoint, courses, Course.fromJSON, toast, t);
    }

    async function getCoursesByStudent(student_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.courses.byStudent.replace('{student_id}', student_id);
        await getList<Course>(endpoint, courses, Course.fromJSON, toast, t);
    }

    async function createCourse(course_data: any, t: ComposerTranslation) {
        const endpoint = endpoints.courses.index;
        create<Course>(endpoint, course_data, course, Course.fromJSON, toast, t);
    }

    async function cloneCourse(course_id: string, clone_assistants: boolean, t: ComposerTranslation) {
        const endpoint = endpoints.courses.clone.replace('{course_id}', course_id);
        create<Course>(endpoint, {clone_assistants: clone_assistants.toString() }, course, Course.fromJSON, toast, t);
    }

    async function deleteCourse(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.courses.retrieve.replace('{id}', id);
        delete_id<Course>(endpoint, course, Course.fromJSON, toast, t);
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