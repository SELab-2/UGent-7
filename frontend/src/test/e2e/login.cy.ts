describe('login', () => {
    it('redirects to login page when not logged in', () => {
        // visit dashboard
        cy.visit('/');
        // should redirect to login page
        cy.url().should('match', /^.*\/auth\/login$/);
    });
    it('does not redirect to login page when logged in', () => {
        // log in as a test student
        cy.visit('/api/auth/test-user/student/');
        // visit dashboard
        cy.visit('/');
        // should not be redirected to login page
        cy.url().should('not.match', /^.*\/auth\/login$/);
        // logout for cleaning up
        cy.get('#logout').click();
    });
    it('redirects to login page after logging out', () => {
        // intercept the retrieval of student info
        cy.intercept('/api/students/*/').as('student');
        // log in as a test student
        cy.visit('/api/auth/test-user/student/');
        // visit dashboard
        cy.visit('/');
        // wait for requests for student info to end
        cy.wait('@student');
        cy.wait('@student');
        cy.wait('@student');
        // logout
        cy.get('#logout').click();
        // should be on login page now
        cy.url().should('match', /^.*\/auth\/login$/);
    });
});
