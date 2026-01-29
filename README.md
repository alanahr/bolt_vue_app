**--------**
**Human Author Note:** 
This is a sample app to test out using Bolt (AI) to generate code with Bolt committing to git directly. I am working on a second version now that I know how to better set up Bolt and processes to get the most out of the AI. Unless otherwise noted like this, all documentation AI-generated.
**--------**

# Vue 3 + TypeScript + FastAPI Fullstack Application

A full-stack CRUD application with Vue 3 frontend and FastAPI backend, featuring TipTap rich text editor, nested details functionality, and comprehensive Docker deployment.

## 🏗️ **Architecture**

```
├── frontend/          # Vue 3 + TypeScript + Vite
│   ├── src/
│   ├── cypress/       # E2E and component tests
│   └── Dockerfile*    # Frontend containers
├── backend/           # FastAPI + Python + MongoDB
│   ├── src/
│   │   ├── models/    # Pydantic models
│   │   ├── routers/   # API endpoints
│   │   ├── services/  # Business logic
│   │   ├── config/    # Database configuration
│   │   └── middleware/# Custom middleware
│   └── Dockerfile*    # Backend containers
├── nginx/             # Reverse proxy configuration
├── ssl/               # SSL certificates
└── docker-compose.yml # Multi-container orchestration
```

## 🚀 **Quick Start**

### **Prerequisites**
- Docker & Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for local development)

### **Setup & Run**
```bash
# Setup environment
npm run docker:setup

# Development (both frontend & backend)
npm run docker:dev

# Production deployment
npm run docker:prod
```

### **Local Development (without Docker)**
```bash
# Install all dependencies
npm run install:all

# Run frontend (terminal 1)
npm run dev:frontend

# Run backend (terminal 2)
cd backend && uvicorn src.main:app --reload
```

## 📡 **API Endpoints**

### **Positions**
- `GET /api/positions` - List all positions
- `GET /api/positions/{id}` - Get position by ID
- `POST /api/positions` - Create new position
- `PUT /api/positions/{id}` - Update position
- `DELETE /api/positions/{id}` - Delete position

### **Entities**
- `GET /api/entities` - List all entities
- `GET /api/entities/{id}` - Get entity by ID
- `POST /api/entities` - Create new entity
- `PUT /api/entities/{id}` - Update entity
- `DELETE /api/entities/{id}` - Delete entity

### **Health Check**
- `GET /health` - Application health status

### **API Documentation**
- `GET /docs` - Interactive Swagger UI
- `GET /redoc` - ReDoc documentation

## 🐳 **Docker Services**

| Service | Port | Description |
|---------|------|-------------|
| `frontend-dev` | 5173 | Vue dev server with hot reload |
| `frontend-prod` | 4173 | Production frontend build |
| `backend-dev` | 8000 | FastAPI dev server with auto-reload |
| `backend-prod` | 8001 | Production FastAPI server |
| `nginx` | 80/443 | Reverse proxy with SSL |
| `mongodb` | 27017 | MongoDB database server |
| `cypress` | - | Testing service (profile: testing) |

## 🔧 **Available Scripts**

### **Development**
```bash
npm run dev              # Full stack development
npm run dev:frontend     # Frontend only
npm run dev:backend      # Backend only (requires Python setup)
npm run docker:dev       # Docker development
```

### **Production**
```bash
npm run build           # Build frontend
npm run docker:prod     # Docker production
```

### **Testing**
```bash
npm run test            # Unit tests
npm run cypress:open    # Cypress interactive
npm run cypress:run     # Cypress headless
npm run docker:test     # Docker testing
```

### **Docker Management**
```bash
npm run docker:setup    # Initial setup
npm run docker:build    # Build all images
npm run docker:clean    # Clean containers & images
```

## 🧪 **Testing**

The application includes comprehensive testing with Cypress for both E2E and component testing.

### **Running Tests Locally**

```bash
# Interactive mode
cd frontend && npm run cypress:open

# Headless mode
cd frontend && npm run cypress:run

# With Docker
npm run docker:test
```

### **CI/CD Pipeline**

Comprehensive GitHub Actions workflows included:

- **Main CI Pipeline**: Build, test, security audit
- **Cypress Dashboard**: Cross-browser testing
- **PR Preview**: Netlify deployment with testing

## 🔒 **Security Features**

- **FastAPI Security**: Built-in request validation and sanitization
- **Pydantic Models**: Strong type validation and data serialization
- **CORS**: Configurable origins
- **Rate Limiting**: API protection
- **TrustedHost Middleware**: Host validation
- **SSL/TLS**: HTTPS support
- **Non-root Containers**: Security best practices

## 🌐 **Access Points**

### **Development**
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### **Production**
- Application: https://localhost (via nginx)
- Backend: http://localhost:8001
- Health Check: https://localhost/health

## 🛠️ **Technology Stack**

### **Frontend**
- Vue 3 with Composition API
- TypeScript
- Vite build tool
- TipTap rich text editor
- Bootstrap 5 UI
- Pinia state management
- Vue Router
- Cypress testing

### **Backend**
- Python 3.11+
- FastAPI framework
- Pydantic for data validation
- Motor (async MongoDB driver)
- Uvicorn ASGI server
- Automatic API documentation
- Type hints throughout

### **Database**
- MongoDB 7.0
- Motor async driver
- Connection pooling
- Automatic reconnection
- Health monitoring

### **DevOps**
- Docker & Docker Compose
- Multi-stage builds
- Nginx reverse proxy
- SSL/TLS termination
- Health checks
- GitHub Actions CI/CD

## 📝 **Environment Variables**

### **Backend (.env)**
```env
NODE_ENV=development
PORT=8000
MONGODB_URI=mongodb://admin:password123@mongodb:27017/vue_crud_db?authSource=admin
MONGODB_DB_NAME=vue_crud_db
CORS_ORIGINS=http://localhost:5173
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100
```

### **Frontend (.env)**
```env
VITE_BACKEND_URI=localhost
VITE_BACKEND_PORT=8000
VITE_BACKEND_WSURI=ws
```

## 🚀 **FastAPI Features**

### **Automatic API Documentation**
- **Swagger UI**: Interactive API documentation at `/docs`
- **ReDoc**: Alternative documentation at `/redoc`
- **OpenAPI Schema**: Automatically generated from Pydantic models

### **Data Validation**
- **Pydantic Models**: Strong typing and validation
- **Request/Response Models**: Automatic serialization/deserialization
- **Error Handling**: Detailed validation error messages

### **Performance**
- **Async/Await**: Non-blocking I/O operations
- **Motor**: Async MongoDB driver
- **Uvicorn**: High-performance ASGI server
- **Connection Pooling**: Efficient database connections

### **Developer Experience**
- **Type Hints**: Full type safety
- **Auto-reload**: Development server with hot reload
- **Dependency Injection**: Clean, testable code architecture
- **Middleware**: Custom rate limiting and security

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 **License**

This project is licensed under the MIT License.
