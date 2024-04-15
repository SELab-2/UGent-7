import { Course } from './Course.ts';
import { type ExtraCheck } from './ExtraCheck.ts';
import { type Group } from './Group.ts';
import { type StructureCheck } from './StructureCheck.ts';
import { type Submission } from './Submission.ts';
import moment from 'moment';

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
        public course: Course | null = null,
        public structure_file: File | null = null,
        public structureChecks: StructureCheck[] = [],
        public extra_checks: ExtraCheck[] = [],
        public groups: Group[] = [],
        public submissions: Submission[] = [],
    ) {}

    /**
     * Get the progress of the project based on its deadline.
     *
     * @returns The progress of the project as a number between 0 and 100.
     */
    public getProgress(): number {
        const max = moment(this.deadline).diff(this.start_date, 'day');
        const now = moment(this.deadline).diff(moment(), 'day');
        return Math.min(100, Math.round(100 - (now / max) * 100));
    }

    /**
     * Convert a project object to a project instance.
     *
     * @param project
     */
    static fromJSON(project: Project|any): Project {
        let course = null;

        if (project.course !== null && project.course !== undefined) {
            course = Course.fromJSON(project.course);
        }

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
            project.group_size,
            course,
        );
    }
}
