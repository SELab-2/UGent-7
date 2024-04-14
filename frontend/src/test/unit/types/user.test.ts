import { describe, it, expect } from 'vitest';

import { type Role, User } from '@/types/users/User';
import { userData } from './data';
import { createUser } from './helper';

describe('user type', () => {
    it('create instance of user with correct properties', () => {
        const user = createUser(userData);

        expect(user).toBeInstanceOf(User);
        expect(user.id).toBe(userData.id);
        expect(user.username).toBe(userData.username);
        expect(user.email).toBe(userData.email);
        expect(user.first_name).toBe(userData.first_name);
        expect(user.last_name).toBe(userData.last_name);
        expect(user.last_enrolled).toBe(userData.last_enrolled);
        expect(user.is_staff).toBe(userData.is_staff);
        expect(user.roles).toStrictEqual(userData.roles);
        expect(user.faculties).toStrictEqual(userData.faculties);
        expect(user.create_time).toStrictEqual(userData.create_time);
        expect(user.last_login).toStrictEqual(userData.last_login);
    });

    it('create a user instance from JSON data', () => {
        const userJSON = { ...userData };
        const user = User.fromJSON(userJSON);

        expect(user).toBeInstanceOf(User);
        expect(user.id).toBe(userData.id);
        expect(user.username).toBe(userData.username);
        expect(user.email).toBe(userData.email);
        expect(user.first_name).toBe(userData.first_name);
        expect(user.last_name).toBe(userData.last_name);
        expect(user.last_enrolled).toBe(userData.last_enrolled);
        expect(user.is_staff).toBe(userData.is_staff);
        expect(user.roles).toStrictEqual(userData.roles);
        expect(user.faculties).toStrictEqual(userData.faculties);
        expect(user.create_time).toStrictEqual(userData.create_time);
        expect(user.last_login).toStrictEqual(userData.last_login);
    });

    it('return use full name when getFullName method is called', () => {
        const user = createUser(userData);

        expect(user.getFullName()).toBe(`${userData.first_name} ${userData.last_name}`);
    });

    it('return false when isStudent method is called', () => {
        const user = createUser(userData);

        expect(user.isStudent()).toBe(false);
    });

    it('return false when isAssistant method is called', () => {
        const user = createUser(userData);

        expect(user.isAssistant()).toBe(false);
    });

    it('return false when isTeacher method is called', () => {
        const user = createUser(userData);

        expect(user.isTeacher()).toBe(false);
    });

    it('return false when isSpecificRole method is called', () => {
        const user = createUser(userData);

        expect(user.isSpecificRole()).toBe(false);
    });

    it('isSpecificRole method', () => {
        const user = createUser(userData);
        const role: Role = 'student';

        expect(user.isSpecificRole()).toBe(false);
        user.roles.push(role);
        expect(user.isSpecificRole()).toBe(true);
    });

    it('hasRoles method', () => {
        const user = createUser(userData);
        const role: Role = 'student';

        expect(user.hasRoles('student')).toBe(false);
        user.roles.push(role);
        expect(user.isSpecificRole()).toBe(true);
    });

    it('hasMultipleRoles method', () => {
        const user = createUser(userData);
        const role1: Role = 'student';
        const role2: Role = 'teacher';

        expect(user.hasRoles('student')).toBe(false);
        user.roles.push(role1);
        expect(user.hasMultipleRoles()).toBe(false);
        user.roles.push(role2);
        expect(user.hasMultipleRoles()).toBe(true);
    });
});
