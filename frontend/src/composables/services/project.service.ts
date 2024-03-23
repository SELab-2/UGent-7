import {Project} from '@/types/Projects.ts';
import {ref} from 'vue';
import axios from 'axios';
import {endpoints} from '@/config/endpoints.ts';

export function useCourses() {
    const courses = ref<Project[]|null>(null);
    const course = ref<Project|null>(null);

    async function getCourseByID(id: number) {
        const endpoint = endpoints.projects.retrieve.replace('{id}', id.toString());

        axios.get(endpoint).then(response => {
            course.value = Project.fromJSON(response.data);
        }).catch(error => {
            console.log(error.data);
        });

        console.log(Project)
    }

    return {
        courses,
        course,
        getCourseByID
    };
}