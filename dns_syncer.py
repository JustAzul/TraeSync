from utils import get_public_ip
from cloudflare_client import CloudflareClient

class DNSSyncer:
    """
    Synchronizes domains extracted from Traefik configuration with Cloudflare DNS records.
    """
    def __init__(self, cloudflare_client, domain_extractor):
        self.cloudflare_client = cloudflare_client
        self.domain_extractor = domain_extractor

    def sync(self):
        public_ip = get_public_ip()
        print(f"Public IP detected: {public_ip}")

        zones = self.cloudflare_client.get_zones()
        domains = self.domain_extractor.extract_domains()

        if not domains:
            print("No domains found in the configuration files.")
            return

        for domain in domains:
            print(f"\nProcessing domain: {domain}")
            zone = CloudflareClient.find_zone_for_domain(domain, zones)
            if not zone:
                print(f"  No matching Cloudflare zone found for domain: {domain}")
                continue

            zone_id = zone["id"]
            record = self.cloudflare_client.get_dns_record(zone_id, domain)
            if record:
                current_ip = record["content"]
                if current_ip == public_ip:
                    print(f"  Record for {domain} is already up-to-date: {public_ip}")
                else:
                    print(f"  Updating record for {domain}: {current_ip} -> {public_ip}")
                    if self.cloudflare_client.update_dns_record(zone_id, record["id"], domain, public_ip):
                        print("  Update successful.")
                    else:
                        print(f"  Failed to update record for {domain}")
            else:
                print(f"  Creating new DNS record for {domain} with IP {public_ip}")
                if self.cloudflare_client.create_dns_record(zone_id, domain, public_ip):
                    print("  Record created successfully.")
                else:
                    print(f"  Failed to create record for {domain}")
