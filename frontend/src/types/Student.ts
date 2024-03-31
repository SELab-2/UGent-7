import { Course } from "./Course";
import { Faculty } from "./Faculty";
import { Group } from "./Group";
import {Role, User} from '@/types/User.ts';

export class Student extends User {
    constructor(
        public id: string,
        public username: string,
        public email: string,
        public first_name: string,
        public last_name: string,
        public is_staff: boolean,
        public last_enrolled: number,
        public student_id: string,
        public roles: Role[] = [],
        public courses: Course[] = [],
        public groups: Group[] = [],
        public faculties: Faculty[] = []
    ) {
        super(id, username, email, first_name, last_name, last_enrolled, is_staff, roles, courses);
    }

    /**
     * Convert a student object to a student instance.
     *
     * @param student
     */
    static fromJSON(student: Student): Student {
        return new Student(
            student.id,
            student.username,
            student.email,
            student.first_name,
            student.last_name,
            student.is_staff,
            student.last_enrolled,
            student.student_id,
            student.roles,
            student.courses,
            student.groups,
            student.faculties
        );
    }

    /**
     * Check if the user is a student.
     *
     * @returns boolean
     */
    public isStudent(): boolean {
        return true;
    }
}