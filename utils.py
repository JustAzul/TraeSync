import requests

def get_public_ip():
    """
    Retrieve the public IP address from the AWS metadata service,
    or fall back to an external service if not running on EC2.
    """
    try:
        response = requests.get("http://169.254.169.254/latest/meta-data/public-ipv4", timeout=2)
        if response.status_code == 200:
            return response.text.strip()
    except Exception:
        pass
    # Fallback if metadata is not available.
    response = requests.get("https://api.ipify.org")
    return response.text.strip()
