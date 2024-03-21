import {Course} from '@/types/Course.ts';
import {ref} from 'vue';
import axios from 'axios';
import {endpoints} from '@/config/endpoints.ts';

export function useCourses() {
    const courses = ref<Course[]|null>(null);
    const course = ref<Course|null>(null);

    async function getCourseByID(id: number) {
        const endpoint = endpoints.courses.retrieve.replace('{id}', id.toString());

        axios.get(endpoint).then(response => {
            course.value = Course.fromJSON(response.data);
        }).catch(error => {
            console.log(error.data);
        });

        console.log(Course)
    }

    return {
        courses,
        course,
        getCourseByID
    };
}