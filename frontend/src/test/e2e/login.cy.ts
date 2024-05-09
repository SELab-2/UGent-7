describe('login', () => {
    it('redirects to login page when not logged in', () => {
        // visit dashboard
        cy.visit('/');
        // should redirect to login page
        cy.url().should('match', /^.*\/auth\/login$/);
    });
    // Next test is commented out because it loads endlessly when clicking login button
    // it('login button redirects to correct external website', () => {
    //     cy.visit('/');
    //     cy.get('#button').click();
    //     cy.url().should('match', /^$/)
    // })
    it('does not redirect to login page when logged in', () => {
        // log in as a test student
        cy.visit('/api/auth/test-user/student/')
        // visit dashboard
        cy.visit('/')
        // should not be redirected to login page
        cy.url().should('not.match', /^.*\/auth\/login$/);
    });
});
