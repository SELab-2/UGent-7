import { type Assistant } from './users/Assistant.ts';
import { type Project } from './Projects';
import { type Student } from './users/Student.ts';
import { type Teacher } from './users/Teacher.ts';
import { Faculty } from '@/types/Faculty.ts';

export class Course {
    constructor(
        public id: string,
        public name: string,
        public description: string | null,
        public academic_startyear: number,
        public parent_course: Course | null = null,
        public faculty: Faculty | null = null,
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
     * @param maxLength
     * @returns string
     */
    public getExcerpt(maxLength: number = 100): string {
        if (this.description === null) return '';

        if (this.description.length < maxLength) return this.description;

        return this.description.substring(0, maxLength) + '...';
    }

    /**
     * Convert a course object to a course instance.
     *
     * @param course
     */
    static fromJSON(course: Course): Course {
        const faculty =
            course.faculty !== null ? Faculty.fromJSON(course.faculty) : null;

        return new Course(
            course.id,
            course.name,
            course.description,
            course.academic_startyear,
            course.parent_course,
            faculty,
        );
    }
}
