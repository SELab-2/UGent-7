// ***********************************************************
// This example support/e2e.ts is processed and
// loaded automatically before your test files.
//
// This is a great place to put global configuration and
// behavior that modifies Cypress.
//
// You can change the location of this file or turn off
// automatically serving support files with the
// 'supportFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

// Import commands.js using ES2015 syntax:
import '../../../../cypress/support/commands.ts'

// Alternatively you can use CommonJS syntax:
// require('./commands')

import { faculty, course, } from "./data.ts";
import { client } from '@/config/axios.ts';

const post = (url: string, csrfToken: string | undefined, body = {}) => {
    cy.request({
        method: 'POST',
        url: url,
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: body,
    }).then(response => {
        console.log(response);
    })
}

before(async () => {
    await client.post('/api/auth/test-user/admin/')

    cy.visit('/');
    cy.getCookie('csrftoken').then((cookie) => {
        debugger;
        if (cookie) {
            const csrfToken = cookie.value;
            // log in as normal users to add 2 users to the database
            post('/api/auth/test-user/student/', csrfToken);
            post('/api/auth/cas/logout/', csrfToken);
            post('/api/auth/test-user/multi/', csrfToken);
            post('/api/auth/cas/logout/', csrfToken);

            // log in as an admin user to insert our test data into the database
            post('/api/auth/test-user/admin/', csrfToken);

            // add test data
            post('/api/faculties/', csrfToken, faculty);
            post('/api/courses/', csrfToken, course);

            // logout for cleanup
            post('/api/auth/cas/logout/', csrfToken);
        } else {
            console.log('cookie not found');
        }
    });
})