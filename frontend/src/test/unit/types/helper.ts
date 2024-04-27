/* eslint-disable @typescript-eslint/no-unsafe-argument */
import { Student } from '@/types/users/Student';
import { Course } from '@/types/Course';
import { Assistant } from '@/types/users/Assistant';
import { Teacher } from '@/types/users/Teacher';
import { User } from '@/types/users/User';
import { Faculty } from '@/types/Faculty';
import { Group } from '@/types/Group';
import { Project } from '@/types/Project';
import { Response } from '@/types/Response';
import { StructureCheck } from '@/types/StructureCheck';
import { SubmissionStatus } from '@/types/SubmisionStatus';
import { Submission } from '@/types/submission/Submission';
import { ExtraCheckResult } from '@/types/submission/ExtraCheckResult.ts';
import { StructureCheckResult } from '@/types/submission/StructureCheckResult';

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
        studentData.roles.slice(),
        studentData.courses.slice(),
        studentData.groups.slice(),
        studentData.faculties.slice(),
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
        assistantData.roles.slice(),
        assistantData.faculties.slice(),
        assistantData.courses.slice(),
        assistantData.create_time,
        assistantData.last_login,
    );
}

export function createTeacher(teacherData: any): Assistant {
    return new Teacher(
        teacherData.id,
        teacherData.username,
        teacherData.email,
        teacherData.first_name,
        teacherData.last_name,
        teacherData.last_enrolled,
        teacherData.is_staff,
        teacherData.roles.slice(),
        teacherData.faculties.slice(),
        teacherData.courses.slice(),
        teacherData.create_time,
        teacherData.last_login,
    );
}

export function createUser(userData: any): User {
    return new User(
        userData.id,
        userData.username,
        userData.email,
        userData.first_name,
        userData.last_name,
        userData.last_enrolled,
        userData.is_staff,
        userData.roles.slice(),
        userData.faculties.slice(),
        userData.create_time,
        userData.last_login,
    );
}

export function createCourse(courseData: any): Course {
    return new Course(
        courseData.id,
        courseData.name,
        courseData.excerpt,
        courseData.description,
        courseData.academic_startyear,
        courseData.parent_course,
        courseData.faculty,
        courseData.teachers.slice(),
        courseData.assistants.slice(),
        courseData.students.slice(),
        courseData.projects.slice(),
    );
}

export function createFaculty(facultyData: any): Faculty {
    return new Faculty(facultyData.id, facultyData.name);
}

export function createGroup(groupData: any): Group {
    return new Group(
        groupData.id,
        groupData.score,
        groupData.project,
        groupData.students.slice(),
        groupData.submissions.slice(),
    );
}

export function createProject(projectData: any): Project {
    return new Project(
        projectData.id,
        projectData.name,
        projectData.description,
        projectData.visible,
        projectData.archived,
        projectData.locked_groups,
        projectData.start_date,
        projectData.deadline,
        projectData.max_score,
        projectData.score_visible,
        projectData.group_size,
        projectData.course,
        projectData.structure_file,
        projectData.structureChecks.slice(),
        projectData.extra_checks.slice(),
        projectData.groups.slice(),
        projectData.submissions.slice(),
    );
}

export function createResponse(responseData: any): Response {
    return new Response(responseData.message);
}

export function createStructureCheck(structureCheckData: any): StructureCheck {
    return new StructureCheck(
        structureCheckData.id,
        structureCheckData.name,
        structureCheckData.obligated_extensions.slice(),
        structureCheckData.blocked_extensions.slice(),
        structureCheckData.project,
    );
}

export function createSubmissionStatus(submissionStatusData: any): SubmissionStatus {
    return new SubmissionStatus(
        submissionStatusData.non_empty_groups,
        submissionStatusData.groups_submitted,
        submissionStatusData.submissions_passed,
    );
}

// export function createSubmission(submissionData: any): Submission {
//     return new Submission(
//         submissionData.id,
//         submissionData.submission_number,
//         submissionData.submission_time,
//         submissionData.files.slice(),
//         submissionData.extra_checks_results.slice(),
//         submissionData.structure_checks_results.slice(),
//         submissionData.is_valid,
//     );
// }

export function createExtraCheckResult(extraCheckResultData: any): ExtraCheckResult {
    return new ExtraCheckResult(
        extraCheckResultData.id,
        extraCheckResultData.result,
        extraCheckResultData.error_message,
        extraCheckResultData.log_file,
        extraCheckResultData.submission,
        extraCheckResultData.extra_check,
        extraCheckResultData.resourcetype,
    );
}
