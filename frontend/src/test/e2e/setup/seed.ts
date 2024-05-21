import { faculty, course } from './data.ts';
import { client } from '@/config/axios.ts';

export const seed = async () => {
    // log in as normal users to add 2 users to the database
    await client.post('/api/auth/test-user/student/');
    await client.post('/api/auth/cas/logout/');
    await client.post('/api/auth/test-user/multi/');
    await client.post('/api/auth/cas/logout/');

    // log in as an admin user to insert our test data into the database
    await client.post('/api/auth/test-user/admin/');

    // add test data
    await client.post('/api/faculties/', faculty);
    await client.post('/api/courses/', course);

    // logout for cleanup
   await  client.post('/api/auth/cas/logout/');
}