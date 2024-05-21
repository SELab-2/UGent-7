import { Project } from '@/types/Project';
import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { create, deleteId, get, getList, patch} from '@/composables/services/helpers.ts';
import { type Response } from '@/types/Response.ts';

interface ProjectState {
    projects: Ref<Project[] | null>;
    project: Ref<Project | null>;
    getProjectByID: (id: string, selfprocessError?: boolean) => Promise<void>;
    getProjectsByCourse: (courseId: string, selfprocessError?: boolean) => Promise<void>;
    getProjectsByStudent: (studentId: string, selfprocessError?: boolean) => Promise<void>;
    getProjectsByAssistant: (assistantId: string, selfprocessError?: boolean) => Promise<void>;
    getProjectsByTeacher: (teacherId: string, selfprocessError?: boolean) => Promise<void>;
    getProjectsByCourseAndDeadline: (courseId: string, deadlineDate: Date, selfprocessError?: boolean) => Promise<void>;
    createProject: (
        projectData: Project,
        courseId: string,
        numberOfGroups: number,
        selfprocessError?: boolean,
    ) => Promise<void>;
    updateProject: (projectData: Project, selfprocessError?: boolean) => Promise<void>;
    deleteProject: (id: string, selfprocessError?: boolean) => Promise<void>;
}

export function useProject(): ProjectState {
    const projects = ref<Project[] | null>(null);
    const project = ref<Project | null>(null);
    const response = ref<Response | null>(null);

    async function getProjectByID(id: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.projects.retrieve.replace('{id}', id);
        await get<Project>(endpoint, project, Project.fromJSON, selfprocessError);
    }

    async function getProjectsByCourse(courseId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.projects.byCourse.replace('{courseId}', courseId);
        await getList<Project>(endpoint, projects, Project.fromJSON, selfprocessError);
    }

    async function getProjectsByStudent(studentId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.projects.byStudent.replace('{studentId}', studentId);
        await getList<Project>(endpoint, projects, Project.fromJSON, selfprocessError);
    }

    async function getProjectsByAssistant(assistantId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.projects.byAssistant.replace('{assistantId}', assistantId);
        await getList<Project>(endpoint, projects, Project.fromJSON, selfprocessError);
    }

    async function getProjectsByTeacher(teacherId: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.projects.byTeacher.replace('{teacherId}', teacherId);
        await getList<Project>(endpoint, projects, Project.fromJSON, selfprocessError);
    }

    async function getProjectsByCourseAndDeadline(
        courseId: string,
        deadlineDate: Date,
        selfprocessError: boolean = true,
    ): Promise<void> {
        await getProjectsByCourse(courseId, selfprocessError);
        const allProjects = (projects.value ?? []).map((projectData: Project) => Project.fromJSON(projectData));
        projects.value = allProjects.filter((project: Project) => {
            return project.deadline.toDateString() === deadlineDate.toDateString();
        });
    }

    async function createProject(
        projectData: Project,
        courseId: string,
        numberOfGroups: number,
        selfprocessError: boolean = true,
    ): Promise<void> {
        const endpoint = endpoints.projects.byCourse.replace('{courseId}', courseId);

        // Initialize an empty object to hold the data to send
        const requestData: Record<string, unknown> = {
            name: projectData.name,
            description: projectData.description,
            visible: projectData.visible,
            archived: projectData.archived,
            locked_groups: projectData.locked_groups,
            start_date: projectData.start_date,
            deadline: projectData.deadline,
            max_score: projectData.max_score,
            score_visible: projectData.score_visible,
            group_size: projectData.group_size,
            zip_structure: projectData.structure_file,
        };

        // Check if the number of groups should be included, only if it is greater than 0
        if (numberOfGroups > 0) {
            requestData.number_groups = numberOfGroups;
        }

        await create<Project>(
            endpoint,
            requestData,
            project,
            Project.fromJSON,
            'multipart/form-data',
            selfprocessError,
        );
    }

    async function updateProject(projectData: Project, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.projects.retrieve.replace('{id}', projectData.id);
        await patch(
            endpoint,
            {
                name: projectData.name,
                description: projectData.description,
                visible: projectData.visible,
                archived: projectData.archived,
                locked_groups: projectData.locked_groups,
                start_date: projectData.start_date,
                deadline: projectData.deadline,
                max_score: projectData.max_score,
                score_visible: projectData.score_visible,
                group_size: projectData.group_size,
                zip_structure: projectData.structure_file,
            },
            response,
            'multipart/form-data',
            selfprocessError,
        );
    }

    async function deleteProject(id: string, selfprocessError: boolean = true): Promise<void> {
        const endpoint = endpoints.projects.retrieve.replace('{id}', id);
        await deleteId<Project>(endpoint, project, Project.fromJSON, selfprocessError);
    }

    return {
        projects,
        project,
        getProjectByID,
        getProjectsByCourse,
        getProjectsByCourseAndDeadline,
        getProjectsByStudent,
        getProjectsByTeacher,
        getProjectsByAssistant,

        createProject,
        updateProject,
        deleteProject,
    };
}
