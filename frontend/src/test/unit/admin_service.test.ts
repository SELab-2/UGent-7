/* eslint-disable @typescript-eslint/no-unused-vars */
import { describe, it, expect, beforeEach } from 'vitest';
import { useAdmin } from '@/composables/services/admins.service.ts';
import { User } from '../../types/users/User';

const {
    admins,
    admin,
    getAdminByID,
    getAdmins,

    createAdmin,
    deleteAdmin,
} = useAdmin();

describe('admin', (): void => {
    it('gets assistant data by id', async () => {
        await getAdminByID('300201547011');
        expect(admin.value).not.toBeNull();
        expect(admin.value?.username).toBe('tverslyp');
        expect(admin.value?.is_staff).toBe(true);
        expect(admin.value?.email).toBe('Tybo.Verslype@UGent.be');
        expect(admin.value?.first_name).toBe('Tybo');
        expect(admin.value?.last_name).toBe('Verslype');
        expect(admin.value?.last_enrolled).toBe(2023);
        expect(admin.value?.last_login).toEqual(new Date('July 23, 2024 01:15:00'));
        expect(admin.value?.create_time).toEqual(new Date('July 21, 2024 01:15:00'));
        expect(admin.value?.faculties).toEqual([]);
    });

    it('gets admins data', async () => {
        await getAdmins();
        expect(admins).not.toBeNull();
        expect(Array.isArray(admins.value)).toBe(true);
        expect(admins.value?.length).toBe(2);

        expect(admins.value?.[0]?.username).toBe('tverslyp');
        expect(admins.value?.[0]?.is_staff).toBe(true);
        expect(admins.value?.[0]?.email).toBe('Tybo.Verslype@UGent.be');
        expect(admins.value?.[0]?.first_name).toBe('Tybo');
        expect(admins.value?.[0]?.last_name).toBe('Verslype');
        expect(admins.value?.[0]?.last_enrolled).toBe(2023);
        expect(admins.value?.[0]?.last_login).toEqual(new Date('July 23, 2024 01:15:00'));
        expect(admins.value?.[0]?.create_time).toEqual(new Date('July 21, 2024 01:15:00'));
        expect(admins.value?.[0]?.faculties).toEqual([]);

        expect(admins.value?.[1]?.username).toBe('simmig');
        expect(admins.value?.[1]?.is_staff).toBe(true);
        expect(admins.value?.[1]?.email).toBe('Simon.Mignolet@UGent.be');
        expect(admins.value?.[1]?.first_name).toBe('Simon');
        expect(admins.value?.[1]?.last_name).toBe('Mignolet');
        expect(admins.value?.[1]?.last_enrolled).toBe(2023);
        expect(admins.value?.[0]?.last_login).toEqual(new Date('July 23, 2024 01:15:00'));
        expect(admins.value?.[0]?.create_time).toEqual(new Date('July 21, 2024 01:15:00'));
        expect(admins.value?.[1]?.faculties).toEqual([]);
    });

    it('create admin', async () => {
        const exampleAdmin = new User(
            '101', // id
            'sample_admin', // username
            'sample.admin@UGent.be', // email
            'Sample', // first_name
            'Admin', // last_name
            2024, // last_enrolled
            true, // is_staff
            ['user'], // roles
            [], // faculties
            new Date('April 2, 2023 01:15:00'), // create_time
            new Date('April 2, 2024 01:15:00'), // last_login
        );

        await getAdmins();
        expect(admins).not.toBeNull();
        expect(Array.isArray(admins.value)).toBe(true);
        const prevLength = admins.value?.length || 0;

        await createAdmin(exampleAdmin);
        await getAdmins()

        expect(admins).not.toBeNull();
        expect(Array.isArray(admins.value)).toBe(true);
        expect(admins.value?.length).toBe(prevLength + 1);

        expect(admins.value?.[prevLength]?.first_name).toBe('Sample');
        expect(admins.value?.[prevLength]?.last_name).toBe('Admin');
        expect(admins.value?.[prevLength]?.email).toBe('sample.admin@UGent.be');
        expect(admins.value?.[prevLength]?.is_staff).toBe(true);
    });
});
