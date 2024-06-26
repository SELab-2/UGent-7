import moment from 'moment';
import { type TreeNode } from 'primevue/treenode';
import { PrimeIcons } from 'primevue/api';
import { Course, type CourseJSON } from './Course.ts';
import { type ExtraCheck } from './ExtraCheck.ts';
import { type Group } from './Group.ts';
import { type StructureCheck } from './StructureCheck.ts';
import { type Submission } from './submission/Submission.ts';
import { SubmissionStatus, type SubmissionStatusJSON } from '@/types/SubmisionStatus.ts';
import { type HyperlinkedRelation } from '@/types/ApiResponse.ts';

export interface ProjectJSON {
    id: string;
    name: string;
    description: string;
    visible: boolean;
    archived: boolean;
    locked_groups: boolean;
    start_date: string;
    deadline: string;
    max_score: number;
    score_visible: boolean;
    group_size: number;
    course: CourseJSON;
    status: SubmissionStatusJSON;
    structure_checks: HyperlinkedRelation;
    extra_checks: HyperlinkedRelation;
    groups: HyperlinkedRelation;
    submissions: HyperlinkedRelation;
}

export class Project {
    constructor(
        public id: string = '',
        public name: string = '',
        public description: string = '',
        public visible: boolean = true,
        public archived: boolean = false,
        public locked_groups: boolean = false,
        public start_date: Date = new Date(),
        public deadline: Date = new Date(),
        public max_score: number = 10,
        public score_visible: boolean = true,
        public group_size: number = 1,
        public course: Course = new Course(),
        public status: SubmissionStatus = new SubmissionStatus(),
        public structure_checks: StructureCheck[] = [],
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
        return moment(this.deadline).startOf('day').diff(moment().startOf('day'), 'days');
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
        return this.groups.sort((a, b) => parseInt(a.id) - parseInt(b.id)).findIndex((g) => g.id === group.id) + 1;
    }

    /**
     * Check if the project is locked.
     *
     * @returns True if the project is locked, false otherwise.
     */
    public isLocked(): boolean {
        return (
            !this.visible || this.archived || this.locked_groups
            // moment(this.start_date).isBefore(moment().startOf('day'))
        );
    }

    /**
     * Given a list of structureChecks (directory path), return a list of TreeNodes representing the tree hierarchy
     * of the structure checks.
     *
     * @param structureChecks
     */
    public static getNodes(structureChecks: StructureCheck[] | undefined): TreeNode[] {
        const nodes: TreeNode[] = [];

        if (structureChecks !== undefined) {
            for (const [i, check] of structureChecks.entries()) {
                const hierarchy = check.getDirectoryHierarchy();
                let currentNodes = nodes;

                for (const [j, part] of hierarchy.entries()) {
                    let node = currentNodes.find((node) => node.label === part);

                    if (node === undefined) {
                        node = Project.newTreeNode(check, `${i}${j}`, part, j === hierarchy.length - 1);
                        currentNodes.push(node);
                    }

                    currentNodes = node.children ?? [];
                }
            }
        }

        return nodes;
    }

    /**
     * Construct a tree node from a structure check folder path.
     *
     * @param check
     * @param key
     * @param label
     * @param leaf
     */
    private static newTreeNode(check: StructureCheck, key: string, label: string, leaf: boolean = false): TreeNode {
        const node: TreeNode = {
            key,
            label,
            data: check,
            icon: PrimeIcons.FOLDER,
            check: leaf,
            children: [],
        };

        if (leaf) {
            node.children = [
                {
                    key: key + '-obligated',
                    icon: PrimeIcons.CHECK_CIRCLE,
                    data: check,
                    obligated: true,
                },
                {
                    key: key + '-blocked',
                    icon: PrimeIcons.TIMES_CIRCLE,
                    data: check,
                    blocked: true,
                },
            ];
        }

        return node;
    }

    /**
     * Convert a project object to a project instance.
     *
     * @param project
     */
    static fromJSON(project: ProjectJSON): Project {
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
            Course.fromJSON(project.course),
            SubmissionStatus.fromJSON(project.status),
        );
    }
}
