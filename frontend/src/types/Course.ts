import { type Assistant } from './users/Assistant.ts';
import { type Project } from './Project.ts';
import { type Student } from './users/Student.ts';
import { type Teacher } from './users/Teacher.ts';
import { Faculty, type FacultyJSON } from '@/types/Faculty.ts';
import { type HyperlinkedRelation } from '@/types/ApiResponse.ts';

export interface CourseJSON {
    id: string;
    name: string;
    academic_startyear: number;
    excerpt: string;
    description: string;
    private_course: boolean;
    invitation_link?: string;
    invitation_link_expires?: string;
    faculty: FacultyJSON;
    parent_course: CourseJSON | null;
    teachers: HyperlinkedRelation;
    assistants: HyperlinkedRelation;
    students: HyperlinkedRelation;
    projects: HyperlinkedRelation;
}

export class Course {
    constructor(
        public id: string = '',
        public name: string = '',
        public excerpt: string = '',
        public description: string = '',
        public academic_startyear: number = getAcademicYear(),
        public private_course: boolean = false,
        public invitation_link: string = '',
        public invitation_link_expires: Date = new Date(),
        public parent_course: Course | null = null,
        public faculty: Faculty = new Faculty(),
        public teachers: Teacher[] = [],
        public assistants: Assistant[] = [],
        public students: Student[] = [],
        public projects: Project[] = [],
    ) {}

    /**
     * Get the course year.
     * @returns string
     */
    public getCourseYear(): string {
        return `${this.academic_startyear} - ${this.academic_startyear + 1}`;
    }

    /**
     * Get the excerpt of the course description.
     *
     * @returns string
     */
    public getExcerpt(): string {
        return this.excerpt;
    }

    /**
     * Check if the course has a given teacher.
     * @param teacher
     */
    public hasTeacher(teacher: Teacher): boolean {
        const teachers = this.teachers ?? [];
        return teachers.some((t) => t.id === teacher.id);
    }

    /**
     * Check if the course has a given assistant.
     * @param assistant
     */
    public hasAssistant(assistant: Assistant): boolean {
        const assistants = this.assistants ?? [];
        return assistants.some((a) => a.id === assistant.id);
    }

    /**
     * Convert a course object to a course instance.
     *
     * @param course
     */
    static fromJSON(course: CourseJSON): Course {
        let parent: CourseJSON | Course | null = course.parent_course;

        if (parent !== null) {
            parent = Course.fromJSON(parent);
        }

        return new Course(
            course.id,
            course.name,
            course.excerpt,
            course.description,
            course.academic_startyear,
            course.private_course,
            course.invitation_link,
            new Date(course.invitation_link_expires ?? ''),
            parent,
            course.faculty,
        );
    }
}

/**
 * Get the academic year of a date.
 *
 * @param date
 * @returns number
 */
export function getAcademicYear(date: Date = new Date()): number {
    const year = date.getFullYear();

    if (date.getMonth() >= 9) {
        return year;
    }

    return year - 1;
}

/**
 * Get the academic years between a minimum and maximum.
 *
 * @param years
 * @returns number[]
 */
export function getAcademicYears(...years: number[]): number[] {
    const min = Math.min(...years);
    const max = Math.max(...years);

    return Array.from({ length: max - min + 1 }, (_, i) => max - i);
}
