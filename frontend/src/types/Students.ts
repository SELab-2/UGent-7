import { Course } from "./Course";
import { Faculty } from "./Faculty";
import { Group } from "./Group";

export class Student {
    constructor(
        public id: number,
        public last_login: Date,
        public username: string,
        public is_staff: boolean,
        public email: string,
        public first_name: string,
        public last_name: string,
        public last_enrolled: number,
        public create_time: Date,
        public student_id: string,
        public courses: Course[] = [],
        public groups: Group[] = [],
        public faculties: Faculty[] = []
    ) {
    }

    /**
     * Convert a student object to a student instance.
     *
     * @param student
     */
    static fromJSON(student: Student): Student {
        return new Student(
            student.id,
            student.last_login,
            student.username,
            student.is_staff,
            student.email,
            student.first_name,
            student.last_name,
            student.last_enrolled,
            student.create_time,
            student.student_id
        );
    }
}