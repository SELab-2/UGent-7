import { describe, it, expect, beforeEach } from 'vitest'
import { useProject } from '@/composables/services/project.service.ts'

const {
    projects,
    project,
    getProjectByID,
    getProjectsByCourse,
    getProjectsByCourseAndDeadline,
    getProjectsByStudent,

    createProject,
    deleteProject
} = useProject()

describe('project', (): void => {
    it('gets project data by id', async () => {
        await getProjectByID('0')
        expect(project.value).not.toBeNull()
        expect(project.value?.name).toBe('sel2')
        expect(project.value?.course).toBeNull()
        expect(project.value?.description).toBe('this is a test')
        expect(project.value?.visible).toBe(true)
        expect(project.value?.archived).toBe(false)
        expect(project.value?.locked_groups).toBe(false)
        expect(project.value?.start_date).toStrictEqual(
            new Date('July 21, 2024 01:15:00')
        )
        expect(project.value?.deadline).toStrictEqual(
            new Date('July 23, 2024 01:15:00')
        )
        expect(project.value?.max_score).toBe(100)
        expect(project.value?.score_visible).toBe(true)
        expect(project.value?.group_size).toBe(8)
        expect(project.value?.course).toBeNull()
        expect(project.value?.structure_checks).toEqual([])
        expect(project.value?.extra_checks).toEqual([])
        expect(project.value?.groups).toEqual([])
        expect(project.value?.submissions).toEqual([])
    })

    it('gets projects data', async () => {
        await getProjectsByCourse('1')
        expect(projects).not.toBeNull()
        expect(Array.isArray(projects.value)).toBe(true)
        expect(projects.value?.length).toBe(2)
        expect(projects.value).not.toBeNull()
        expect(projects.value?.[0]?.name).toBe('sel2')
        expect(projects.value?.[0]?.course).toBeNull()
        expect(projects.value?.[0]?.description).toBe('this is a test')
        expect(projects.value?.[0]?.visible).toBe(true)
        expect(projects.value?.[0]?.archived).toBe(false)
        expect(projects.value?.[0]?.locked_groups).toBe(false)
        expect(projects.value?.[0]?.start_date).toStrictEqual(
            new Date('July 21, 2024 01:15:00')
        )
        expect(projects.value?.[0]?.deadline).toStrictEqual(
            new Date('July 23, 2024 01:15:00')
        )
        expect(projects.value?.[0]?.max_score).toBe(100)
        expect(projects.value?.[0]?.score_visible).toBe(true)
        expect(projects.value?.[0]?.group_size).toBe(8)
        expect(projects.value?.[0]?.course).toBeNull()
        expect(projects.value?.[0]?.structure_checks).toEqual([])
        expect(projects.value?.[0]?.extra_checks).toEqual([])
        expect(projects.value?.[0]?.groups).toEqual([])
        expect(projects.value?.[0]?.submissions).toEqual([])

        expect(projects.value?.[1]?.name).toBe('sel3')
        expect(projects.value?.[1]?.course).toBeNull()
        expect(projects.value?.[1]?.description).toBe('make a project')
        expect(projects.value?.[1]?.visible).toBe(true)
        expect(projects.value?.[1]?.archived).toBe(false)
        expect(projects.value?.[1]?.locked_groups).toBe(false)
        expect(projects.value?.[1]?.start_date).toStrictEqual(
            new Date('July 21, 2024 01:15:00')
        )
        expect(projects.value?.[1]?.deadline).toStrictEqual(
            new Date('July 23, 2024 01:15:00')
        )
        expect(projects.value?.[1]?.max_score).toBe(20)
        expect(projects.value?.[1]?.score_visible).toBe(false)
        expect(projects.value?.[1]?.group_size).toBe(3)
        expect(projects.value?.[1]?.course).toBeNull()
        expect(projects.value?.[1]?.structure_checks).toEqual([])
        expect(projects.value?.[1]?.extra_checks).toEqual([])
        expect(projects.value?.[1]?.groups).toEqual([])
        expect(projects.value?.[1]?.submissions).toEqual([])
    })

    it('gets projects data', async () => {
        await getProjectsByStudent('1')
        expect(projects).not.toBeNull()
        expect(Array.isArray(projects.value)).toBe(true)
        expect(projects.value?.length).toBe(2)
        expect(projects.value).not.toBeNull()
        expect(projects.value?.[0]?.name).toBe('sel2')
        expect(projects.value?.[0]?.course).toBeNull()
        expect(projects.value?.[0]?.description).toBe('this is a test')
        expect(projects.value?.[0]?.visible).toBe(true)
        expect(projects.value?.[0]?.archived).toBe(false)
        expect(projects.value?.[0]?.locked_groups).toBe(false)
        expect(projects.value?.[0]?.start_date).toStrictEqual(
            new Date('July 21, 2024 01:15:00')
        )
        expect(projects.value?.[0]?.deadline).toStrictEqual(
            new Date('July 23, 2024 01:15:00')
        )
        expect(projects.value?.[0]?.max_score).toBe(100)
        expect(projects.value?.[0]?.score_visible).toBe(true)
        expect(projects.value?.[0]?.group_size).toBe(8)
        expect(projects.value?.[0]?.course).toBeNull()
        expect(projects.value?.[0]?.structure_checks).toEqual([])
        expect(projects.value?.[0]?.extra_checks).toEqual([])
        expect(projects.value?.[0]?.groups).toEqual([])
        expect(projects.value?.[0]?.submissions).toEqual([])

        expect(projects.value?.[1]?.name).toBe('sel3')
        expect(projects.value?.[1]?.course).toBeNull()
        expect(projects.value?.[1]?.description).toBe('make a project')
        expect(projects.value?.[1]?.visible).toBe(true)
        expect(projects.value?.[1]?.archived).toBe(false)
        expect(projects.value?.[1]?.locked_groups).toBe(false)
        expect(projects.value?.[1]?.start_date).toStrictEqual(
            new Date('July 21, 2024 01:15:00')
        )
        expect(projects.value?.[1]?.deadline).toStrictEqual(
            new Date('July 23, 2024 01:15:00')
        )
        expect(projects.value?.[1]?.max_score).toBe(20)
        expect(projects.value?.[1]?.score_visible).toBe(false)
        expect(projects.value?.[1]?.group_size).toBe(3)
        expect(projects.value?.[1]?.course).toBeNull()
        expect(projects.value?.[1]?.structure_checks).toEqual([])
        expect(projects.value?.[1]?.extra_checks).toEqual([])
        expect(projects.value?.[1]?.groups).toEqual([])
        expect(projects.value?.[1]?.submissions).toEqual([])
    })
})
