import {Project} from '@/types/Projects.ts';
import { Course } from '@/types/Course';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import axios from 'axios';
import { get, getList, getListMerged, create, delete_id, processError } from '@/composables/services/helpers.ts';
import {ComposerTranslation} from "vue-i18n";


export function useProject() {
    const projects = ref<Project[]|null>(null);
    const project = ref<Project|null>(null);

    async function getProjectByID(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.projects.retrieve.replace('{id}', id);
        await get<Project>(endpoint, project, Project.fromJSON, t);
    }

    async function getProjectsByCourse(course_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.projects.byCourse.replace('{course_id}', course_id);
        await getList<Project>(endpoint, projects, Project.fromJSON, t);
    }

    async function getProjectsByStudent(student_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.courses.byStudent.replace('{student_id}', student_id);
        const courses = ref<Course[]|null>(null);
        await getList<Course>(endpoint, courses, Course.fromJSON, t);

        const endpList = [];
        for (const course of courses.value?courses.value:[]){
            endpList.push(endpoints.projects.byCourse.replace('{course_id}', course.id.toString()));
        }
      
        await getListMerged<Project>(endpList, projects, Project.fromJSON, t);
    }

    async function getProjectsByCourseAndDeadline(course_id: string, deadlineDate: Date, t: ComposerTranslation ) {

        const endpoint = endpoints.projects.byCourse.replace('{course_id}', course_id);

        await axios.get(endpoint).then(response => {
            const allProjects = response.data.map((projectData: Project) => Project.fromJSON(projectData));

            // Filter projects based on the deadline date
            const projectsWithMatchingDeadline = allProjects.filter((project: Project) => {
                const projectDeadlineDate = project.deadline;
                return projectDeadlineDate.toDateString() === deadlineDate.toDateString();
            });

            // Update the projects ref with the filtered projects
            projects.value = projectsWithMatchingDeadline;
        }).catch(error => {
            processError(error, t);
            console.log(error.data);
        });
    }


    async function createProject(project_data: any, course_id: string, t: ComposerTranslation) {
        const endpoint = endpoints.projects.byCourse.replace('{course_id}', course_id);
        await create<Project>(endpoint, project_data, project, Project.fromJSON, t);
    }

    async function deleteProject(id: string, t: ComposerTranslation) {
        const endpoint = endpoints.projects.retrieve.replace('{id}', id);
        await delete_id<Project>(endpoint, project, Project.fromJSON, t);
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