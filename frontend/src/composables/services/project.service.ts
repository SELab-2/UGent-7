import {Project} from '@/types/Projects.ts';
import {ref} from 'vue';
import {endpoints} from '@/config/endpoints.ts';
import axios from 'axios';
import { get, getList, getListMerged } from '@/composables/services/helpers.ts';
import { Course } from '@/types/Course';
import { useToast } from 'primevue/usetoast';


export function useProject() {
    const projects = ref<Project[]|null>(null);
    const project = ref<Project|null>(null);
    const toast = useToast();

    async function getProjectByID(id: number) {
        const endpoint = endpoints.projects.retrieve.replace('{id}', id.toString());
        get<Project>(endpoint, project, Project.fromJSON, toast);
        console.log(project)
    }

    async function getProjectsByCourse(course_id: number) {
        const endpoint = endpoints.projects.byCourse.replace('{course_id}', course_id.toString());
        getList<Project>(endpoint, projects, Project.fromJSON, toast);
        console.log(projects.value ? projects.value.map((project, index) => `Project ${index + 1}: ${JSON.stringify(project)}`) : 'Projects is null');
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
        console.log(projects.value ? projects.value.map((project, index) => `Project ${index + 1}: ${JSON.stringify(project)}`) : 'Projects is null');
    }

    async function getProjectWithCourseContext(student_id: string) {
        const endpoint = endpoints.courses.byStudent.replace('{student_id}', student_id);
        const courses = ref<Course[]|null>(null);
        await getList<Course>(endpoint, courses, Course.fromJSON, toast);

        for (const course of courses.value ? courses.value : []) {
            const courseEndpoint = endpoints.projects.byCourse.replace('{course_id}', course.id.toString());
            axios.get(courseEndpoint).then(response => {
                const allProjectsFromCourse = response.data.map((projectData: any) => Project.fromJSONWithCourse(projectData, course));
                projects.value = [...(projects.value || []), ...allProjectsFromCourse];
            });
        }
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
        getProjectsByCourseAndDeadline,
        getProjectsByStudent,
        getProjectWithCourseContext
    };
}