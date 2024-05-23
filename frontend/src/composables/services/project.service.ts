import { Project, ProjectJSON } from '@/types/Project';
import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import { i18n } from '@/config/i18n.ts';
import axios from 'axios';
import { create, deleteId, get, getList, patch, processError } from '@/composables/services/helpers.ts';
import { type Response } from '@/types/Response.ts';
import { useMessagesStore } from '@/store/messages.store.ts';

interface ProjectState {
    projects: Ref<Project[] | null>;
    project: Ref<Project | null>;
    getProjectByID: (id: string, selfProcessError?: boolean) => Promise<void>;
    getProjectsByCourse: (courseId: string, selfProcessError?: boolean) => Promise<void>;
    getProjectsByStudent: (studentId: string, selfProcessError?: boolean) => Promise<void>;
    getProjectsByAssistant: (assistantId: string, selfProcessError?: boolean) => Promise<void>;
    getProjectsByTeacher: (teacherId: string, selfProcessError?: boolean) => Promise<void>;
    getProjectsByCourseAndDeadline: (courseId: string, deadlineDate: Date, selfProcessError?: boolean) => Promise<void>;
    createProject: (
        projectData: Project,
        courseId: string,
        numberOfGroups: number,
        selfProcessError?: boolean,
    ) => Promise<void>;
    updateProject: (projectData: Project, selfProcessError?: boolean) => Promise<void>;
    deleteProject: (id: string, selfProcessError?: boolean) => Promise<void>;
}

export function useProject(): ProjectState {
    const projects = ref<Project[] | null>(null);
    const project = ref<Project | null>(null);
    const response = ref<Response | null>(null);

    async function getProjectByID(id: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.projects.retrieve.replace('{id}', id);
        await get<Project>(endpoint, project, Project.fromJSON, selfProcessError);
    }

    async function getProjectsByCourse(courseId: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.projects.byCourse.replace('{courseId}', courseId);
        await getList<Project>(endpoint, projects, Project.fromJSON, selfProcessError);
    }

    async function getProjectsByStudent(studentId: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.projects.byStudent.replace('{studentId}', studentId);
        await getList<Project>(endpoint, projects, Project.fromJSON, selfProcessError);
    }

    async function getProjectsByAssistant(assistantId: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.projects.byAssistant.replace('{assistantId}', assistantId);
        await getList<Project>(endpoint, projects, Project.fromJSON, selfProcessError);
    }

    async function getProjectsByTeacher(teacherId: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.projects.byTeacher.replace('{teacherId}', teacherId);
        await getList<Project>(endpoint, projects, Project.fromJSON, selfProcessError);
    }

    async function getProjectsByCourseAndDeadline(
        courseId: string,
        deadlineDate: Date,
        selfProcessError: boolean = true,
    ): Promise<void> {
        await getProjectsByCourse(courseId, selfProcessError);

        if (projects.value !== null) {
            projects.value = projects.value.filter((project: Project) => {
                return project.deadline.toDateString() === deadlineDate.toDateString();
            });
        }
    }

    async function createProject(
        projectData: Project,
        courseId: string,
        numberOfGroups: number,
        selfProcessError: boolean = true,
    ): Promise<void> {
        const { t } = i18n.global;
        const { addSuccessMessage } = useMessagesStore();

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
            selfProcessError,
        );
        addSuccessMessage(
            t('toasts.messages.success'),
            t('toasts.messages.projects.create.success', [project.value?.name]),
        );
    }

    async function updateProject(projectData: Project, selfProcessError: boolean = true): Promise<void> {
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
            },
            response,
            'multipart/form-data',
            selfProcessError,
        );
    }

    async function deleteProject(id: string, selfProcessError: boolean = true): Promise<void> {
        const endpoint = endpoints.projects.retrieve.replace('{id}', id);
        await deleteId<Project>(endpoint, project, Project.fromJSON, selfProcessError);
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
