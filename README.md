# Up to Date - Selfie-Based Dating App

A modern dating application built with Flask, Docker, Supabase, and Redis.

## Architecture

- **Backend**: Python Flask
- **Database**: Supabase (PostgreSQL)
- **Cache**: Upstash Redis
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Deployment**: DigitalOcean

## Development Setup

### Prerequisites
- Docker and Docker Compose
- Git
- GitHub CLI (gh)

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/Easierfungus/uptodate-app.git
cd uptodate-app
```

2. Create your `.env.development` file with your Supabase and Upstash credentials:
```bash
cp .env.development .env.development.local
# Edit .env.development.local with your actual credentials
```

3. Start the development environment:
```bash
docker-compose up --build
```

The app will be available at `http://localhost:5000` with hot-reload enabled.

## Working on Features

### 1. Create a new feature branch from dev:
```bash
git checkout dev
git pull origin dev
git checkout -b feature/your-feature-name
```

### 2. Make your changes
The Docker container will automatically reload when you save files.

### 3. Test your changes:
```bash
# Run tests
docker-compose exec web pytest tests/

# Run linting
docker-compose exec web flake8 app/

# Check logs
docker-compose logs -f
```

### 4. Commit and push:
```bash
git add .
git commit -m "Add your feature description"
git push origin feature/your-feature-name
```

### 5. Create a Pull Request:
```bash
gh pr create --base dev --title "Your feature title" --body "Description of changes"
```

## Deployment Pipeline

### Development (dev branch):
- Push to `dev` branch triggers automatic deployment to development environment
- Tests and linting run automatically
- Docker image is built and pushed to GitHub Container Registry
- Deploys to DigitalOcean development droplet

### Production (main branch):
- Create PR from `dev` to `main`
- After merge, automatic deployment to production
- Full test suite runs
- Production Docker image is built
- Deploys to DigitalOcean production droplet

## Environment Variables

### Required for Development:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_ANON_KEY`: Supabase anonymous key
- `REDIS_URL`: Upstash Redis connection string

### GitHub Secrets Required:
- `DO_DEV_HOST`: DigitalOcean dev droplet IP
- `DO_PROD_HOST`: DigitalOcean prod droplet IP
- `DO_USERNAME`: SSH username
- `DO_SSH_KEY`: SSH private key for deployment

## API Endpoints

- `GET /`: Health check
- `POST /api/auth/register`: User registration
- `POST /api/auth/login`: User login
- `POST /api/auth/logout`: User logout
- `GET /api/profile`: Get user profile
- `POST /api/profile`: Create user profile
- `POST /api/profile/selfie`: Upload selfie

## Database Schema

Run the SQL script in `scripts/setup-supabase.sql` in your Supabase project to set up:
- Users table (managed by Supabase Auth)
- Profiles table
- Matches table
- Likes table
- Messages table
- Storage bucket for selfies
- Row Level Security policies

## Project Structure

```
uptodate-app/
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── main.py
│   │   └── profile.py
│   ├── services/
│   │   ├── supabase_service.py
│   │   └── redis_service.py
│   └── models/
├── tests/
├── scripts/
├── .github/workflows/
├── docker-compose.yml
├── docker-compose.prod.yml
├── Dockerfile
├── Dockerfile.dev
└── requirements.txt
```