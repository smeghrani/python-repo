import os
from configparser import ConfigParser
import requests
import base64
from src.config import CONFIG_PATH, JIRA_API_TOKEN


class JiraClient:
    def __init__(self):
        """
        Initialize JiraClient with configuration and authentication details.
        """
        self.config = ConfigParser()
        self.config.read(os.path.join(CONFIG_PATH, "config.ini"))
        self.jira_api_token = JIRA_API_TOKEN
        self.jira_base_url = self.config["Jira"]["JIRA_BASE_URL"]
        self.jira_username = self.config["Jira"]["JIRA_USERNAME"]

        # Basic authentication encoding
        self.auth_str = f"{self.jira_username}:{self.jira_api_token}"
        self.auth_header = {
            "Authorization": f"Basic {self._encode_auth()}",
            "Content-Type": "application/json"
        }

    def _encode_auth(self):
        """
        Encode Jira credentials in Base64 for HTTP headers.
        """
        auth_bytes = self.auth_str.encode("ascii")
        return base64.b64encode(auth_bytes).decode("ascii")

    def get_tickets(self, project_key: str):
        """
        Fetch a list of tickets from a Jira project.
        :param project_key: The key of the Jira project (e.g., "TEST").
        :return: JSON response with the list of issues.
        """
        url = f"{self.jira_base_url}/rest/api/3/search"
        jql = f"project = {project_key}"
        params = {"jql": jql}

        response = requests.get(url, headers=self.auth_header, params=params)
        response.raise_for_status()  # Raises an exception for bad HTTP status codes
        return response.json()

    def get_issue(self, ticket_id: str):
        """
        Fetch details of a single Jira ticket.
        :param ticket_id: The ID or key of the Jira ticket (e.g., "TEST-1").
        :return: JSON response with ticket details.
        """
        url = f"{self.jira_base_url}/rest/api/3/issue/{ticket_id}"

        response = requests.get(url, headers=self.auth_header)
        response.raise_for_status()  # Raises an exception for bad HTTP status codes
        return response.json()