import { type Course } from './Course'
import { type Faculty } from './Faculty'
import { type Role, User } from '@/types/User.ts'

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
        public faculties: Faculty[] = [],
        public courses: Course[] = [],
        public create_time: Date,
        public last_login: Date | null
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
            courses
        )
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
            assistant.faculties,
            assistant.courses,
            new Date(assistant.create_time),
            assistant.last_login !== null
                ? new Date(assistant.last_login)
                : null
        )
    }

    /**
     * Check if the user is a assistant.
     *
     * @returns boolean
     */
    public isAssistant(): boolean {
        return true
    }
}
