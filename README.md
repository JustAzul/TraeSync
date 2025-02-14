# TraeSync

TraeSync is a lightweight tool that automatically synchronizes your Cloudflare DNS A records with your EC2 instance’s public IP—using your Traefik configuration files as the source of truth. It continuously monitors for changes in your configuration files and your public IP, ensuring your DNS records are always up-to-date.

## Features

- **Automatic Domain Extraction:**  
  Recursively scans your Traefik YAML configuration files to extract domain names based on `Host(...)` rules.

- **Continuous Monitoring:**  
  Uses a file watcher (via the `watchdog` library) and periodic IP checks to trigger DNS syncs when configuration files or the public IP change.

## Prerequisites

- **Python 3.9+**  
- **Docker** (if deploying using the provided Dockerfile)
- A **Cloudflare API Token** with `write:packages`, `read:packages` scopes.
- A directory containing your Traefik configuration files.
