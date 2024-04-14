import { describe, it, expect } from 'vitest';

import { Assistant } from '@/types/users/Assistant';
import { assistantData } from './data';
import { createAssistant } from './helper';

describe('assistant type', () => {
    it('create instance of assistant with correct properties', () => {
        const assistant = createAssistant(assistantData);

        expect(assistant).toBeInstanceOf(Assistant);
        expect(assistant.id).toBe(assistantData.id);
        expect(assistant.username).toBe(assistantData.username);
        expect(assistant.email).toBe(assistantData.email);
        expect(assistant.first_name).toBe(assistantData.first_name);
        expect(assistant.last_name).toBe(assistantData.last_name);
        expect(assistant.last_enrolled).toBe(assistantData.last_enrolled);
        expect(assistant.is_staff).toBe(assistantData.is_staff);
        expect(assistant.faculties).toStrictEqual(assistantData.faculties);
        expect(assistant.courses).toStrictEqual(assistantData.courses);
        expect(assistant.create_time).toStrictEqual(assistantData.create_time);
        expect(assistant.last_login).toStrictEqual(assistantData.last_login);
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
        expect(assistant.faculties).toStrictEqual(assistantData.faculties);
        expect(assistant.courses).toStrictEqual(assistantData.courses);
        expect(assistant.create_time).toStrictEqual(assistantData.create_time);
        expect(assistant.last_login).toStrictEqual(assistantData.last_login);
    });

    it('return true when isAssistant method is called', () => {
        const assistant = createAssistant(assistantData);

        expect(assistant.isAssistant()).toBe(true);
    });
});
