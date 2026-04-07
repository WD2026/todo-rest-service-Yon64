# Best Practices for Managing TLS Certificates

Managing TLS certificates is a critical aspect of infrastructure security. This document outlines recommendations for storing, renewing, and maintaining certificates on self-managed VMs or cloud services.

## 1. Where to Store Public and Private Keys?

### Secure Key Storage
- **Private Keys**: These must **NEVER** be committed to a version control system (Git, SVN, etc.). If a private key is leaked, the security of the entire domain is compromised.
- **Filesystem Permissions**: On the server, set strict permissions:
  - Private keys: `chmod 600` (Read/Write for owner only).
  - Public certificates: `chmod 644` (Read for everyone, Write for owner).
- **Secrets Management**: For more complex environments, use a dedicated secrets manager like **HashiCorp Vault**, **AWS Secrets Manager**, or **Azure Key Vault**. These tools provide encryption-at-rest and audit logs of who accessed the keys.
- **Isolation**: Storing certificates in a dedicated Docker volume (e.g., `/srv/docker/certs`) separates them from the application code and host OS.

## 2. How to Manage Renewal?

### Automation is Key
- **Let's Encrypt**: Certbot should be configured to run automatically. In a Docker setup, this can be done via a sidecar container or a looping entrypoint as shown in this project.
- **Monitoring and Alerting**: Do not rely solely on automation. Implement monitoring using tools like **Prometheus** (with `ssl_exporter`), **Uptime Kuma**, or simple scripts that check the expiration date and send alerts (Email, Slack, Discord) when the remaining time is less than 14 days.
- **Test Renewals**: Periodically run a "dry run" (`certbot renew --dry-run`) to ensure the renewal process is still functional and not blocked by firewall or configuration changes.

## 3. Revocation and Rotation

- **Key Rotation**: It is a good practice to rotate your private keys periodically. Let's Encrypt does this automatically every 90 days during renewal by default.
- **Revocation Plan**: If you suspect a private key has been compromised, you must revoke the certificate immediately using `certbot revoke --cert-name domain.com`. This informs browsers that the certificate is no longer trustworthy.

## 4. Backups and Disaster Recovery

- **Configuration Backup**: Regularly back up the `/etc/letsencrypt` configuration and archive directories. This allows you to quickly restore your certificate setup if the VM's disk fails.
- **Separate Volume**: Store certificates on a persistent external volume, not in the container's ephemeral layer. This ensures that even if the container is deleted, the certificates remain.

---

*By following these practices, you ensure that your web services remain secure, compliant, and always available to users without interruption from expired certificates.*
