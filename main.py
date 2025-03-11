import os
import sys
import argparse
import threading
from flask import Flask
from cloudflare_client import CloudflareClient
from domain_extractor import DomainExtractor
from dns_syncer import DNSSyncer
from watcher import Watcher

# Initialize Flask app
app = Flask(__name__)

@app.route('/health')
def health_check():
    return {'status': 'healthy'}, 200

def run_flask(port):
    app.run(host='0.0.0.0', port=port)

def main():
    parser = argparse.ArgumentParser(
        description="Continuously sync Traefik domains to Cloudflare DNS records."
    )
    parser.add_argument(
        "--config-folder",
        type=str,
        required=True,
        help="Path to the Traefik config folder containing .yml files"
    )
    parser.add_argument(
        "--check-interval",
        type=int,
        default=60,
        help="IP check interval in seconds (default: 60)"
    )
    args = parser.parse_args()

    api_token = os.environ.get("CLOUDFLARE_API_TOKEN")
    if not api_token:
        print("Error: CLOUDFLARE_API_TOKEN environment variable not set")
        sys.exit(1)

    # Start the Flask server in a separate thread only if HEALTH_CHECK_PORT is set
    health_check_port = os.environ.get("HEALTH_CHECK_PORT")
    if health_check_port:
        try:
            port = int(health_check_port)
            flask_thread = threading.Thread(target=run_flask, args=(port,), daemon=True)
            flask_thread.start()
            print(f"Health check endpoint started on port {port}")
        except ValueError:
            print(f"Warning: Invalid HEALTH_CHECK_PORT value: {health_check_port}")

    cloudflare_client = CloudflareClient(api_token)
    domain_extractor = DomainExtractor(args.config_folder)
    dns_syncer = DNSSyncer(cloudflare_client, domain_extractor)

    # Initial sync
    dns_syncer.sync()

    # Start the watcher to monitor file and IP changes continuously.
    watcher = Watcher(args.config_folder, dns_syncer.sync, check_interval=args.check_interval)
    watcher.start()

if __name__ == "__main__":
    main()
