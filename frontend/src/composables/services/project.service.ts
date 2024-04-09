import { Project } from '@/types/Projects.ts';
import { Course } from '@/types/Course';
import { type Ref, ref } from 'vue';
import { endpoints } from '@/config/endpoints.ts';
import axios from 'axios';
import { get, getList, getListMerged, create, deleteId, processError } from '@/composables/services/helpers.ts';

interface ProjectState {
    projects: Ref<Project[] | null>;
    project: Ref<Project | null>;
    getProjectByID: (id: string) => Promise<void>;
    getProjectsByCourse: (courseId: string) => Promise<void>;
    getProjectsByStudent: (studentId: string) => Promise<void>;
    getProjectsByCourseAndDeadline: (courseId: string, deadlineDate: Date) => Promise<void>;
    createProject: (projectData: Project, courseId: string) => Promise<void>;
    deleteProject: (id: string) => Promise<void>;
}

export function useProject(): ProjectState {
    const projects = ref<Project[] | null>(null);
    const project = ref<Project | null>(null);

    async function getProjectByID(id: string): Promise<void> {
        const endpoint = endpoints.projects.retrieve.replace('{id}', id);
        await get<Project>(endpoint, project, Project.fromJSON);
    }

    async function getProjectsByCourse(courseId: string): Promise<void> {
        const endpoint = endpoints.projects.byCourse.replace('{courseId}', courseId);
        await getList<Project>(endpoint, projects, Project.fromJSON);
    }

    async function getProjectsByStudent(studentId: string): Promise<void> {
        const endpoint = endpoints.courses.byStudent.replace('{studentId}', studentId);
        const courses = ref<Course[] | null>(null);
        await getList<Course>(endpoint, courses, Course.fromJSON);

        const endpList = [];
        let coursesValue: Course[] | null = courses.value;
        if (coursesValue === null) {
            coursesValue = [];
        }
        for (const course of coursesValue) {
            endpList.push(endpoints.projects.byCourse.replace('{courseId}', course.id.toString()));
        }

        await getListMerged<Project>(endpList, projects, Project.fromJSON);
    }

    async function getProjectsByCourseAndDeadline(courseId: string, deadlineDate: Date): Promise<void> {
        const endpoint = endpoints.projects.byCourse.replace('{courseId}', courseId);

        await axios
            .get(endpoint)
            .then((response) => {
                const allProjects = response.data.map((projectData: Project) => Project.fromJSON(projectData));

                // Filter projects based on the deadline date
                const projectsWithMatchingDeadline = allProjects.filter((project: Project) => {
                    const projectDeadlineDate = project.deadline;
                    return projectDeadlineDate.toDateString() === deadlineDate.toDateString();
                });

                // Update the projects ref with the filtered projects
                projects.value = projectsWithMatchingDeadline;
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

    async function createProject(projectData: Project, courseId: string): Promise<void> {
        const endpoint = endpoints.projects.byCourse.replace('{courseId}', courseId);
        await create<Project>(
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
            project,
            Project.fromJSON,
            'multipart/form-data'
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

        createProject,
        deleteProject,
    };
}
