export class Faculty {
    constructor(
        public name: string,
    ) {
    }

    /**
     * Convert a faculty object to a faculty instance.
     *
     * @param faculty
     */
    static fromJSON(faculty: Faculty): Faculty {
        return new Faculty(faculty.name);
    }
}