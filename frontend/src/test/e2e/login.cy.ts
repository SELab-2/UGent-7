describe('login', () => {
    it('redirects to login page when not logged in', () => {
        cy.visit('/');
        cy.url().should('match', /^.*\/auth\/login$/);
    });
    // Next test is commented out because it loads endlessly when clicking login button
    // it('login button redirects to correct external website', () => {
    //     cy.visit('/');
    //     cy.get('#button').click();
    //     cy.url().should('match', /^$/)
    // })
    it('does not redirect to login page when logged in', () => {

    })
});
