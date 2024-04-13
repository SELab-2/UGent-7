
import { Student } from '@/types/users/Student';
import { Course } from '@/types/Course';
import { Assistant } from '@/types/users/Assistant';

export function createStudent(studentData: any): Student {
    return new Student(
        studentData.id,
        studentData.username,
        studentData.email,
        studentData.first_name,
        studentData.last_name,
        studentData.is_staff,
        studentData.last_enrolled,
        studentData.create_time,
        studentData.last_login,
        studentData.studentId,
        studentData.roles,
        studentData.courses,
        studentData.groups,
        studentData.faculties,
    );
}

export function createAssistant(assistantData: any): Assistant {
    return new Assistant(
        assistantData.id,
        assistantData.username,
        assistantData.email,
        assistantData.first_name,
        assistantData.last_name,
        assistantData.last_enrolled,
        assistantData.is_staff,
        assistantData.roles,
        assistantData.faculties,
        assistantData.courses,
        assistantData.create_time,
        assistantData.last_login,
    );
}


export function createCourse(courseData: any): Course {
    return new Course(
        courseData.id,
        courseData.name,
        courseData.description,
        courseData.academic_startyear,
        courseData.parent_course,
        courseData.faculty,
        courseData.teachers,
        courseData.assistants,
        courseData.students,
        courseData.projects,
    );
}
