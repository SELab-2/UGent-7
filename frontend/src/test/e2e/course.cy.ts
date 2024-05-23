describe('course', () => {
    context('teacher', () => {
        it('creates course', () => {
            // login as a professor
            cy.request('POST', '/api/auth/test-user/professor/');
            // visit the dashboard
            cy.visit('/');
            // click button to create new coursre
            cy.get('#courseCreate').click();
            // fill in the required values for a new course
            cy.get('#courseName').type('Course');
            cy.get('#courseExcerpt').type('Description');
            cy.get('#courseFaculty').click();
            cy.get('#courseFaculty_1').click();
            // click the save button
            cy.get('#courseSave').click();
            // should redirect to dashboard
            cy.url().should('equal', Cypress.config('baseUrl') + '/');
        });
    });
    context('student', () => {
        it('able to enroll into course', () => {
            // login as a student
            cy.request('POST', '/api/auth/test-user/student/');
            // visit the dashboard
            cy.visit('/');
            // navigate to course selector
            cy.get('#courses').click();
            // enroll into course
            cy.get('#courseEnroll').click();
        });
    });
});
