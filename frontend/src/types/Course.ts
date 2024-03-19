export default class Course {
    constructor(
        public id: string,
    ) {
    }

    /**
     * Convert a course object to a course instance.
     *
     * @param course
     */
    static fromJSON(course: object): Course {
        return new Course(
            course.id
        );
    }
}