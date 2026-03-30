import requests

class CloudflareClient:
    """
    A client to interact with the Cloudflare API.
    """
    API_BASE = "https://api.cloudflare.com/client/v4"

    def __init__(self, api_token):
        if not api_token:
            raise ValueError("Cloudflare API token must be provided.")
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

    def get_zones(self):
        """
        Retrieve all zones from Cloudflare.
        """
        zones = []
        page = 1
        per_page = 50
        while True:
            params = {"page": page, "per_page": per_page}
            response = requests.get(f"{self.API_BASE}/zones", headers=self.headers, params=params)
            data = response.json()
            if not data.get("success"):
                raise Exception(f"Error fetching zones: {data}")
            zones.extend(data.get("result", []))
            if len(data.get("result", [])) < per_page:
                break
            page += 1
        return zones

    @staticmethod
    def find_zone_for_domain(domain, zones):
        """
        Find the appropriate Cloudflare zone for a given domain.
        It selects the zone whose name is a suffix of the domain,
        preferring the longest match.
        """
        matching_zone = None
        for zone in zones:
            zone_name = zone["name"]
            if domain.endswith(zone_name):
                if matching_zone is None or len(zone_name) > len(matching_zone["name"]):
                    matching_zone = zone
        return matching_zone

    def get_dns_record(self, zone_id, domain):
        """
        Retrieve the existing A record for the given domain in a zone.
        """
        params = {"type": "A", "name": domain}
        response = requests.get(f"{self.API_BASE}/zones/{zone_id}/dns_records", headers=self.headers, params=params)
        data = response.json()
        if data.get("success"):
            records = data.get("result", [])
            if records:
                return records[0]
        return None

    def update_dns_record(self, zone_id, record_id, domain, ip):
        """
        Update an existing A record with a new IP address.
        """
        payload = {"type": "A", "name": domain, "content": ip, "ttl": 1, "proxied": True}
        response = requests.put(f"{self.API_BASE}/zones/{zone_id}/dns_records/{record_id}",
                                headers=self.headers, json=payload)
        data = response.json()
        return data.get("success", False)

    def create_dns_record(self, zone_id, domain, ip):
        """
        Create a new A record for the given domain with the provided IP address.
        """
        payload = {"type": "A", "name": domain, "content": ip, "ttl": 1, "proxied": True}
        response = requests.post(f"{self.API_BASE}/zones/{zone_id}/dns_records", headers=self.headers, json=payload)
        data = response.json()
        return data.get("success", False)
