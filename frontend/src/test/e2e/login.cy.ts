describe('login', () => {
    it('redirects to login page when not logged in', () => {
        // visit dashboard
        cy.visit('/');
        // should redirect to login page
        cy.url().should('match', /^.*\/auth\/login$/);
    });
    it('does not redirect to login page when logged in', () => {
        // log in as a test student
        cy.request('POST', '/api/auth/test-user/student/');
        // visit dashboard
        cy.visit('/');
        // should not be redirected to login page
        cy.url().should('not.match', /^.*\/auth\/login$/);
    });
    it('redirects to login page after logging out', () => {
        // log in as a test student
        cy.request('POST', '/api/auth/test-user/student/');
        // visit dashboard
        cy.visit('/');
        // logout
        cy.get('#logout').click();
        // should be on login page now
        cy.url().should('match', /^.*\/auth\/login$/);
    });
});
