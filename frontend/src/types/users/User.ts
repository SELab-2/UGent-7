import { type Faculty } from '../Faculty.ts';

export const roles = ['user', 'student', 'assistant', 'teacher'] as const;
export type Role = (typeof roles)[number];

export class User {
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
        public create_time: Date,
        public last_login: Date | null,
    ) {}

    /**
     * Get the academic years of the user.
     */
    get academic_years(): number[] {
        const startYear = User.getAcademicYear(this.create_time);
        const endYear = User.getAcademicYear(new Date());

        return Array.from({ length: endYear - startYear + 1 }, (_, i) => startYear + i);
    }

    /**
     * Get the full name of the user.
     *
     * @returns string
     */
    public getFullName(): string {
        return `${this.first_name} ${this.last_name}`;
    }

    /**
     * Get the academic year of a date.
     *
     * @param date
     * @returns number
     */
    public static getAcademicYear(date: Date = new Date()): number {
        const year = date.getFullYear();

        if (date.getMonth() >= 9) {
            return year;
        }

        return year - 1;
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
        return this.isStudent() || this.isAssistant() || this.isTeacher();
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
     * Convert a user object to a user instance.
     *
     * @param user
     */
    static fromJSON(user: User): User {
        return new User(
            user.id,
            user.username,
            user.email,
            user.first_name,
            user.last_name,
            user.last_enrolled,
            user.is_staff,
            user.roles,
            user.faculties,
            new Date(user.create_time),
            user.last_login !== null ? new Date(user.last_login) : null,
        );
    }

    static blankUser(): User {
        return new User('', '', '', '', '', 0, false, [], [], new Date(), null);
    }
}
