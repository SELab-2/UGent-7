import { type Faculty } from '../Faculty.ts';

export const roles: string[] = ['user', 'student', 'assistant', 'teacher'];
export type Role = (typeof roles)[number];

export interface UserJSON {
    id: string;
    first_name: string;
    last_name: string;
    email: string;
    username: string;
    is_staff: boolean;
    last_enrolled: number;
    create_time: string;
    last_login: string | null;
    roles: Role[];
}

export class User {
    constructor(
        public id: string = '',
        public username: string = '',
        public email: string = '',
        public first_name: string = '',
        public last_name: string = '',
        public last_enrolled: number = 0,
        public is_staff: boolean = false,
        public roles: Role[] = [],
        public faculties: Faculty[] = [],
        public create_time: Date = new Date(),
        public last_login: Date | null = null,
    ) {}

    /**
     * Get the full name of the user.
     *
     * @returns string
     */
    public getFullName(): string {
        return `${this.first_name} ${this.last_name}`;
    }

    /**
     * Check if the user is a student.
     *
     * @returns boolean
     */
    public isStudent(): boolean {
        return false;
    }

    /**
     * Check if the user is an assistant.
     *
     * @returns boolean
     */
    public isAssistant(): boolean {
        return false;
    }

    /**
     * Check if the user is a teacher.
     *
     * @returns boolean
     */
    public isTeacher(): boolean {
        return false;
    }

    /**
     * Check if the user is a specific role.
     *
     * @returns boolean
     */
    public isSpecificRole(): boolean {
        return this.roles.length > 0;
    }

    /**
     * Check if the user has a role.
     *
     * @param roles
     */
    public hasRoles(...roles: Role[]): boolean {
        return roles.every((role) => this.roles.includes(role));
    }

    /**
     *  Check if the user has multiple roles.
     *
     *  @returns boolean
     */
    public hasMultipleRoles(): boolean {
        return this.roles.length > 1;
    }

    /**
     * Get the role of the user in a string format.
     * @returns string
     */
    public getRole(): string {
        return '';
    }

    /**
     * Convert a user object to a user instance.
     *
     * @param user
     */
    static fromJSON(user: UserJSON): User {
        console.log(user);

        return new User(
            user.id,
            user.username,
            user.email,
            user.first_name,
            user.last_name,
            user.last_enrolled,
            user.is_staff,
            user.roles,
            [],
            new Date(user.create_time),
            user.last_login !== null ? new Date(user.last_login) : null,
        );
    }

    static blankUser(): User {
        return new User('', '', '', '', '', 0, false, [], [], new Date(), null);
    }
}
