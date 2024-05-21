import { describe, it, expect } from 'vitest';
import { useAssistant } from '@/composables/services/assistant.service.ts';
import { Assistant } from '@/types/users/Assistant';

const {
    assistants,
    assistant,
    getAssistantByID,
    getAssistantsByCourse,
    getAssistants,
    createAssistant,
    deleteAssistant,
} = useAssistant();

function resetService(): void {
    assistant.value = null;
    assistants.value = null;
}

describe('assistant', (): void => {
    it('gets assistant data by id', async () => {
        resetService();

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
        resetService();

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
        resetService();

        await getAssistantsByCourse('1');
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
        resetService();

        const exampleAssistant = new Assistant(
            'assistant_id', // id
            '', // username
            '', // email
            '', // first_name
            '', // last name
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
        expect(assistants.value?.[prevLength]?.id).toBe('assistant_id');
    });

    it('delete assistant', async () => {
        resetService();

        await getAssistants();
        expect(assistants.value).not.toBeNull();
        expect(Array.isArray(assistants.value)).toBe(true);
        const prevLength = assistants.value?.length ?? 0;

        let assistantId = '0';
        if (assistants.value?.[0]?.id !== undefined && assistants.value?.[0].id !== null) {
            assistantId = assistants.value?.[0]?.id;
        }

        await deleteAssistant(assistantId);
        await getAssistants();

        expect(assistants).not.toBeNull();
        expect(Array.isArray(assistants.value)).toBe(true);
        expect(assistants.value?.length).toBe(prevLength - 1);
        expect(assistants.value?.[0]?.id).not.toBe(assistantId);
    });
});
