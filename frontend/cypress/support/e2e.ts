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
import './commands.ts'

// Alternatively you can use CommonJS syntax:
// require('./commands')

Cypress.on('uncaught:exception', (err, runnable) => {
  // log uncaught error
  console.error('Uncaught exception:', err.message);

  return !err.message.includes('401');
});

const logout = () => {
    cy.getCookie('csrftoken').then((cookie) => {
        cy.getCookie('sessionid').then((cookie2) => {
            if (cookie && cookie2) {
                cy.request({
                    method: 'POST',
                    url: '/api/auth/cas/logout/',
                    headers: {
                        'Referer': Cypress.config('baseUrl'),
                        'X-CSRFToken': cookie.value,
                    },
                });
            }
        })

    });
}

// before(() => {
//     cy.request('POST', '/api/auth/test-user/student/');
//     logout();
//     cy.request('POST', '/api/auth/test-user/multi/');
//     logout();
//     cy.request('POST', '/api/auth/test-user/admin/');
//     logout();
// })

afterEach(() => {
    logout();
})
