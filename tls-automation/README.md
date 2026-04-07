# TLS Automation for Nginx with Let's Encrypt

This repository provides a reliable, repeatable way to obtain and manage TLS certificates for a self-managed VM using Docker, Nginx, and Certbot.

## Problem 1: Automated Certificate Acquisition

### Approach
We use a **Dockerized Certbot** setup to handle the ACME protocol (Let's Encrypt). This ensures that the environment is consistent regardless of the host OS and minimizes manual configuration.

### Prerequisites
1. **Docker and Docker Compose** installed on the VM.
2. **Public Domain Name** (e.g., `labXXX.kasetsart.university`) pointing to the VM's public IP.
3. **Ports 80 and 443 open** in the VM's firewall.

### Installation & Usage
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/tls-automation.git
   cd tls-automation
   ```
2. **Configure domains**: Edit `init-letsencrypt.sh` and set the `domains` array and `email`.
3. **Run the bootstrap script**:
   ```bash
   chmod +x init-letsencrypt.sh
   ./init-letsencrypt.sh
   ```
   This script will:
   - Create dummy certificates so Nginx can start.
   - Request real certificates from Let's Encrypt.
   - Replace dummy certificates and reload Nginx.

## Problem 2: Nginx HTTPS Configuration

The Nginx configuration in `data/nginx/app.conf` is tuned for maximum security and performance, aiming for an **"A" Grade** on SSL Labs.

### Security Features:
- **TLS 1.2 and 1.3 only**: Disables older, insecure protocols.
- **Modern Ciphers**: Optimized for security and performance.
- **HSTS (HTTP Strict Transport Security)**: Forces browsers to use HTTPS.
- **OCSP Stapling**: Speeds up certificate validation for clients.
- **Automatic HTTP to HTTPS Redirection**: Ensures all traffic is encrypted.

## How to Test
After running the script, visit:
`https://www.ssllabs.com/ssltest/analyze.html?d=labXXX.kasetsart.university`

## Automatic Renewal
The `docker-compose.yml` includes a renewal loop in the Certbot container that checks for expiration every 12 hours. Nginx is configured to reload its configuration every 6 hours to pick up any renewed certificates without downtime.
