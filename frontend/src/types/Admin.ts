import { Faculty } from "./Faculty";

export class Admin {
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
     * Convert a admin object to a admin instance.
     *
     * @param admin
     */
    static fromJSON(admin: Admin): Admin {
        return new Admin(
            admin.id,
            admin.last_login ? new Date(admin.last_login) : null,
            admin.username,
            admin.is_staff,
            admin.email,
            admin.first_name,
            admin.last_name,
            admin.last_enrolled,
            new Date(admin.create_time)
        );
    }
}