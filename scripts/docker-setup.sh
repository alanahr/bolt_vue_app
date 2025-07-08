#!/bin/bash

# Docker setup script for Vue CRUD application

set -e

echo "🚀 Setting up Docker environment for Vue CRUD application..."

# Create necessary directories
mkdir -p ssl
mkdir -p mock-backend

# Generate self-signed SSL certificates for development
if [ ! -f ssl/cert.pem ]; then
    echo "📜 Generating self-signed SSL certificates..."
    openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
    echo "✅ SSL certificates generated"
fi

# Create mock backend server
if [ ! -f mock-backend/server.js ]; then
    echo "🔧 Creating mock backend server..."
    cat > mock-backend/server.js << 'EOF'
const http = require('http');
const url = require('url');

const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    
    // Enable CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }
    
    // Mock API responses
    if (parsedUrl.pathname === '/health') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'healthy', timestamp: new Date().toISOString() }));
    } else if (parsedUrl.pathname.startsWith('/api/')) {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ message: 'Mock API response', path: parsedUrl.pathname }));
    } else {
        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Not found' }));
    }
});

const PORT = process.env.PORT || 8000;
server.listen(PORT, '0.0.0.0', () => {
    console.log(`Mock backend server running on port ${PORT}`);
});
EOF

    cat > mock-backend/package.json << 'EOF'
{
  "name": "mock-backend",
  "version": "1.0.0",
  "description": "Mock backend for Vue CRUD app",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  }
}
EOF
    echo "✅ Mock backend created"
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
cypress/videos
cypress/screenshots
.github
EOF
    echo "✅ .dockerignore created"
fi

echo "🎉 Docker setup complete!"
echo ""
echo "Available commands:"
echo "  Development:     docker-compose up frontend-dev"
echo "  Production:      docker-compose -f docker-compose.yml -f docker-compose.prod.yml up"
echo "  Testing:         docker-compose --profile testing up cypress"
echo "  With backend:    docker-compose --profile with-backend up"
echo "  Full stack:      docker-compose --profile with-backend up frontend-dev backend"
echo ""
echo "Access points:"
echo "  Development:     http://localhost:5173"
echo "  Production:      https://localhost (with nginx)"
echo "  Mock Backend:    http://localhost:8000"