import os
import requests
from crewai_tools import BaseTool

class HubspotTool(BaseTool):
    name: str
    description: str
    api_key: str

    def __init__(self, name: str, description: str, api_key: str):
        super().__init__(name=name, description=description, api_key=api_key)  # to call constructor of base class
        self.api_key = api_key
        self.name = name
        self.description = description

    def _run(self, action, *args, **kwargs):
        """
        Perform an action using the api based on given action and argument.
        
        - action (str): The action to perform.
        - args (tuple): Positional arguments specific to the action.
        - kwargs (dict): Keyword arguments specific to the action.

        Returns:
        - dict: Result of action performed.
        """

        config = kwargs.pop('config', None)

        # this method is required by BaseTool
        if action == 'add_lead':
            return self.add_lead(*args, config=config, **kwargs)
        else:
            raise ValueError(f"Unsupported action: {action}")

    # def add_lead(self, lead_data, config=None):
    #     url = "https://api.hubapi.com/crm/v3/objects/contacts"
    #     headers = {
    #         "Content-Type": "application/json",
    #         "Authorization": f"Bearer {self.api_key}"
    #     }
    #     response = requests.post(url, json=lead_data, headers=headers)
    #     if response.status_code == 201:
    #         return response.json()
    #     else:
    #         response.raise_for_status()
