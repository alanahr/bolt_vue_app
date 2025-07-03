describe('Entities CRUD Operations', () => {
  beforeEach(() => {
    cy.visit('/entities')
  })

  it('should display the entities list', () => {
    cy.contains('h2', 'Entities').should('be.visible')
    cy.get('table').should('be.visible')
    cy.get('tbody tr').should('have.length.at.least', 1)
  })

  it('should create a new entity', () => {
    cy.get('.btn-success').contains('Create New Entity').click()
    
    cy.get('#name').type('Cypress Testing')
    cy.get('#entity_type').select('skill')
    cy.get('button[type="submit"]').click()
    
    // Should redirect to entities list
    cy.url().should('include', '/entities')
    cy.contains('Cypress Testing').should('be.visible')
  })

  it('should view an entity', () => {
    cy.get('tbody tr').first().within(() => {
      cy.get('.btn-info').click()
    })
    
    cy.url().should('match', /\/entities\/\d+$/)
    cy.contains('h2', 'View Entity').should('be.visible')
    cy.contains('Type:').should('be.visible')
  })

  it('should edit an entity', () => {
    cy.get('tbody tr').first().within(() => {
      cy.get('.btn-primary').click()
    })
    
    cy.url().should('match', /\/entities\/\d+\/edit$/)
    cy.get('#name').clear().type('Updated Entity Name')
    cy.get('button[type="submit"]').click()
    
    cy.url().should('include', '/entities')
    cy.contains('Updated Entity Name').should('be.visible')
  })

  it('should delete an entity', () => {
    // Create an entity to delete
    cy.get('.btn-success').contains('Create New Entity').click()
    cy.get('#name').type('Entity to Delete')
    cy.get('#entity_type').select('tool')
    cy.get('button[type="submit"]').click()
    
    // View the entity
    cy.contains('tr', 'Entity to Delete').within(() => {
      cy.get('.btn-info').click()
    })
    
    // Delete the entity
    cy.get('.btn-danger').contains('Delete').click()
    
    // Confirm deletion
    cy.on('window:confirm', () => true)
    
    // Should redirect to entities list
    cy.url().should('include', '/entities')
    cy.contains('Entity to Delete').should('not.exist')
  })
})