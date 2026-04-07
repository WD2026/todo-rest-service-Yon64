# Best Practices for TLS Certificate Management

Managing TLS certificates is a critical aspect of infrastructure security. This document outlines "best practices" for storing, renewing, and maintaining certificates on self-managed VMs.

---

## 1. Key & Certificate Storage

> [!IMPORTANT]
> **Never commit your private keys to Git.** Public certificates can be shared, but private keys (`privkey.pem`) must remain strictly protected on the server.

### Secure Filesystem Permissions
On the server, always enforce strict permissions:
| File Type | Recommended Permission | Why? |
| :--- | :--- | :--- |
| **Private Keys** | `chmod 600` | Only the root/owner can read/write. |
| **Certificates** | `chmod 644` | Everyone can read for validation, but only owner can write. |

### Storage in External Volumes
As per the reproducible design, certificates should be stored in an **external Docker volume** (e.g., `/srv/docker/certs` or `./data/certbot/conf`).
- **Isolation**: Keeps security credentials separate from the application container.
- **Persistence**: Certificates survive even if the Nginx container is deleted or rebuilt.
- **Portability**: Makes it easier to backup or migrate the credentials to another VM.

---

## 2. Renewal Management

> [!TIP]
> **Automate first, monitor second.** Let's Encrypt certificates expire every 90 days. Manual renewal is prone to human error and downtime.

### Automated Logic
- **Sidecar Containers**: Use a sidecar Certbot container (like our `tls-certbot`) that runs `certbot renew` in a loop (every 12 hours).
- **Reload Signal**: After a successful renewal, the web server (Nginx) **must** reload to pick up the new certificate. Our automation uses a background loop in the Nginx container to perform a `nginx -s reload` every 6 hours.

### Monitoring & Alerting
- **Uptime Monitoring**: Use tools like **Uptime Kuma** or **Better Stack** to monitor the HTTPS expiration date and send alerts (Discord/Slack/Email) if the certificate has less than 14 days left.
- **Log Review**: Periodically check your `certbot` container logs to ensure the ACME challenge is not failing due to firewall or DNS changes.

---

## 3. Disaster Recovery & Revocation

- **Backups**: Include your `/etc/letsencrypt` configurations in your server's periodic backups.
- **Revocation**: If a private key is accidentally leaked (e.g., committed to GitHub), immediately revoke it using `certbot revoke` and rotate the keys.
- **HSTS Preloading**: Once your TLS is stable, consider submitting your domain to the [HSTS Preload List](https://hstspreload.org/) for permanent browser-level enforcement.

---
*By following these practices, you ensure that your web services remain secure, compliant, and always available to users without interruption.*
