describe('Positions CRUD Operations', () => {
  beforeEach(() => {
    cy.visit('/')
  })

  it('should display the positions list', () => {
    cy.visit('/positions')
    cy.contains('h1', 'Positions').should('be.visible')
    cy.get('table').should('be.visible')
    cy.get('tbody tr').should('have.length.at.least', 1)
  })

  it('should create a new position', () => {
    cy.createPosition('Test Engineer', 2024, 1, 15, 85000)
    
    // Should redirect to positions list
    cy.url().should('include', '/positions')
    cy.contains('Test Engineer').should('be.visible')
  })

  it('should view a position', () => {
    cy.visit('/positions')
    cy.get('tbody tr').first().within(() => {
      cy.get('.btn-info').click()
    })
    
    cy.url().should('match', /\/positions\/\d+$/)
    cy.get('h1').should('be.visible')
    cy.contains('Position Details').should('be.visible')
    cy.contains('Start Date:').should('be.visible')
  })

  it('should edit a position', () => {
    cy.visit('/positions')
    cy.get('tbody tr').first().within(() => {
      cy.get('.btn-primary').click()
    })
    
    cy.url().should('match', /\/positions\/\d+\/edit$/)
    cy.get('#name').clear().type('Updated Position Title')
    cy.get('button[type="submit"]').click()
    
    cy.url().should('include', '/positions')
    cy.contains('Updated Position Title').should('be.visible')
  })

  it('should delete a position', () => {
    // First create a position to delete
    cy.createPosition('Position to Delete', 2024, 1, 1, 50000)
    
    cy.visit('/positions')
    cy.contains('Position to Delete').should('be.visible')
    
    // Click view to go to position detail page
    cy.contains('tr', 'Position to Delete').within(() => {
      cy.get('.btn-info').click()
    })
    
    // Delete the position
    cy.get('.btn-danger').contains('Delete').click()
    
    // Confirm deletion in the alert
    cy.on('window:confirm', () => true)
    
    // Should redirect to positions list
    cy.url().should('include', '/positions')
    cy.contains('Position to Delete').should('not.exist')
  })
})