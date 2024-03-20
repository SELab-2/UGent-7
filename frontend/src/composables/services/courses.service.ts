import {Course} from '@/types/Course.ts';
import {ref} from 'vue';

export function useCourses() {
    const courses = ref<Course[]>([]);

    const loadCourses = async () => {
        const response = await fetch('http://localhost:3000/courses');
        const data = await response.json();

        courses.value = data.map((course: Course) => {
            return Course.fromJSON(course);
        });
    }

    return {
        courses,
        loadCourses
    };
}