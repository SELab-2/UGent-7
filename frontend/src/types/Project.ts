import moment from 'moment';
import { Course } from './Course.ts';
import { type ExtraCheck } from './ExtraCheck.ts';
import { type Group } from './Group.ts';
import { type StructureCheck } from './StructureCheck.ts';
import { type Submission } from './submission/Submission.ts';

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
        public structureChecks: StructureCheck[] | null = null,
        public extra_checks: ExtraCheck[] | null = null,
        public groups: Group[] | null = null,
        public submissions: Submission[] | null = null,
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
     * Get the formatted start date of the project.
     *
     * @returns The formatted start date of the project.
     */
    public getFormattedStartDate(): string {
        return moment(this.start_date).format('DD MMMM YYYY');
    }

    /**
     * Get the formatted deadline hour of the project.
     *
     * @returns The formatted deadline hour of the project.
     */
    public getFormattedDeadlineHour(): string {
        return moment(this.deadline).format('HH:mm');
    }

    /**
     * Get the days left until the deadline of the project.
     *
     * @returns The days left until the deadline of the project.
     */
    public getDaysLeft(): number {
        return moment(this.deadline).diff(moment(), 'days');
    }

    /**
     * Get the formatted deadline of the project.
     *
     * @returns The formatted deadline of the project.
     */
    public getFormattedDeadline(): string {
        return moment(this.deadline).format('DD MMMM YYYY');
    }

    /**
     * Get the group number of a group.
     *
     * @param group The group to get the number of.
     * @returns The number of the group.
     */
    public getGroupNumber(group: Group): number {
        const groups = this.groups ?? [];

        return groups.sort((a, b) => parseInt(a.id) - parseInt(b.id)).findIndex((g) => g.id === group.id) + 1;
    }

    /**
     * Check if the project is locked.
     *
     * @returns True if the project is locked, false otherwise.
     */
    public isLocked(): boolean {
        console.log("hier")
        console.log(this.start_date);
        return !this.visible || this.archived || this.locked_groups || moment(this.start_date).isBefore();
    }

    /**
     * Convert a project object to a project instance.
     *
     * @param project
     */
    static fromJSON(project: Project): Project {
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
