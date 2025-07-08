describe('Responsive Design', () => {
  const viewports = [
    { device: 'mobile', width: 375, height: 667 },
    { device: 'tablet', width: 768, height: 1024 },
    { device: 'desktop', width: 1280, height: 720 }
  ]

  viewports.forEach(({ device, width, height }) => {
    it(`should work correctly on ${device} (${width}x${height})`, () => {
      cy.viewport(width, height)
      cy.visit('/positions')
      
      // Check that the page loads
      cy.contains('h1', 'Positions').should('be.visible')
      
      // Check that the table is responsive
      cy.get('.table-responsive').should('be.visible')
      
      // Check navbar toggle on mobile
      if (device === 'mobile') {
        cy.get('.navbar-toggler').should('be.visible')
        cy.get('.navbar-collapse').should('not.be.visible')
        
        // Test mobile menu
        cy.get('.navbar-toggler').click()
        cy.get('.navbar-collapse').should('be.visible')
      } else {
        cy.get('.navbar-nav').should('be.visible')
      }
    })
  })
})