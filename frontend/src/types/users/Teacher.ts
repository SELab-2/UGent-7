import { type Course } from '../Course.ts';
import { type Faculty } from '../Faculty.ts';
import { type Role, User } from '@/types/users/User.ts';

export class Teacher extends User {
    constructor(
        public id: string,
        public username: string,
        public email: string,
        public first_name: string,
        public last_name: string,
        public last_enrolled: number,
        public is_staff: boolean,
        public roles: Role[] = [],
        public faculties: Faculty[] = [],
        public courses: Course[] = [],
        public create_time: Date,
        public last_login: Date | null,
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
     * Convert a teacher object to a teacher instance.
     *
     * @param teacher
     */

    static fromJSON(teacher: Teacher): Teacher {
        return new Teacher(
            teacher.id,
            teacher.username,
            teacher.email,
            teacher.first_name,
            teacher.last_name,
            teacher.last_enrolled,
            teacher.is_staff,
            teacher.roles,
            teacher.faculties,
            teacher.courses,
            new Date(teacher.create_time),
            teacher.last_login !== null ? new Date(teacher.last_login) : null,
        );
    }

    /**
     * Check if the user is a teacher.
     *
     * @returns boolean
     */
    public isTeacher(): boolean {
        return true;
    }

    /**
     * Get the role of the user in a string format.
     * @returns string
     */
    public getRole(): string {
        return 'types.roles.teacher';
    }
}
