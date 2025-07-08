/// <reference types="cypress" />

// Custom commands for the Vue CRUD app

declare global {
  namespace Cypress {
    interface Chainable {
      /**
       * Custom command to create a new position
       * @example cy.createPosition('Software Engineer', 2023, 1, 1, 100000)
       */
      createPosition(name: string, startYear: number, startMonth: number, startDay: number, salary?: number): Chainable<Element>
      
      /**
       * Custom command to create a new entity
       * @example cy.createEntity('JavaScript', 'skill')
       */
      createEntity(name: string, entityType: string): Chainable<Element>
      
      /**
       * Custom command to add a detail to a position
       * @example cy.addDetailToPosition('Worked on frontend development')
       */
      addDetailToPosition(detailName: string): Chainable<Element>
      
      /**
       * Custom command to wait for TipTap editor to be ready
       */
      waitForTipTapEditor(): Chainable<Element>
    }
  }
}

Cypress.Commands.add('createPosition', (name: string, startYear: number, startMonth: number, startDay: number, salary?: number) => {
  cy.visit('/positions/new')
  cy.get('#name').type(name)
  cy.get('#start_year').clear().type(startYear.toString())
  cy.get('#start_month').clear().type(startMonth.toString())
  cy.get('#start_day').clear().type(startDay.toString())
  
  if (salary) {
    cy.get('#salary').clear().type(salary.toString())
  }
  
  cy.get('button[type="submit"]').click()
})

Cypress.Commands.add('createEntity', (name: string, entityType: string) => {
  cy.visit('/entities/new')
  cy.get('#name').type(name)
  cy.get('#entity_type').select(entityType)
  cy.get('button[type="submit"]').click()
})

Cypress.Commands.add('addDetailToPosition', (detailName: string) => {
  cy.get('.btn-success').contains('Add Detail').click()
  cy.get('.detail-editor').last().within(() => {
    cy.get('input[placeholder="Detail name"]').type(detailName)
  })
})

Cypress.Commands.add('waitForTipTapEditor', () => {
  cy.get('.ProseMirror').should('be.visible')
  cy.wait(500) // Give editor time to initialize
})