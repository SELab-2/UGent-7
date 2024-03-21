import {Course} from '@/types/Course.ts';
import {ref} from 'vue';

export function useCourses() {
    const courses = ref<Course[]|null>(null);
    const course = ref<Course|null>(null);

    async function getCourseByID(id: number) {
        setTimeout(() => {
            course.value = new Course(id, 'Information Security Yippee', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In purus arcu, pharetra sit amet purus posuere, laoreet ullamcorper mi. Vivamus vitae egestas nibh. Proin id enim condimentum, egestas nisl in, vehicula nunc. Fusce ornare mattis dolor finibus dictum.', 2023);
        }, 1000);
    }

    return {
        courses,
        course,
        getCourseByID
    };
}