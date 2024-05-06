import { type Assistant } from './users/Assistant.ts';
import { type Project } from './Project.ts';
import { type Student } from './users/Student.ts';
import { type Teacher } from './users/Teacher.ts';
import { Faculty } from '@/types/Faculty.ts';

export class Course {
    constructor(
        public id: string,
        public name: string,
        public excerpt: string,
        public description: string | null,
        public academic_startyear: number,
        public private_course: boolean = false,
        public invitation_link: string | null = null,
        public invitation_link_expires: Date | null = null,
        public parent_course: Course | null = null,
        public faculty: Faculty | null = null,
        public teachers: Teacher[] | null = null,
        public assistants: Assistant[] | null = null,
        public students: Student[] | null = null,
        public projects: Project[] | null = null,
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
     * Convert a course object to a course instance.
     *
     * @param course
     */
    static fromJSON(course: Course): Course {
        const faculty =
            course.faculty !== undefined && course.faculty !== null ? Faculty.fromJSON(course.faculty) : null;

        return new Course(
            course.id,
            course.name,
            course.excerpt,
            course.description,
            course.academic_startyear,
            course.private_course,
            course.invitation_link,
            course.invitation_link_expires,
            course.parent_course,
            faculty,
        );
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
