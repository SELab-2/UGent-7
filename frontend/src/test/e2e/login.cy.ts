// cypress uses mocha and chai assertions by default
// vitest are also based on these assertions, but they modified it a bit
// expect().toBe in vitest would be expect().to.be in cypress
// check out https://www.chaijs.com/api/bdd/ for more in detail explanation for assertions
describe('login page', () => {
    beforeEach(() => {
        // these are e2e tests, they have access to the whole website, not a single component
        // for specific tests, we want to go to a specific parts of the website though
        // we use cy.visit for this, with input an absolute or relative url with https://localhost as current baseUrl
        cy.visit('/auth/login')
    })

    it('routes to course when button clicked', () => {
        // we can check for elements in a web page using a selector or the contents of the element you're searching for
        cy.contains('UGent login') // .click()

        // then you can check whether the new url is correct
        // currently it seems to take too long to load, though
        // cy.url().should("include", "https://login.microsoft.com/")
    })

    it('routes to dashboard when pressing dashboard button', () => {
        cy.contains('Dashboard').click()
        cy.url()
            // we check whether it ends with "/"
            .should('match', /\/$/)
            // we check whether we're not still on the login page
            .should('not.include', '/auth/login')
    })
})
