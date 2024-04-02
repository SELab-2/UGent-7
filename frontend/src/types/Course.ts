import { type Assistant } from './users/Assistant.ts';
import { type Project } from './Projects';
import { type Student } from './users/Student.ts';
import { type Teacher } from './users/Teacher.ts';

export class Course {
    constructor(
        public id: string,
        public name: string,
        public description: string | null,
        public academic_startyear: number,
        public parent_course: Course | null = null,
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
     * Convert a course object to a course instance.
     *
     * @param course
     */
    static fromJSON(course: Course): Course {
        return new Course(course.id, course.name, course.description, course.academic_startyear, course.parent_course);
    }
}
