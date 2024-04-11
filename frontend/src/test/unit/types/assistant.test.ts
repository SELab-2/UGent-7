import { describe, it, expect } from 'vitest';

import { Assistant } from "@/types/users/Assistant";

describe('Assistant class', () => {
    const assistantData = {
        id: '1',
        username: 'assistant1',
        email: 'assistant1@example.com',
        first_name: 'John',
        last_name: 'Doe',
        last_enrolled: 2024,
        is_staff: true,
        roles: [],
        faculties: [],
        courses: [],
        create_time: new Date(),
        last_login: null,
    };

    // Test constructor
    it('should create an instance of Assistant with correct properties', () => {
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
            assistantData.last_login
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

    // Test static method fromJSON
    it('should create an Assistant instance from JSON data', () => {
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

    // Test method isAssistant
    it('should return true when isAssistant method is called', () => {
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
            assistantData.last_login
        );

        expect(assistant.isAssistant()).toBe(true);
    });
});