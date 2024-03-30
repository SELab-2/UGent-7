import { Faculty } from "./Faculty";
import {Role, User} from '@/types/User.ts';

export class Assistant extends User {
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
     * Convert a assistant object to a assistant instance.
     *
     * @param assistant
     */
    static fromJSON(assistant: Assistant): Assistant {
        return new Assistant(
            assistant.id,
            assistant.username,
            assistant.email,
            assistant.first_name,
            assistant.last_name,
            assistant.last_enrolled,
            assistant.is_staff,
            assistant.roles,
            assistant.faculties
        );
    }
}