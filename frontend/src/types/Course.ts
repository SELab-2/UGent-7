export default class Course {
    constructor(
        public id: number,
        public name: string,
        public description: string,
        public academic_startyear: number
    ) {
    }

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
        return new Course(
            course.id,
            course.name,
            course.description,
            course.academic_startyear
        );
    }
}