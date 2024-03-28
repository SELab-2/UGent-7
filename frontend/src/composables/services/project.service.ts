import {Project} from '@/types/Projects.ts';
import { Course } from '@/types/Course';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import axios from 'axios';
import { get, getList, getListMerged, create, delete_id, processError } from '@/composables/services/helpers.ts';


export function useProject() {
    const projects = ref<Project[]|null>(null);
    const project = ref<Project|null>(null);

    async function getProjectByID(id: string) {
        const endpoint = endpoints.projects.retrieve.replace('{id}', id);
        await get<Project>(endpoint, project, Project.fromJSON);
    }

    async function getProjectsByCourse(course_id: string) {
        const endpoint = endpoints.projects.byCourse.replace('{course_id}', course_id);
        await getList<Project>(endpoint, projects, Project.fromJSON);
    }

    async function getProjectsByStudent(student_id: string) {
        const endpoint = endpoints.courses.byStudent.replace('{student_id}', student_id);
        const courses = ref<Course[]|null>(null);
        await getList<Course>(endpoint, courses, Course.fromJSON);

        const endpList = [];
        for (const course of courses.value?courses.value:[]){
            endpList.push(endpoints.projects.byCourse.replace('{course_id}', course.id.toString()));
        }
      
        await getListMerged<Project>(endpList, projects, Project.fromJSON);
    }

    async function getProjectsByCourseAndDeadline(course_id: string, deadlineDate: Date ) {

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
            processError(error);
            console.log(error.data);
        });
    }


    async function createProject(project_data: Project, course_id: string) {
        const endpoint = endpoints.projects.byCourse.replace('{course_id}', course_id);
        await create<Project>(endpoint, 
            {
                name: project_data.name,
                description: project_data.description,
                visible: project_data.visible,
                archived: project_data.archived,
                locked_groups: project_data.locked_groups,
                start_data: project_data.start_date,
                deadline: project_data.deadline,
                max_score: project_data.max_score,
                score_visible: project_data.score_visible,
                group_size: project_data.group_size
            },
        project, Project.fromJSON);
    }

    async function deleteProject(id: string) {
        const endpoint = endpoints.projects.retrieve.replace('{id}', id);
        await delete_id<Project>(endpoint, project, Project.fromJSON);
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