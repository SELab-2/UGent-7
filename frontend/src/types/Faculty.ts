export class Faculty {
    constructor(
        public id: string,
        public name: string,
    ) {}

    /**
     * Convert a faculty object to a faculty instance.
     *
     * @param faculty
     */
    static fromJSON(faculty: Faculty): Faculty {
        console.log(JSON.stringify(faculty))
        return new Faculty(faculty.id, faculty.name);
    }
}
