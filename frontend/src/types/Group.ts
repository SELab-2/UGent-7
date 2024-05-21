import { Project, ProjectJSON } from './Project.ts';
import { type Student } from './users/Student.ts';
import { type Submission } from './submission/Submission.ts';
import { HyperlinkedRelation } from '@/types/ApiResponse.ts';

export type GroupJSON = {
    id: string;
    score: number;
    project: ProjectJSON;
    students: HyperlinkedRelation;
    submissions: HyperlinkedRelation;
}

export class Group {
    constructor(
        public id: string = '',
        public score: number = -1,
        public project: Project = new Project(),
        public students: Student[] = [],
        public submissions: Submission[] = [],
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
    static fromJSON(group: GroupJSON): Group {
        return new Group(group.id, group.score, Project.fromJSON(group.project));
    }
}
