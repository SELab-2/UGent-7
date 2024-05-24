import { Course } from '@/types/Course.ts';
import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { get, getList, create, patch, deleteId, getPaginatedList } from '@/composables/services/helpers.ts';
import { type Response } from '@/types/Response.ts';
import { type CoursePaginatorResponse } from '@/types/filter/Paginator.ts';
import { type Filter } from '@/types/filter/Filter.ts';
import { type User } from '@/types/users/User.ts';

interface CoursesState {
    pagination: Ref<CoursePaginatorResponse | null>;
    courses: Ref<Course[] | null>;
    course: Ref<Course | null>;

    getCourseByID: (id: string, selfProcessError?: boolean) => Promise<void>;
    getCourses: (selfProcessError?: boolean) => Promise<void>;
    searchCourses: (filters: Filter, page: number, pageSize: number, selfProcessError?: boolean) => Promise<void>;
    getCoursesByStudent: (studentId: string, selfProcessError?: boolean) => Promise<void>;
    getCoursesByTeacher: (teacherId: string, selfProcessError?: boolean) => Promise<void>;
    getCourseByAssistant: (assistantId: string, selfProcessError?: boolean) => Promise<void>;
    getCoursesByUser: (user: User, selfProcessError?: boolean) => Promise<void>;
    createCourse: (courseData: Course, selfProcessError?: boolean) => Promise<void>;
    updateCourse: (courseData: Course, selfProcessError?: boolean) => Promise<void>;
    cloneCourse: (
        courseId: string,
        cloneAssistants: boolean,
        cloneTeachers: boolean,
        selfProcessError?: boolean,
    ) => Promise<void>;
    activateInvitationLink: (courseId: string, linkDuration: number, selfProcessError?: boolean) => Promise<void>;
    deleteCourse: (id: string, selfProcessError?: boolean) => Promise<void>;
}

export function useCourses(): CoursesState {
    const pagination = ref<CoursePaginatorResponse | null>(null);
    const courses = ref<Course[] | null>(null);
    const course = ref<Course | null>(null);
    const response = ref<Response | null>(null);

    async function getCourseByID(id: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.courses.retrieve.replace('{id}', id);
        await get<Course>(endpoint, course, Course.fromJSON, selfProcessError);
    }

    async function getCourses(selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.courses.index;
        await getList<Course>(endpoint, courses, Course.fromJSON, selfProcessError);
    }

    async function searchCourses(
        filters: Filter,
        page: number,
        pageSize: number,
        selfProcessError: boolean = true,
    ): Promise<void> {
        const endpoint = endpoints.courses.search;
        await getPaginatedList<Course>(
            endpoint,
            filters,
            page,
            pageSize,
            pagination,
            Course.fromJSON,
            selfProcessError,
        );
    }

    async function getCoursesByStudent(studentId: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.courses.byStudent.replace('{studentId}', studentId);
        await getList<Course>(endpoint, courses, Course.fromJSON, selfProcessError);
    }

    async function getCoursesByTeacher(teacherId: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.courses.byTeacher.replace('{teacherId}', teacherId);
        await getList<Course>(endpoint, courses, Course.fromJSON, selfProcessError);
    }

    async function getCourseByAssistant(assistantId: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.courses.byAssistant.replace('{assistantId}', assistantId);
        await getList<Course>(endpoint, courses, Course.fromJSON, selfProcessError);
    }

    async function getCoursesByUser(user: User, selfProcessError: boolean = true): Promise<void> {
        if (user.isTeacher()) {
            await getCoursesByTeacher(user.id, selfProcessError);
        } else if (user.isAssistant()) {
            await getCourseByAssistant(user.id, selfProcessError);
        } else if (user.isStudent()) {
            await getCoursesByStudent(user.id, selfProcessError);
        } else {
            courses.value = [];
        }
    }

    async function createCourse(courseData: Course, selfProcessError: boolean = true): Promise<void> {
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
                faculty_id: courseData.faculty?.id,
            },
            course,
            Course.fromJSON,
            undefined,
            selfProcessError,
        );
    }

    async function updateCourse(courseData: Course, selfProcessError: boolean = true): Promise<void> {
        // Endpoint to update is same as retrieve
        const endpoint = endpoints.courses.retrieve.replace('{id}', courseData.id);

        await patch(
            endpoint,
            {
                id: courseData.id,
                name: courseData.name,
                description: courseData.description,
                excerpt: courseData.excerpt,
                faculty_id: courseData.faculty?.id,
                private_course: courseData.private_course,
            },
            response,
            undefined,
            selfProcessError,
        );
    }

    async function cloneCourse(
        courseId: string,
        cloneAssistants: boolean,
        cloneTeachers: boolean,
        selfProcessError: boolean = true,
    ): Promise<void> {
        const endpoint = endpoints.courses.clone.replace('{courseId}', courseId);
        await create<Course>(
            endpoint,
            {
                clone_assistants: cloneAssistants.toString(),
                clone_teachers: cloneTeachers.toString(),
            },
            course,
            Course.fromJSON,
            undefined,
            selfProcessError,
        );
    }

    async function deleteCourse(id: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.courses.retrieve.replace('{id}', id);
        await deleteId<Course>(endpoint, course, Course.fromJSON, selfProcessError);
    }

    async function activateInvitationLink(
        courseId: string,
        linkDuration: number,
        selfProcessError: boolean = true,
    ): Promise<void> {
        const endpoint = endpoints.courses.invitationLink.replace('{courseId}', courseId);
        await patch(
            endpoint,
            {
                link_duration: linkDuration,
            },
            response,
            undefined,
            selfProcessError,
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
        getCoursesByUser,

        createCourse,
        updateCourse,
        cloneCourse,
        deleteCourse,
        activateInvitationLink,
    };
}
