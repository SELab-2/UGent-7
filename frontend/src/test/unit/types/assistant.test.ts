import { describe, it, expect } from 'vitest';

import { Assistant } from '@/types/users/Assistant';
import { assistantData } from './data';

describe('Assistant class', () => {
    it('create instance of assistant with correct properties', () => {
        const assistant = new Assistant(
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

        expect(assistant).toBeInstanceOf(Assistant);
        expect(assistant.id).toBe(assistantData.id);
        expect(assistant.username).toBe(assistantData.username);
        expect(assistant.email).toBe(assistantData.email);
        expect(assistant.first_name).toBe(assistantData.first_name);
        expect(assistant.last_name).toBe(assistantData.last_name);
        expect(assistant.last_enrolled).toBe(assistantData.last_enrolled);
        expect(assistant.is_staff).toBe(assistantData.is_staff);
        expect(assistant.faculties).toBe(assistantData.faculties);
        expect(assistant.courses).toBe(assistantData.courses);
        expect(assistant.create_time).toBe(assistantData.create_time);
        expect(assistant.last_login).toBe(assistantData.last_login);
    });

    it('create an Assistant instance from JSON data', () => {
        const assistantJSON = { ...assistantData };
        const assistant = Assistant.fromJSON(assistantJSON);

        expect(assistant).toBeInstanceOf(Assistant);
        expect(assistant.id).toBe(assistantData.id);
        expect(assistant.username).toBe(assistantData.username);
        expect(assistant.email).toBe(assistantData.email);
        expect(assistant.first_name).toBe(assistantData.first_name);
        expect(assistant.last_name).toBe(assistantData.last_name);
        expect(assistant.last_enrolled).toBe(assistantData.last_enrolled);
        expect(assistant.is_staff).toBe(assistantData.is_staff);
        expect(assistant.faculties).toBe(assistantData.faculties);
        expect(assistant.courses).toBe(assistantData.courses);
        expect(assistant.create_time).toStrictEqual(assistantData.create_time);
        expect(assistant.last_login).toStrictEqual(assistantData.last_login);
    });

    it('return true when isAssistant method is called', () => {
        const assistant = new Assistant(
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

        expect(assistant.isAssistant()).toBe(true);
    });
});
