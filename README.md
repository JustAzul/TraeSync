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
- A **Cloudflare API Token** with `write:packages` and `read:packages` scopes.
- A directory containing your Traefik configuration files.

## Docker Image on GitHub Container Registry (GHCR)

The TraeSync Docker image is published on GitHub Container Registry under the repository `ghcr.io/justazul/traesync`. This image is automatically built and versioned with each release.

### Pulling the Image

- **Latest Version:**  
  To pull the latest image, run:

  ```bash
  docker pull ghcr.io/justazul/traesync:latest
  ```

- **Specific Version:**  
  To pull a specific version (e.g., v1.0.0), run:

  ```bash
  docker pull ghcr.io/justazul/traesync:1.0.0
  ```

### Running the Container

You can run TraeSync using the Docker image with a command like the following. Ensure you provide your Cloudflare API token and mount your Traefik configuration directory:

```bash
docker run -d --name traesync \
  -e CLOUDFLARE_API_TOKEN=your_cloudflare_api_token_here \
  -v /path/to/your/traefik/config:/app/config:ro \
  ghcr.io/justazul/traesync:latest \
  python3 main.py --config-folder /app/config --check-interval 60
```

### Using Docker Compose

Alternatively, you can deploy with Docker Compose. Here’s an example `docker-compose.yml` snippet that uses the GHCR image:

```yaml
version: '3.8'

services:
  traesync:
    image: ghcr.io/justazul/traesync:latest
    container_name: traesync
    env_file:
      - .env
    volumes:
      - /path/to/your/traefik/config:/app/config:ro
    command: ["python3", "main.py", "--config-folder", "/app/config", "--check-interval", "60"]
    restart: unless-stopped
```

Run the service with:

```bash
docker compose up -d
```

### Versioning and Tags

- The image is tagged with each release version (e.g., `1.0.0`).
- The `latest` tag always points to the most recent release.
- Using the appropriate tag ensures that your deployment is tied to a specific version of TraeSync.
