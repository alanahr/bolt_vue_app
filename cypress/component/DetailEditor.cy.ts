import DetailEditor from '../../src/components/DetailEditor.vue'
import { createPinia } from 'pinia'

describe('DetailEditor Component', () => {
  beforeEach(() => {
    const pinia = createPinia()
    
    const mockDetail = {
      id: 1,
      name: 'Test Detail',
      description: {},
      tags: [],
      details: []
    }
    
    cy.mount(DetailEditor, {
      props: {
        detail: mockDetail
      },
      global: {
        plugins: [pinia]
      }
    })
  })

  it('should render the detail editor', () => {
    cy.get('.detail-editor').should('be.visible')
    cy.get('input[placeholder="Detail name"]').should('have.value', 'Test Detail')
  })

  it('should show TipTap editor toolbar', () => {
    cy.get('.btn-toolbar').should('be.visible')
    cy.get('.btn-outline-primary').should('have.length.at.least', 6) // H1-H6 buttons
    cy.get('.btn-outline-secondary').should('have.length.at.least', 4) // Bold, italic, etc.
  })

  it('should allow adding nested details', () => {
    cy.get('.btn-success').contains('+ Nested Detail').click()
    cy.get('.detail-editor').should('have.length', 2)
  })

  it('should show tag management interface', () => {
    cy.get('.btn-outline-secondary').contains('+ Tag').click()
    cy.get('input[placeholder="Search entities..."]').should('be.visible')
  })
})