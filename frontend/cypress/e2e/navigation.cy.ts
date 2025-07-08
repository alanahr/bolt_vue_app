describe('Navigation and Routing', () => {
  it('should navigate between pages correctly', () => {
    cy.visit('/')
    
    // Should redirect to positions by default
    cy.url().should('include', '/positions')
    cy.contains('h1', 'Positions').should('be.visible')
    
    // Navigate to entities
    cy.get('.navbar-nav').contains('Entities').click()
    cy.url().should('include', '/entities')
    cy.contains('h2', 'Entities').should('be.visible')
    
    // Navigate back to positions
    cy.get('.navbar-nav').contains('Positions').click()
    cy.url().should('include', '/positions')
    cy.contains('h1', 'Positions').should('be.visible')
    
    // Test brand link
    cy.get('.navbar-brand').click()
    cy.url().should('include', '/positions')
  })

  it('should handle 404 routes gracefully', () => {
    cy.visit('/nonexistent-route', { failOnStatusCode: false })
    // The app should still load, just show the default route
    cy.get('body').should('be.visible')
  })
})