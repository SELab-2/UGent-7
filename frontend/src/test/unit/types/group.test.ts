/* eslint-disable @typescript-eslint/no-unused-vars */
import { describe, it, expect } from 'vitest';

describe('placeholder', (): void => {
    it('aaaaaaaa', () => {
        
    })
});

// import { describe, it, expect } from 'vitest';

// import { Group } from '@/types/Group';
// import { groupData } from './data';
// import { createGroup } from './helper';

// describe('group type', () => {
//     it('create instance of group with correct properties', () => {
//         const group = createGroup(groupData);

//         expect(group).toBeInstanceOf(Group);
//         expect(group.id).toBe(groupData.id);
//         expect(group.score).toBe(groupData.score);
//         expect(group.project).toBe(groupData.project);
//         expect(group.students).toStrictEqual(groupData.students);
//         expect(group.submissions).toStrictEqual(groupData.submissions);
//     });

//     it('create a minimal group instance from JSON data', () => {
//         const groupJSON = { ...groupData };
//         const group = Group.fromJSON(groupJSON);

//         expect(group).toBeInstanceOf(Group);
//         expect(group.id).toBe(groupData.id);
//         expect(group.score).toBe(groupData.score);
//     });

//     it('create a full group instance from JSON data', () => {
//         const groupJSON = { ...groupData };
//         const group = Group.fromJSONFullObject(groupJSON);

//         expect(group).toBeInstanceOf(Group);
//         expect(group.id).toBe(groupData.id);
//         expect(group.score).toBe(groupData.score);
//         expect(group.project).toBe(groupData.project);
//         expect(group.students).toStrictEqual(groupData.students);
//         expect(group.submissions).toStrictEqual(groupData.submissions);
//     });
// });
