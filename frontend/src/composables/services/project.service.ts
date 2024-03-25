import {Project} from '@/types/Projects.ts';
import { Course } from '@/types/Course';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import axios from 'axios';
import { get, getList, getListMerged, create, delete_id, processError } from '@/composables/services/helpers.ts';
import { useToast } from 'primevue/usetoast';


export function useProject() {
    const projects = ref<Project[]|null>(null);
    const project = ref<Project|null>(null);
    const toast = useToast();

    async function getProjectByID(id: number) {
        const endpoint = endpoints.projects.retrieve.replace('{id}', id.toString());
        get<Project>(endpoint, project, Project.fromJSON, toast);
    }

    async function getProjectsByCourse(course_id: number) {
        const endpoint = endpoints.projects.byCourse.replace('{course_id}', course_id.toString());
        getList<Project>(endpoint, projects, Project.fromJSON, toast);
    }

    async function getProjectsByStudent(student_id: string) {
        const endpoint = endpoints.courses.byStudent.replace('{student_id}', student_id);
        const courses = ref<Course[]|null>(null);
        await getList<Course>(endpoint, courses, Course.fromJSON, toast);

        const endpList = [];
        for (const course of courses.value?courses.value:[]){
            endpList.push(endpoints.projects.byCourse.replace('{course_id}', course.id.toString()));
        }
        await getListMerged<Project>(endpList, projects, Project.fromJSON, toast);
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
            processError(error, toast);
            console.log(error.data);
        });
    }


    async function createProject(project_data: any, course_id: string) {
        const endpoint = endpoints.projects.byCourse.replace('{course_id}', course_id);
        create<Project>(endpoint, project_data, project, Project.fromJSON, toast);
    }

    async function deleteProject(id: string) {
        const endpoint = endpoints.projects.retrieve.replace('{id}', id.toString());
        delete_id<Project>(endpoint, project, Project.fromJSON, toast);
    }

    return {
        projects,
        project,
        getProjectByID,
        getProjectsByCourse,
        getProjectsByCourseAndDeadline,
        getProjectsByStudent,

        createProject,
        deleteProject
    };
}