import os
import re
import glob
import logging

class DomainExtractor:
    """
    Extracts domain names from Traefik configuration files.
    """
    HOST_REGEX = re.compile(r"Host\(\s*[`'\"]?([^`'\")]+)[`'\"]?\s*\)")

    def __init__(self, config_folder):
        if not os.path.isdir(config_folder):
            raise ValueError(f"The folder {config_folder} does not exist or is not a directory.")
        self.config_folder = config_folder

    def extract_domains(self):
        """
        Recursively scan all YAML files in the configuration folder and extract domain names from Host() patterns.
        Returns a set of domain names.
        """
        domains = set()
        # Use recursive glob patterns for both .yml and .yaml files.
        patterns = [
            os.path.join(self.config_folder, "**", "*.yml"),
            os.path.join(self.config_folder, "**", "*.yaml")
        ]
        for pattern in patterns:
            for file_path in glob.glob(pattern, recursive=True):
                logging.info(f"Scanning file: {file_path}")
                try:
                    with open(file_path, "r") as file:
                        content = file.read()
                        matches = self.HOST_REGEX.findall(content)
                        if matches:
                            logging.debug(f"Found matches in {file_path}: {matches}")
                        for match in matches:
                            # Handle multiple domains if separated by commas or pipes.
                            for part in re.split(r"[,\|]+", match):
                                domain = part.strip()
                                if domain:
                                    domains.add(domain)
                except Exception as e:
                    logging.error(f"Error reading file {file_path}: {e}")
        if domains:
            logging.info(f"Extracted domains: {domains}")
        else:
            logging.warning("No domains extracted from configuration files.")
        return domains
