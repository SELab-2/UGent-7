/* eslint-disable @typescript-eslint/no-unused-vars */
import { describe, it, expect } from 'vitest';
import { useAssistant } from '@/composables/services/assistant.service.ts';
import { Assistant } from '@/types/users/Assistant';

const {
    assistants,
    assistant,

    getAssistantByID,
    getAssistantByCourse,
    getAssistants,

    createAssistant,
    deleteAssistant,

    assistantJoinCourse,
    assistantLeaveCourse,
} = useAssistant();

function resetService() {
    assistant.value = null
    assistants.value = null
}

describe('assistant', (): void => {
    it('gets assistant data by id', async () => {
        resetService()

        await getAssistantByID('235');
        expect(assistant.value).not.toBeNull();
        expect(assistant.value?.username).toBe('bsimpson');
        expect(assistant.value?.is_staff).toBe(false);
        expect(assistant.value?.email).toBe('Bart.Simpson@gmail.be');
        expect(assistant.value?.first_name).toBe('Bart');
        expect(assistant.value?.last_name).toBe('Simpson');
        expect(assistant.value?.last_enrolled).toBe(2023);
        expect(assistant.value?.last_login).toBeNull();
        expect(assistant.value?.create_time).toEqual(new Date('July 21, 2024 01:15:00'));
        expect(assistant.value?.courses).toEqual([]);
        expect(assistant.value?.faculties).toEqual([]);
    });

    it('gets assistants data', async () => {
        resetService()

        await getAssistants();
        expect(assistants).not.toBeNull();
        expect(Array.isArray(assistants.value)).toBe(true);
        expect(assistants.value?.length).toBe(2);

        expect(assistants.value?.[0]?.username).toBe('bsimpson');
        expect(assistants.value?.[0]?.is_staff).toBe(false);
        expect(assistants.value?.[0]?.email).toBe('Bart.Simpson@gmail.be');
        expect(assistants.value?.[0]?.first_name).toBe('Bart');
        expect(assistants.value?.[0]?.last_name).toBe('Simpson');
        expect(assistants.value?.[0]?.last_enrolled).toBe(2023);
        expect(assistants.value?.[0]?.last_login).toBeNull();
        expect(assistants.value?.[0]?.create_time).toEqual(new Date('July 21, 2024 01:15:00'));
        expect(assistants.value?.[0]?.courses).toEqual([]);
        expect(assistants.value?.[0]?.faculties).toEqual([]);

        expect(assistants.value?.[1]?.username).toBe('kclijster');
        expect(assistants.value?.[1]?.is_staff).toBe(false);
        expect(assistants.value?.[1]?.email).toBe('Kim.Clijsters@gmail.be');
        expect(assistants.value?.[1]?.first_name).toBe('Kim');
        expect(assistants.value?.[1]?.last_name).toBe('Clijsters');
        expect(assistants.value?.[1]?.last_enrolled).toBe(2023);
        expect(assistants.value?.[0]?.last_login).toBeNull();
        expect(assistants.value?.[0]?.create_time).toEqual(new Date('July 21, 2024 01:15:00'));
        expect(assistants.value?.[1]?.courses).toEqual([]);
        expect(assistants.value?.[1]?.faculties).toEqual([]);
    });

    it('gets assistants data by course', async () => {
        resetService()

        await getAssistantByCourse('1');
        expect(assistants).not.toBeNull();
        expect(Array.isArray(assistants.value)).toBe(true);
        expect(assistants.value?.length).toBe(2);

        expect(assistants.value?.[0]?.username).toBe('bsimpson');
        expect(assistants.value?.[0]?.is_staff).toBe(false);
        expect(assistants.value?.[0]?.email).toBe('Bart.Simpson@gmail.be');
        expect(assistants.value?.[0]?.first_name).toBe('Bart');
        expect(assistants.value?.[0]?.last_name).toBe('Simpson');
        expect(assistants.value?.[0]?.last_enrolled).toBe(2023);
        expect(assistants.value?.[0]?.last_login).toBeNull();
        expect(assistants.value?.[0]?.create_time).toEqual(new Date('July 21, 2024 01:15:00'));
        expect(assistants.value?.[0]?.courses).toEqual([]);
        expect(assistants.value?.[0]?.faculties).toEqual([]);

        expect(assistants.value?.[1]?.username).toBe('kclijster');
        expect(assistants.value?.[1]?.is_staff).toBe(false);
        expect(assistants.value?.[1]?.email).toBe('Kim.Clijsters@gmail.be');
        expect(assistants.value?.[1]?.first_name).toBe('Kim');
        expect(assistants.value?.[1]?.last_name).toBe('Clijsters');
        expect(assistants.value?.[1]?.last_enrolled).toBe(2023);
        expect(assistants.value?.[0]?.last_login).toBeNull();
        expect(assistants.value?.[0]?.create_time).toEqual(new Date('July 21, 2024 01:15:00'));
        expect(assistants.value?.[1]?.courses).toEqual([]);
        expect(assistants.value?.[1]?.faculties).toEqual([]);
    });

    it('create assistant', async () => {
        resetService()

        const exampleAssistant = new Assistant(
            '', // id
            '', // username
            'sample.assistant@UGent.be', // email
            'assistant_first_name', // first_name
            'assistant_last_name', // last name
            2023, // last enrolled
            true, // is_staff
            [], // roles
            [], // faculties
            [], // courses
            new Date(), // create_time
            null, // last_login
        );

        await getAssistants();
        expect(assistants).not.toBeNull();
        expect(Array.isArray(assistants.value)).toBe(true);
        const prevLength = assistants.value?.length ?? 0;

        await createAssistant(exampleAssistant);
        await getAssistants();

        expect(assistants).not.toBeNull();
        expect(Array.isArray(assistants.value)).toBe(true);
        expect(assistants.value?.length).toBe(prevLength + 1);

        // Only check for fields that are sent to the backend
        expect(assistants.value?.[prevLength]?.first_name).toBe('assistant_first_name');
        expect(assistants.value?.[prevLength]?.last_name).toBe('assistant_last_name');
        expect(assistants.value?.[prevLength]?.email).toBe('sample.assistant@UGent.be');
    });
});
