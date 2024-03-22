import {Project} from '@/types/Projects.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import axios from 'axios';
import { get, getList } from '@/composables/services/helpers.ts';


export function useProject() {
    const projects = ref<Project[]|null>(null);
    const project = ref<Project|null>(null);

    async function getProjectByID(id: number) {
        const endpoint = endpoints.projects.retrieve.replace('{id}', id.toString());
        get<Project>(endpoint, project, Project.fromJSON);
        console.log(project)
    }

    async function getProjectsByCourse(course_id: number) {
        const endpoint = endpoints.projects.byCourse.replace('{course_id}', course_id.toString());
        getList<Project>(endpoint, projects, Project.fromJSON);
        console.log(projects.value ? projects.value.map((project, index) => `Project ${index + 1}: ${JSON.stringify(project)}`) : 'Projects is null');
    }

    async function getProjectsByCourseAndDeadline(course_id: number, deadlineDate: Date ) {

        const endpoint = endpoints.projects.byCourse.replace('{course_id}', course_id.toString());

        axios.get(endpoint).then(response => {
            const allProjects = response.data.map((projectData: Project) => Project.fromJSON(projectData));

            // Filter projects based on the deadline date
            const projectsWithMatchingDeadline = allProjects.filter((project: Project) => {
                const projectDeadlineDate = project.deadline;
                return projectDeadlineDate.toDateString() === deadlineDate.toDateString();
            });

            // Update the projects ref with the filtered projects
            projects.value = projectsWithMatchingDeadline;
        }).catch(error => {
            console.log(error.data);
        });

        console.log(projects.value ? projects.value.map((project, index) => `Project ${index + 1}: ${JSON.stringify(project)}`) : 'Projects is null');
    }

    return {
        projects,
        project,
        getProjectByID,
        getProjectsByCourse,
        getProjectsByCourseAndDeadline
    };
}