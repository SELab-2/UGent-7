import { Course } from "./Course";
import { Extra_check } from "./Extra_check";
import { Group } from "./Group";
import { Structure_check } from "./Structure_check";
import { Submission } from "./Submission";

export class Project {
    constructor(
        public id: string,
        public name: string,
        public description: string,
        public visible: boolean,
        public archived: boolean,
        public locked_groups: boolean,
        public start_date: Date,
        public deadline: Date,
        public max_score: number,
        public score_visible: boolean,
        public group_size: number,

        public course: Course|null = null,
        public structure_checks: Structure_check[] = [],
        public extra_checks: Extra_check[] = [],
        public groups: Group[] = [],
        public submissions: Submission[] = []
    ) {
    }

    /**
     * Convert a project object to a project instance.
     *
     * @param project
     */
    static fromJSON(project: Project): Project {
        return new Project(
            project.id,
            project.name,
            project.description,
            project.visible,
            project.archived,
            project.locked_groups,
            new Date(project.start_date),
            new Date(project.deadline),
            project.max_score,
            project.score_visible,
            project.group_size
        );
    }
}