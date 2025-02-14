import os
import re
import glob

class DomainExtractor:
    """
    Extracts domain names from Traefik configuration files.
    """
    HOST_REGEX = re.compile(r"Host\(\s*`([^`]+)`\s*\)")

    def __init__(self, config_folder):
        if not os.path.isdir(config_folder):
            raise ValueError(f"The folder {config_folder} does not exist or is not a directory.")
        self.config_folder = config_folder

    def extract_domains(self):
        """
        Scan all YAML files in the configuration folder and extract domain names from Host() patterns.
        Returns a set of domain names.
        """
        domains = set()
        pattern = os.path.join(self.config_folder, "*.yml")
        for file_path in glob.glob(pattern):
            with open(file_path, "r") as file:
                content = file.read()
                matches = self.HOST_REGEX.findall(content)
                for match in matches:
                    # Handle multiple domains in one rule (separated by commas or ||)
                    for part in re.split(r"[,\|]+", match):
                        domain = part.strip()
                        if domain:
                            domains.add(domain)
        return domains
