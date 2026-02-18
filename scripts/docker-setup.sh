#!/bin/bash

# Docker setup script for Vue CRUD fullstack application

set -e

echo "Setting up Docker environment for Vue CRUD fullstack application..."

# Create necessary directories
mkdir -p ssl

# Generate self-signed SSL certificates for development
if [ ! -f ssl/cert.pem ]; then
    echo "Generating self-signed SSL certificates..."
    openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
    echo "SSL certificates generated"
fi

# Create .dockerignore if it doesn't exist
if [ ! -f .dockerignore ]; then
    echo "📝 Creating .dockerignore..."
    cat > .dockerignore << 'EOF'
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
.nyc_output
coverage
.cache
dist
.DS_Store
frontend/cypress/videos
frontend/cypress/screenshots
.github
backend/node_modules
frontend/node_modules
EOF
    echo ".dockerignore created"
fi

# Install dependencies for both frontend and backend
echo "Installing dependencies..."
if [ -d "frontend" ] && [ -f "frontend/package.json" ]; then
    echo "Installing frontend dependencies..."
    cd frontend && npm install && cd ..
fi

if [ -d "backend" ] && [ -f "backend/package.json" ]; then
    echo "Installing backend dependencies..."
    cd backend && npm install && cd ..
fi

echo "Docker setup complete!"
echo ""
echo "Available commands:"
echo "  Development:     npm run docker:dev"
echo "  Production:      npm run docker:prod"
echo "  Testing:         npm run docker:test"
echo "  Full stack dev:  docker-compose up frontend-dev backend-dev"
echo ""
echo "Access points:"
echo "  Frontend Dev:    http://localhost:5173"
echo "  Backend Dev:     http://localhost:8000"
echo "  Production:      https://localhost (with nginx)"
echo "  Backend Prod:    http://localhost:8001"