import { Course } from '@/types/Course.ts';
import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import {
    get,
    getList,
    create,
    deleteId,
    getPaginatedList,
} from '@/composables/services/helpers.ts';
import { type Filters, type PaginationResponse } from '@/types/Pagination.ts';

interface CoursesState {
    pagination: Ref<PaginationResponse<Course> | null>;
    courses: Ref<Course[] | null>;
    course: Ref<Course | null>;
    getCourseByID: (id: string) => Promise<void>;
    getCourses: () => Promise<void>;
    searchCourses: (filters: Filters) => Promise<void>;
    getCoursesByStudent: (studentId: string) => Promise<void>;
    getCoursesByTeacher: (teacherId: string) => Promise<void>;
    getCourseByAssistant: (assistantId: string) => Promise<void>;
    createCourse: (courseData: Course) => Promise<void>;
    cloneCourse: (courseId: string, cloneAssistants: boolean) => Promise<void>;
    deleteCourse: (id: string) => Promise<void>;
}

export function useCourses(): CoursesState {
    const pagination = ref<PaginationResponse<Course> | null>(null);
    const courses = ref<Course[] | null>(null);
    const course = ref<Course | null>(null);

    async function getCourseByID(id: string): Promise<void> {
        const endpoint = endpoints.courses.retrieve.replace('{id}', id);
        await get<Course>(endpoint, course, Course.fromJSON);
    }

    async function getCourses(): Promise<void> {
        const endpoint = endpoints.courses.index;
        await getList<Course>(endpoint, courses, Course.fromJSON);
    }

    async function searchCourses(filters: Filters): Promise<void> {
        const endpoint = endpoints.courses.search;
        await getPaginatedList<Course>(
            endpoint,
            filters,
            pagination,
            Course.fromJSON,
        );
    }

    async function getCoursesByStudent(studentId: string): Promise<void> {
        const endpoint = endpoints.courses.byStudent.replace(
            '{studentId}',
            studentId,
        );
        await getList<Course>(endpoint, courses, Course.fromJSON);
    }

    async function getCoursesByTeacher(teacherId: string): Promise<void> {
        const endpoint = endpoints.courses.byTeacher.replace(
            '{teacherId}',
            teacherId,
        );
        await getList<Course>(endpoint, courses, Course.fromJSON);
    }

    async function getCourseByAssistant(assistantId: string): Promise<void> {
        const endpoint = endpoints.courses.byAssistant.replace(
            '{assistantId}',
            assistantId,
        );
        await getList<Course>(endpoint, courses, Course.fromJSON);
    }

    async function createCourse(courseData: Course): Promise<void> {
        const endpoint = endpoints.courses.index;
        await create<Course>(
            endpoint,
            {
                name: courseData.name,
                description: courseData.description,
                academic_startyear: courseData.academic_startyear,
            },
            course,
            Course.fromJSON,
        );
    }

    async function cloneCourse(
        courseId: string,
        cloneAssistants: boolean,
    ): Promise<void> {
        const endpoint = endpoints.courses.clone.replace(
            '{courseId}',
            courseId,
        );
        await create<Course>(
            endpoint,
            { cloneAssistants: cloneAssistants.toString() },
            course,
            Course.fromJSON,
        );
    }

    async function deleteCourse(id: string): Promise<void> {
        const endpoint = endpoints.courses.retrieve.replace('{id}', id);
        await deleteId<Course>(endpoint, course, Course.fromJSON);
    }

    return {
        pagination,
        courses,
        course,

        getCourseByID,
        searchCourses,
        getCourses,
        getCoursesByStudent,
        getCoursesByTeacher,
        getCourseByAssistant,

        createCourse,
        cloneCourse,
        deleteCourse,
    };
}
