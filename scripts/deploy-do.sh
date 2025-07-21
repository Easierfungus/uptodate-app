#!/bin/bash

# DigitalOcean Deployment Script
# This script sets up a Docker-ready droplet

echo "Setting up DigitalOcean droplet for Up to Date app..."

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Setup firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 5000/tcp
sudo ufw --force enable

# Create app directory
mkdir -p ~/uptodate-app

# Setup environment files
echo "Please upload your .env.development or .env.production file to ~/"

# Create docker network
docker network create uptodate-network || true

# Setup automatic container restart
sudo systemctl enable docker

echo "DigitalOcean droplet setup complete!"
echo "Next steps:"
echo "1. Upload your environment file"
echo "2. The GitHub Actions pipeline will handle deployments automatically"