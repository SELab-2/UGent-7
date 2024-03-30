import { Faculty } from "./Faculty";
import {Role, User} from '@/types/User.ts';

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
        public faculties: Faculty[] = []
    ) {
        super(id, username, email, first_name, last_name, last_enrolled, is_staff, roles);
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
            teacher.faculties
        );
    }
}