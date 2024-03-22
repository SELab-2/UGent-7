import { describe, it, expect } from 'vitest'

import { Course } from '../Course.ts'

describe("course", (): void => {
    it("returns correct course year", (): void => {
        const course: Course = new Course(1, "course", "description", 2003)
        expect(course.getCourseYear()).toBe("2003 - 2004")
    })
})