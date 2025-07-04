<template>
  <div class="sidebar bg-light p-3 rounded shadow-sm">
    <h5 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mb-3">
      <span>Quick Navigation</span>
    </h5>
    
    <ul class="nav flex-column">
      <li class="nav-item">
        <router-link class="nav-link" to="/entities">
          <i class="bi bi-person me-2"></i>
          Entities
        </router-link>
      </li>
      <li class="nav-item">
        <router-link class="nav-link" to="/companies">
          <i class="bi bi-briefcase me-2"></i>
          All Jobs
        </router-link>
      </li>
    </ul>
    
    <h5 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-3">
      <span>Actions</span>
    </h5>
    
    <ul class="nav flex-column">
      <li class="nav-item">
        <router-link class="nav-link" to="/entities/new">
          <i class="bi bi-plus-circle me-2"></i>
          Add Entity
        </router-link>
      </li>
      <li class="nav-item">
        <router-link class="nav-link" to="/companies/new">
          <i class="bi bi-plus-circle me-2"></i>
          Add Job
        </router-link>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.sidebar {
  height: 100%;
}

.nav-link {
  color: #495057;
  border-radius: 0.25rem;
  transition: background-color 0.2s ease;
}

.nav-link:hover, .nav-link:focus {
  background-color: #e9ecef;
  color: #007bff;
}

.nav-link.router-link-active {
  color: #007bff;
  background-color: rgba(0, 123, 255, 0.1);
  font-weight: 500;
}

.sidebar-heading {
  font-size: 0.9rem;
  text-transform: uppercase;
  color: #6c757d;
}
</style>