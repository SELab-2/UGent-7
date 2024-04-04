import { type Project } from './Projects';
import { type Student } from './users/Student.ts';
import { type Submission } from './Submission';

export class Group {
    constructor(
        public id: string,
        public score: number = -1,
        public project: Project | null = null,
        public students: Student[] = [],
        public submissions: Submission[] = [],
    ) {}

    /**
     * Convert a group object to a group instance.
     *
     * @param group
     */
    static fromJSON(group: Group): Group {
        return new Group(group.id, group.score);
    }

    static fromJSONFullObject(group: Group): Group {
        return new Group(group.id, group.score, group.project, group.students, group.submissions);
    }
}
