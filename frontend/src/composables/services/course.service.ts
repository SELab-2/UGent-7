import { Course } from '@/types/Course.ts';
import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { get, getList, create, patch, deleteId, getPaginatedList } from '@/composables/services/helpers.ts';
import { type Response } from '@/types/Response.ts';
import { type CoursePaginatorResponse } from '@/types/filter/Paginator.ts';
import { type Filter } from '@/types/filter/Filter.ts';

interface CoursesState {
    pagination: Ref<CoursePaginatorResponse | null>;
    courses: Ref<Course[] | null>;
    course: Ref<Course | null>;
    getCourseByID: (id: string) => Promise<void>;
    getCourses: () => Promise<void>;
    searchCourses: (filters: Filter, page: number, pageSize: number) => Promise<void>;
    getCoursesByStudent: (studentId: string) => Promise<void>;
    getCoursesByTeacher: (teacherId: string) => Promise<void>;
    getCourseByAssistant: (assistantId: string) => Promise<void>;
    createCourse: (courseData: Course) => Promise<void>;
    updateCourse: (courseData: Course) => Promise<void>;
    cloneCourse: (courseId: string, cloneAssistants: boolean, cloneTeachers: boolean) => Promise<void>;
    activateInvitationLink: (courseId: string, linkDuration: number) => Promise<void>;
    deleteCourse: (id: string) => Promise<void>;
}

export function useCourses(): CoursesState {
    const pagination = ref<CoursePaginatorResponse | null>(null);
    const courses = ref<Course[] | null>(null);
    const course = ref<Course | null>(null);
    const response = ref<Response | null>(null);

    async function getCourseByID(id: string): Promise<void> {
        const endpoint = endpoints.courses.retrieve.replace('{id}', id);
        await get<Course>(endpoint, course, Course.fromJSON);
    }

    async function getCourses(): Promise<void> {
        const endpoint = endpoints.courses.index;
        await getList<Course>(endpoint, courses, Course.fromJSON);
    }

    async function searchCourses(filters: Filter, page: number, pageSize: number): Promise<void> {
        const endpoint = endpoints.courses.search;
        await getPaginatedList<Course>(endpoint, filters, page, pageSize, pagination, Course.fromJSON);
    }

    async function getCoursesByStudent(studentId: string): Promise<void> {
        const endpoint = endpoints.courses.byStudent.replace('{studentId}', studentId);
        await getList<Course>(endpoint, courses, Course.fromJSON);
    }

    async function getCoursesByTeacher(teacherId: string): Promise<void> {
        const endpoint = endpoints.courses.byTeacher.replace('{teacherId}', teacherId);
        await getList<Course>(endpoint, courses, Course.fromJSON);
    }

    async function getCourseByAssistant(assistantId: string): Promise<void> {
        const endpoint = endpoints.courses.byAssistant.replace('{assistantId}', assistantId);
        await getList<Course>(endpoint, courses, Course.fromJSON);
    }

    async function createCourse(courseData: Course): Promise<void> {
        const endpoint = endpoints.courses.index;
        await create<Course>(
            endpoint,
            {
                id: courseData.id,
                name: courseData.name,
                description: courseData.description,
                excerpt: courseData.excerpt,
                academic_startyear: courseData.academic_startyear,
                private_course: courseData.private_course,
                faculty: courseData.faculty,
            },
            course,
            Course.fromJSON,
        );
    }

    async function updateCourse(courseData: Course): Promise<void> {
        // Endpoint to update is same as retrieve
        const endpoint = endpoints.courses.retrieve.replace('{id}', courseData.id);

        await patch(
            endpoint,
            {
                id: courseData.id,
                name: courseData.name,
                description: courseData.description,
                faculty: courseData.faculty,
                private_course: courseData.private_course,
            },
            response,
        );
    }

    async function cloneCourse(courseId: string, cloneAssistants: boolean, cloneTeachers: boolean): Promise<void> {
        const endpoint = endpoints.courses.clone.replace('{courseId}', courseId);
        await create<Course>(
            endpoint,
            {
                clone_assistants: cloneAssistants.toString(),
                clone_teachers: cloneTeachers.toString(),
            },
            course,
            Course.fromJSON,
        );
    }

    async function deleteCourse(id: string): Promise<void> {
        const endpoint = endpoints.courses.retrieve.replace('{id}', id);
        await deleteId<Course>(endpoint, course, Course.fromJSON);
    }

    async function activateInvitationLink(courseId: string, linkDuration: number): Promise<void> {
        const endpoint = endpoints.courses.invitationLink.replace('{courseId}', courseId);
        await patch(
            endpoint,
            {
                link_duration: linkDuration,
            },
            response,
        );
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
        updateCourse,
        cloneCourse,
        deleteCourse,
        activateInvitationLink,
    };
}
