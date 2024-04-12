import { Course } from '@/types/Course.ts';
import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { get, getList, create, deleteId, getPaginatedList } from '@/composables/services/helpers.ts';
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
    cloneCourse: (courseId: string, cloneAssistants: boolean, cloneTeachers: boolean) => Promise<void>;
    deleteCourse: (id: string) => Promise<void>;
}

export function useCourses(): CoursesState {
    const pagination = ref<CoursePaginatorResponse | null>(null);
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
                name: courseData.name,
                description: courseData.description,
                academic_startyear: courseData.academic_startyear,
                faculty: courseData.faculty?.id,
            },
            course,
            Course.fromJSON,
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
