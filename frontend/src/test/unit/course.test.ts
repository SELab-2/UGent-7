import { describe, it, expect } from 'vitest'

import { Course } from '@/types/Course.ts'

// "describe" bundles tests about 1 specific thing; here we're testing course
// aka a test suite
describe("course", (): void => {
    // "it" is used to specify tests
    // you can also import "test" instead of "it", because it's the exact same
    // but with "it", it's easy to read => it (referring to the course) returns correct course year
    it("returns correct course year", (): void => {
        const course: Course = new Course("1", "course", "description", 2003)
        // use expect for assertions
        // after expect, there are a multitude of possible functions such as:
        // toBe, toEqual, toContain
        // check https://vitest.dev/api/expect.html for all possibilities
        expect(course.getCourseYear()).toBe("2003 - 2004")
        // assert can also be used instead, if you like its syntax more
        // check out https://vitest.dev/api/assert.html for more info
    })
})