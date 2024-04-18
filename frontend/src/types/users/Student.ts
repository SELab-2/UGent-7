import { type Course } from '../Course.ts';
import { type Faculty } from '../Faculty.ts';
import { type Group } from '../Group.ts';
import { type Role, User } from '@/types/users/User.ts';

interface StudentProps {
    [key: string]: any;
}

export class Student extends User {
    constructor(
        public id: string,
        public username: string,
        public email: string,
        public first_name: string,
        public last_name: string,
        public is_staff: boolean,
        public last_enrolled: number,
        public create_time: Date,
        public last_login: Date | null,
        public studentId: string,
        public roles: Role[] = [],
        public courses: Course[] = [],
        public groups: Group[] = [],
        public faculties: Faculty[] = [],
    ) {
        super(
            id,
            username,
            email,
            first_name,
            last_name,
            last_enrolled,
            is_staff,
            roles,
            faculties,
            create_time,
            last_login,
        );
    }

    /**
     * Convert a student object to a student instance.
     *
     * @param student
     */
    static fromJSON(student: StudentProps): Student {
        return new Student(
            student.id,
            student.username,
            student.email,
            student.first_name,
            student.last_name,
            student.is_staff,
            student.last_enrolled,
            new Date(student.create_time),
            student.last_login !== null ? new Date(student.last_login) : null,
            student.studentId,
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

    /**
     * Get the role of the user.
     * @returns string
     */
    public getRole(): string {
        return 'types.roles.student';
    }
}
