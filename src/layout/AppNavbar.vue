<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/">
        <i class="bi bi-briefcase me-2"></i>
        Employment History
      </router-link>
      
      <button 
        class="navbar-toggler" 
        type="button" 
        data-bs-toggle="collapse" 
        data-bs-target="#navbarContent"
        aria-controls="navbarContent" 
        aria-expanded="false" 
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      
      <div class="collapse navbar-collapse" id="navbarContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link" to="/" active-class="active" exact>
              Home
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/entities" active-class="active">
              Entities
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/companies" active-class="active">
              Jobs
            </router-link>
          </li>
        </ul>
        
        <div class="d-flex">
          <div class="dropdown">
            <button 
              class="btn btn-outline-light dropdown-toggle" 
              type="button" 
              id="createDropdown" 
              data-bs-toggle="dropdown" 
              aria-expanded="false"
            >
              <i class="bi bi-plus-circle me-1"></i> Create New
            </button>
            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="createDropdown">
              <li>
                <router-link class="dropdown-item" to="/entities/new">
                  <i class="bi bi-building me-2"></i> Entity
                </router-link>
              </li>
              <li>
                <router-link class="dropdown-item" to="/companies/new">
                  <i class="bi bi-briefcase me-2"></i> Job
                </router-link>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>