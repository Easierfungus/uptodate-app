# Up to Date App - Development Guidelines

## Project Overview
"Up to Date" is a selfie-based dating application built with Flask, Docker, Supabase, and Redis.

## Development Workflow

### 1. Starting Development
```bash
# Always work from dev branch
git checkout dev
git pull origin dev

# Start Docker development environment
docker-compose up --build
```

### 2. Creating Features
```bash
# Create feature branch
git checkout -b feature/feature-name

# After making changes, run tests
docker-compose exec web pytest tests/

# Run linting
docker-compose exec web flake8 app/
```

### 3. Testing Commands
```bash
# Run all tests
docker-compose exec web pytest tests/ -v

# Run with coverage
docker-compose exec web pytest tests/ --cov=app --cov-report=term-missing

# Linting
docker-compose exec web flake8 app/

# Format code
docker-compose exec web black app/
```

### 4. Monitoring Docker
```bash
# View logs
docker-compose logs -f

# Check container status
docker ps

# Access container shell
docker-compose exec web bash
```

## Environment Setup

### Required Services:
1. **Supabase** (Dev & Prod projects)
   - Create projects at https://supabase.com
   - Run scripts/setup-supabase.sql in SQL editor
   - Get URL and anon key from project settings

2. **Upstash Redis** (Dev & Prod instances)
   - Create databases at https://upstash.com
   - Get Redis URL from database details

3. **DigitalOcean** (Dev & Prod droplets)
   - Create Ubuntu droplets
   - Run scripts/deploy-do.sh on each droplet
   - Add GitHub secrets for deployment

### GitHub Secrets Required:
- `DO_DEV_HOST`: Dev droplet IP
- `DO_PROD_HOST`: Prod droplet IP
- `DO_USERNAME`: SSH username (usually 'root')
- `DO_SSH_KEY`: SSH private key

## API Testing with curl

```bash
# Register user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Create profile (use token from login)
curl -X POST http://localhost:5000/api/profile \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"name":"Test User","bio":"Hello!","age":25,"location":"NYC"}'
```

## Common Issues & Solutions

1. **Docker not refreshing**: Make sure volumes are mounted correctly in docker-compose.yml
2. **Supabase connection errors**: Check SUPABASE_URL and SUPABASE_ANON_KEY in .env
3. **Redis connection errors**: Verify REDIS_URL format is correct
4. **Tests failing**: Run `docker-compose down -v` and rebuild

## Feature Implementation Checklist

When implementing new features:
- [ ] Create feature branch from dev
- [ ] Write tests first (TDD)
- [ ] Implement feature
- [ ] Run all tests
- [ ] Run linting and formatting
- [ ] Update API documentation if needed
- [ ] Create PR to dev branch
- [ ] After dev testing, create PR to main