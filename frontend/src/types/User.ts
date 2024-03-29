export type Role = 'user' | 'student' | 'assistant' | 'teacher';

export class User {
    constructor(
        public id: string,
        public username: string,
        public email: string,
        public first_name: string,
        public last_name: string,
        public last_enrolled: number,
        public is_staff: boolean,
        public roles: Role[] = []
    ) {
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
     * Check if the user is a student.
     *
     * @returns boolean
     */
    public isStudent(): boolean {
        return this.roles.includes('student');
    }

    /**
     * Check if the user is an assistant.
     *
     * @returns boolean
     */
    public isAssistant(): boolean {
        return this.roles.includes('assistant');
    }

    /**
     * Check if the user is a teacher.
     *
     * @returns boolean
     */
    public isTeacher(): boolean {
        return this.roles.includes('teacher');
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
            user.roles
        );
    }
}