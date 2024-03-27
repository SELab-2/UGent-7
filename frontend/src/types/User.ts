export class User {
    constructor(
        public id: number,
        public username: string,
        public first_name: string,
        public last_name: string,
        public last_enrolled: number
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
     * Convert a user object to a user instance.
     *
     * @param user
     */
    static fromJSON(user: User): User {
        return new User(
            user.id,
            user.username,
            user.first_name,
            user.last_name,
            user.last_enrolled
        );
    }
}