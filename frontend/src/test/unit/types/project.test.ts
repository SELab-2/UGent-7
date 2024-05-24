/* eslint-disable @typescript-eslint/no-unused-vars */
import { describe, it } from 'vitest';

describe('placeholder', (): void => {
    it('aaaaaaaa', () => {});
});

// import { describe, it, expect } from 'vitest';

// import { Project } from '@/types/Project';
// import { projectData } from './data';
// import { createProject } from './helper';

// describe('project type', () => {
//     it('create instance of project with correct properties', () => {
//         const project = createProject(projectData);

//         expect(project).toBeInstanceOf(Project);
//         expect(project.id).toBe(projectData.id);
//         expect(project.name).toBe(projectData.name);
//         expect(project.description).toBe(projectData.description);
//         expect(project.visible).toBe(projectData.visible);
//         expect(project.archived).toBe(projectData.archived);
//         expect(project.locked_groups).toBe(projectData.locked_groups);
//         expect(project.start_date).toStrictEqual(projectData.start_date);
//         expect(project.deadline).toStrictEqual(projectData.deadline);
//         expect(project.max_score).toBe(projectData.max_score);
//         expect(project.score_visible).toBe(projectData.score_visible);
//         expect(project.group_size).toBe(projectData.group_size);
//         expect(project.structure_file).toStrictEqual(projectData.structure_file);
//         expect(project.course).toStrictEqual(projectData.course);
//         expect(project.structureChecks).toStrictEqual(projectData.structureChecks);
//         expect(project.extra_checks).toStrictEqual(projectData.extra_checks);
//         expect(project.groups).toStrictEqual(projectData.groups);
//         expect(project.submissions).toStrictEqual(projectData.submissions);
//     });

//     it('create a project instance from JSON data', () => {
//         const projectJSON = { ...projectData };
//         const project = Project.fromJSON(projectJSON);

//         expect(project).toBeInstanceOf(Project);
//         expect(project.id).toBe(projectData.id);
//         expect(project.name).toBe(projectData.name);
//         expect(project.description).toBe(projectData.description);
//         expect(project.visible).toBe(projectData.visible);
//         expect(project.archived).toBe(projectData.archived);
//         expect(project.locked_groups).toBe(projectData.locked_groups);
//         expect(project.start_date).toStrictEqual(projectData.start_date);
//         expect(project.deadline).toStrictEqual(projectData.deadline);
//         expect(project.max_score).toBe(projectData.max_score);
//         expect(project.score_visible).toBe(projectData.score_visible);
//         expect(project.group_size).toBe(projectData.group_size);
//     });
// });
