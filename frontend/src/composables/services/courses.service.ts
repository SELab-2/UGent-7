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

        console.log(course)
    }

    async function getCourses() {
        const endpoint = endpoints.courses.index;

        axios.get(endpoint).then(response => {
            courses.value = response.data.map((courseData: Course) => Course.fromJSON(courseData));
        }).catch(error => {
            console.log(error.data);
        });

        console.log(courses.value ? courses.value.map((course, index) => `Course ${index + 1}: ${JSON.stringify(course)}`) : 'Courses is null');
    }

    return {
        courses,
        course,
        getCourseByID,
        getCourses
    };
}