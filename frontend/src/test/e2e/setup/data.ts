const date = new Date();

export const faculty = {
    id: '0',
    name: 'Faculty'
};

export const course = {
    name: 'Course',
    academic_startyear: date.getMonth() > 8 ? date.getFullYear() : date.getFullYear() - 1,
    excerpt: 'This is a course',
    faculty: faculty.id,
    private_course: false
};

