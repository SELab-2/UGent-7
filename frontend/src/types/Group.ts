import { type Project } from './Project.ts';
import { type Student } from './users/Student.ts';
import { type Submission } from './submission/Submission.ts';

export class Group {
    constructor(
        public id: string,
        public score: number = -1,
        public project: Project | null = null,
        public students: Student[] | null = null,
        public submissions: Submission[] | null = null,
    ) {}

    /**
     * Check if the group is locked.
     *
     * @returns {boolean}
     */
    public isLocked(): boolean {
        const students = this.students ?? [];

        if (this.project !== null) {
            return students.length >= this.project?.group_size || this.project.isLocked();
        }

        return true;
    }

    /**
     * Get the size of the group.
     *
     * @returns {number} The size of the group.
     */
    public getSize(): number {
        return this.students?.length ?? 0;
    }

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
