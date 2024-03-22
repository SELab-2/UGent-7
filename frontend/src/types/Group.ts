import { Project } from "./Projects";
import { Student } from "./Student";
import { Submission } from "./Submission";

export class Group {
    constructor(
        public id: number,
        public score: number = -1,
        public projects: Project[] = [],
        public students: Student[] = [],
        public submissions: Submission[] = []
    ) {
    }

    /**
     * Convert a group object to a group instance.
     *
     * @param group
     */
        static fromJSON(group: Group): Group {
            return new Group(
                group.id,
                group.score
            );
        }
}