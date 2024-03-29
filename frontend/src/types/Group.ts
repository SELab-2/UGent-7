import {Project} from "./Projects";
import {Student} from "./Student";
import {Submission} from "./Submission";

export class Group {
    constructor(
        public id: string,
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

    static fromJSONFullObject(group: Group): Group {
        return new Group(
            group.id,
            group.score,
            group.projects,
            group.students,
            group.submissions
        );
    }
}