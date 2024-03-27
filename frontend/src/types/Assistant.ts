import { Faculty } from "./Faculty";

export class Assistant {
    constructor(
        public id: string,
        public last_login: Date |null,
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
     * Convert a assistant object to a assistant instance.
     *
     * @param assistant
     */
    
    static fromJSON(assistant: Assistant): Assistant {
        return new Assistant(
            assistant.id,
            assistant.last_login ? new Date(assistant.last_login) : null,
            assistant.username,
            assistant.is_staff,
            assistant.email,
            assistant.first_name,
            assistant.last_name,
            assistant.last_enrolled,
            new Date(assistant.create_time)
        );
    }
}