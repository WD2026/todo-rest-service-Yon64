# TLS Automation for Nginx with Let's Encrypt

This repository provides a reliable, repeatable way to obtain and manage TLS certificates for a self-managed VM using Docker, Nginx, and Certbot.

## Problem 1: Automated Certificate Acquisition

### Approach
We use a **Dockerized Certbot** setup to handle the ACME protocol (Let's Encrypt). This ensures that the environment is consistent regardless of the host OS and minimizes manual configuration. 

> [!NOTE]
> The automation script `init-letsencrypt.sh` is designed to handle the "chicken-and-egg" problem: Nginx cannot start without certificates, but Certbot cannot get certificates without a running web server (for the HTTP-01 challenge).

### Prerequisites
1. **Docker and Docker Compose** installed on the VM.
2. **Public Domain Name** (e.g., `lab068.kasetsart.university`) pointing to the VM's public IP.
3. **Ports 80 and 443 open** in the VM's firewall.

### Installation & Usage
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/tls-automation.git
   cd tls-automation
   ```
2. **Configure details**: Edit `init-letsencrypt.sh` and set the `domains` array and `email`.
3. **Run the bootstrap script**:
   ```bash
   chmod +x init-letsencrypt.sh
   ./init-letsencrypt.sh
   ```

### Troubleshooting
- **Command Not Found**: The script automatically detects if you have `docker compose` (modern V2) or `docker-compose` (legacy V1).
- **Port 80/443 Conflict**: Ensure no other web server is running. Use `docker stop nginx` if your other project is active on port 80.
- **EE key too small**: The script uses **2048-bit RSA keys** to comply with modern security standards.

## Problem 2: Nginx HTTPS Configuration

The Nginx configuration in `data/nginx/app.conf` is tuned for maximum security, aiming for an **"A" Grade** on SSL Labs.

### Security Layout:
- **HSTS (HTTP Strict Transport Security)**: Forces browsers to use HTTPS for the next 2 years.
- **Modern TLS**: Only TLS 1.2 and 1.3 are enabled.
- **OCSP Stapling**: Speeds up certificate validation by providing the status directly from the server.
- **Automatic Redirection**: Port 80 traffic is instantly upgraded to Port 443.

## How to Test
After running the script, visit:
`https://www.ssllabs.com/ssltest/analyze.html?d=lab068.kasetsart.university`

## Automatic Renewal
- **Certbot Sidecar**: The `tls-certbot` container checks for renewal every 12 hours.
- **Nginx Reload**: The `tls-nginx` container runs a background loop to reload its configuration every 6 hours to pick up renewed certificates without downtime.
