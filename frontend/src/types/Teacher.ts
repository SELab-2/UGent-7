import { Faculty } from "./Faculty";

export class Teacher {
    constructor(
        public id: string,
        public last_login: Date | null,
        public username: string,
        public is_staff: boolean,
        public email: string,
        public first_name: string,
        public last_name: string,
        public last_enrolled: number,
        public create_time: Date,
        public faculties: Faculty[] = []
    ) {
    }

    /**
     * Convert a teacher object to a teacher instance.
     *
     * @param teacher
     */
    
    static fromJSON(teacher: Teacher): Teacher {
        return new Teacher(
            teacher.id,
            teacher.last_login ? new Date(teacher.last_login) : null,
            teacher.username,
            teacher.is_staff,
            teacher.email,
            teacher.first_name,
            teacher.last_name,
            teacher.last_enrolled,
            new Date(teacher.create_time)
        );
    }
}