export type FacultyJSON = {
    id: string;
    name: string;
};

export class Faculty {
    constructor(
        public id: string = '',
        public name: string = '',
    ) {}

    /**
     * Convert a faculty object to a faculty instance.
     *
     * @param faculty
     */
    static fromJSON(faculty: FacultyJSON): Faculty {
        return new Faculty(faculty.id, faculty.name);
    }
}
