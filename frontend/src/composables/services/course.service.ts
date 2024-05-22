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

    getCourseByID: (id: string, selfprocessError?: boolean) => Promise<void>;
    getCourses: (selfprocessError?: boolean) => Promise<void>;
    searchCourses: (filters: Filter, page: number, pageSize: number, selfprocessError?: boolean) => Promise<void>;
    getCoursesByStudent: (studentId: string, selfprocessError?: boolean) => Promise<void>;
    getCoursesByTeacher: (teacherId: string, selfprocessError?: boolean) => Promise<void>;
    getCourseByAssistant: (assistantId: string, selfprocessError?: boolean) => Promise<void>;
    getCoursesByUser: (user: User, selfprocessError?: boolean) => Promise<void>;
    createCourse: (courseData: Course, selfprocessError?: boolean) => Promise<void>;
    updateCourse: (courseData: Course, selfprocessError?: boolean) => Promise<void>;
    cloneCourse: (
        courseId: string,
        cloneAssistants: boolean,
        cloneTeachers: boolean,
        selfprocessError?: boolean,
    ) => Promise<void>;
    activateInvitationLink: (courseId: string, linkDuration: number, selfprocessError?: boolean) => Promise<void>;
    deleteCourse: (id: string, selfprocessError?: boolean) => Promise<void>;
}

export function useCourses(): CoursesState {
    const pagination = ref<CoursePaginatorResponse | null>(null);
    const courses = ref<Course[] | null>(null);
    const course = ref<Course | null>(null);
    const response = ref<Response | null>(null);

    async function getCourseByID(id: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.courses.retrieve.replace('{id}', id);
        await get<Course>(endpoint, course, Course.fromJSON, selfprocessError);
    }

    async function getCourses(selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.courses.index;
        await getList<Course>(endpoint, courses, Course.fromJSON, selfprocessError);
    }

    async function searchCourses(
        filters: Filter,
        page: number,
        pageSize: number,
        selfprocessError: boolean = true,
    ): Promise<void> {
        const endpoint = endpoints.courses.search;
        await getPaginatedList<Course>(
            endpoint,
            filters,
            page,
            pageSize,
            pagination,
            Course.fromJSON,
            selfprocessError,
        );
    }

    async function getCoursesByStudent(studentId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.courses.byStudent.replace('{studentId}', studentId);
        await getList<Course>(endpoint, courses, Course.fromJSON, selfprocessError);
    }

    async function getCoursesByTeacher(teacherId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.courses.byTeacher.replace('{teacherId}', teacherId);
        await getList<Course>(endpoint, courses, Course.fromJSON, selfprocessError);
    }

    async function getCourseByAssistant(assistantId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.courses.byAssistant.replace('{assistantId}', assistantId);
        await getList<Course>(endpoint, courses, Course.fromJSON, selfprocessError);
    }

    async function getCoursesByUser(user: User, selfprocessError: boolean = true): Promise<void> {
        if (user.isTeacher()) {
            await getCoursesByTeacher(user.id, selfprocessError);
        } else if (user.isAssistant()) {
            await getCourseByAssistant(user.id, selfprocessError);
        } else if (user.isStudent()) {
            await getCoursesByStudent(user.id, selfprocessError);
        } else {
            courses.value = [];
        }
    }

    async function createCourse(courseData: Course, selfprocessError: boolean = true): Promise<void> {
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
                faculty: courseData.faculty?.id,
            },
            course,
            Course.fromJSON,
            undefined,
            selfprocessError,
        );
    }

    async function updateCourse(courseData: Course, selfprocessError: boolean = true): Promise<void> {
        // Endpoint to update is same as retrieve
        const endpoint = endpoints.courses.retrieve.replace('{id}', courseData.id);

        await patch(
            endpoint,
            {
                id: courseData.id,
                name: courseData.name,
                description: courseData.description,
                excerpt: courseData.excerpt,
                faculty: courseData.faculty?.id,
                private_course: courseData.private_course,
            },
            response,
            undefined,
            selfprocessError,
        );
    }

    async function cloneCourse(
        courseId: string,
        cloneAssistants: boolean,
        cloneTeachers: boolean,
        selfprocessError: boolean = true,
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
            selfprocessError,
        );
    }

    async function deleteCourse(id: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.courses.retrieve.replace('{id}', id);
        await deleteId<Course>(endpoint, course, Course.fromJSON, selfprocessError);
    }

    async function activateInvitationLink(
        courseId: string,
        linkDuration: number,
        selfprocessError: boolean = true,
    ): Promise<void> {
        const endpoint = endpoints.courses.invitationLink.replace('{courseId}', courseId);
        await patch(
            endpoint,
            {
                link_duration: linkDuration,
            },
            response,
            undefined,
            selfprocessError,
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
