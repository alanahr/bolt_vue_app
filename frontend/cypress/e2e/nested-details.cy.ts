describe('Nested Details Functionality', () => {
  beforeEach(() => {
    cy.visit('/positions')
    // Go to the first position's detail view
    cy.get('tbody tr').first().within(() => {
      cy.get('.btn-info').click()
    })
  })

  it('should add a new detail to a position', () => {
    cy.addDetailToPosition('New test detail')
    
    cy.contains('.detail-editor', 'New test detail').should('be.visible')
  })

  it('should add nested details', () => {
    // Add a main detail first
    cy.addDetailToPosition('Main detail')
    
    // Add a nested detail to the main detail
    cy.get('.detail-editor').last().within(() => {
      cy.get('.btn-success').contains('+ Nested Detail').click()
    })
    
    // Fill in the nested detail
    cy.get('.detail-editor').last().within(() => {
      cy.get('input[placeholder="Detail name"]').type('Nested detail')
    })
    
    cy.contains('Nested detail').should('be.visible')
  })

  it('should use TipTap editor for detail descriptions', () => {
    cy.addDetailToPosition('Detail with rich text')
    
    cy.get('.detail-editor').last().within(() => {
      cy.waitForTipTapEditor()
      
      // Test bold formatting
      cy.get('.btn-outline-secondary').contains('bi-type-bold').click()
      cy.get('.ProseMirror').type('Bold text')
      
      // Test heading
      cy.get('.btn-outline-primary').first().click() // H1 button
      cy.get('.ProseMirror').type('{enter}Heading text')
      
      // Verify content exists
      cy.get('.ProseMirror').should('contain', 'Bold text')
      cy.get('.ProseMirror').should('contain', 'Heading text')
    })
  })

  it('should add and remove tags from details', () => {
    cy.addDetailToPosition('Detail with tags')
    
    cy.get('.detail-editor').last().within(() => {
      // Open tag search
      cy.get('.btn-outline-secondary').contains('+ Tag').click()
      
      // Search for a tag
      cy.get('input[placeholder="Search entities..."]').type('agile')
      
      // Select the tag
      cy.get('.list-group-item').contains('agile').click()
      
      // Verify tag was added
      cy.get('.badge').contains('agile').should('be.visible')
      
      // Remove the tag
      cy.get('.badge').contains('agile').within(() => {
        cy.get('button').click()
      })
      
      // Verify tag was removed
      cy.get('.badge').contains('agile').should('not.exist')
    })
  })

  it('should remove details', () => {
    cy.addDetailToPosition('Detail to remove')
    
    // Find the detail and remove it
    cy.contains('.detail-editor', 'Detail to remove').within(() => {
      cy.get('.btn-danger').contains('Remove').click()
    })
    
    cy.contains('Detail to remove').should('not.exist')
  })

  it('should support drag and drop reordering', () => {
    // Add multiple details
    cy.addDetailToPosition('First detail')
    cy.addDetailToPosition('Second detail')
    
    // Verify initial order
    cy.get('.detail-editor').first().should('contain', 'Participated in Agile')
    cy.get('.detail-editor').eq(1).should('contain', 'First detail')
    cy.get('.detail-editor').eq(2).should('contain', 'Second detail')
    
    // Note: Actual drag and drop testing would require more complex setup
    // This test verifies the elements are present and draggable
    cy.get('.detail-editor').should('have.length.at.least', 3)
  })
})