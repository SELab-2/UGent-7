import { Project } from '@/types/Project';
import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import axios from 'axios';
import { create, deleteId, get, getList, patch, processError } from '@/composables/services/helpers.ts';
import { type Response } from '@/types/Response.ts';

interface ProjectState {
    projects: Ref<Project[] | null>;
    project: Ref<Project | null>;
    getProjectByID: (id: string) => Promise<void>;
    getProjectsByCourse: (courseId: string) => Promise<void>;
    getProjectsByStudent: (studentId: string) => Promise<void>;
    getProjectsByAssistant: (assistantId: string) => Promise<void>;
    getProjectsByTeacher: (teacherId: string) => Promise<void>;
    getProjectsByCourseAndDeadline: (courseId: string, deadlineDate: Date) => Promise<void>;
    createProject: (projectData: Project, courseId: string, numberOfGroups: number) => Promise<void>;
    updateProject: (projectData: Project) => Promise<void>;
    deleteProject: (id: string) => Promise<void>;
}

export function useProject(): ProjectState {
    const projects = ref<Project[] | null>(null);
    const project = ref<Project | null>(null);
    const response = ref<Response | null>(null);

    async function getProjectByID(id: string): Promise<void> {
        const endpoint = endpoints.projects.retrieve.replace('{id}', id);
        await get<Project>(endpoint, project, Project.fromJSON);
    }

    async function getProjectsByCourse(courseId: string): Promise<void> {
        const endpoint = endpoints.projects.byCourse.replace('{courseId}', courseId);
        await getList<Project>(endpoint, projects, Project.fromJSON);
    }

    async function getProjectsByStudent(studentId: string): Promise<void> {
        const endpoint = endpoints.projects.byStudent.replace('{studentId}', studentId);
        await getList<Project>(endpoint, projects, Project.fromJSON);
    }

    async function getProjectsByAssistant(assistantId: string): Promise<void> {
        const endpoint = endpoints.projects.byAssistant.replace('{assistantId}', assistantId);
        await getList<Project>(endpoint, projects, Project.fromJSON);
    }

    async function getProjectsByTeacher(teacherId: string): Promise<void> {
        const endpoint = endpoints.projects.byTeacher.replace('{teacherId}', teacherId);
        await getList<Project>(endpoint, projects, Project.fromJSON);
    }

    async function getProjectsByCourseAndDeadline(courseId: string, deadlineDate: Date): Promise<void> {
        const endpoint = endpoints.projects.byCourse.replace('{courseId}', courseId);

        await axios
            .get(endpoint)
            .then((response) => {
                const allProjects = response.data.map((projectData: Project) => Project.fromJSON(projectData));

                // Filter projects based on the deadline date
                // Update the projects ref with the filtered projects
                projects.value = allProjects.filter((project: Project) => {
                    return project.deadline.toDateString() === deadlineDate.toDateString();
                });
            })
            .catch((error) => {
                if (axios.isAxiosError(error)) {
                    processError(error);
                    console.log(error.response?.data);
                } else {
                    console.error('An unexpected error ocurred: ', error);
                }
            });
    }

    async function createProject(projectData: Project, courseId: string, numberOfGroups: number): Promise<void> {
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
            group_size: projectData.group_size
        };

        // Check if the number of groups should be included, only if it is greater than 0
        if (numberOfGroups > 0) {
            requestData.number_groups = numberOfGroups;
        }

        await create<Project>(endpoint, requestData, project, Project.fromJSON, 'multipart/form-data');
    }

    async function updateProject(projectData: Project): Promise<void> {
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
        );
    }

    async function deleteProject(id: string): Promise<void> {
        const endpoint = endpoints.projects.retrieve.replace('{id}', id);
        await deleteId<Project>(endpoint, project, Project.fromJSON);
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
