# src/hubspot_api.py
from hubspot.crm.contacts import ApiException, SimplePublicObjectInput, PublicObjectSearchRequest
# import hubspot.crm.companies
from hubspot import HubSpot
import requests

hubspot = HubSpot(access_token='')

def get_contacts():
    all_contacts = []
    after = None
    try:
        while True:
            # Fetch contacts
            api_response = hubspot.crm.contacts.basic_api.get_page(
                limit=100,
                after=after,
                properties=['firstname', 'lastname', 'email', 'bio', 'linkedin', 'jobtitle', 'company', 'company_size']
            )
            contacts = api_response.results
            all_contacts.extend(contacts)

            if not api_response.paging or not api_response.paging.next:
                break
            after = api_response.paging.next.after
    except ApiException as e:
        print(f"Exception when calling basic_api->get_page: {e}")
        return []
    return all_contacts

def create_contact(api_client, contact_data):
    try:
        simple_public_object_input_for_create = SimplePublicObjectInput(properties=contact_data["properties"])
        response = api_client.crm.contacts.basic_api.create(simple_public_object_input_for_create=simple_public_object_input_for_create)
        return response.to_dict()
    except ApiException as e:
        print(f"Exception when creating company: {e}")
        return None


def update_contact(contact_id, prompt, response):
    try:
        update_data = {
            "properties": {
                "ai_agent_prompts": prompt,
                "ai_agent_prompt_response": response
            }
        }
        simple_public_object_input_for_update = SimplePublicObjectInput(properties=update_data["properties"])
        response = hubspot.crm.contacts.basic_api.update(contact_id, simple_public_object_input=simple_public_object_input_for_update)
        return response.to_dict()
    except ApiException as e:
        print(f"Exception when updating contact: {e}")
        return None


def get_contact_id_by_name(first_name, last_name):
    try:
        # Define the search request
        search_request = PublicObjectSearchRequest(
            filter_groups=[{
                "filters": [
                    {"value": first_name, "propertyName": "firstname", "operator": "EQ"},
                    {"value": last_name, "propertyName": "lastname", "operator": "EQ"}
                ]
            }],
            limit=1,  # Limit to one result
            properties=["id", "firstname", "lastname"]
        )

        # Perform the search
        search_response = hubspot.crm.contacts.search_api.do_search(search_request)

        # Check if any results were returned
        if search_response.results:
            contact_id = search_response.results[0].id
            return contact_id
        else:
            print("No contact found with the given name.")
            return None

    except ApiException as e:
        print(f"Exception when searching for contact: {e}")
        return None

#####################################

def contacts_to_add(prompt, response):
    contact_data = {
        "properties": {
            "firstname": "test",
            "lastname": "test",
            "email": "example@example.com",
            "ai_agent_prompts": prompt,
            "ai_agent_prompt_response": response
        }
    }
    return contact_data


####################################

# Example usage (for testing purposes, not needed for the automated process)
if __name__ == "__main__":
    hubspot = HubSpot(access_token='pat-na1-556ea00b-fc93-42fb-83c3-150a2cebb9fb')
    prompt = "AI Agent prompt goes here"
    response = "AI agent response goes here"
    try:
        # ## getting contacts from hubspot
        # contacts = hubspot.crm.contacts.get_all()
        # ## retrieve contact ids
        # contact_ids = [contact.id for contact in contacts]

        ## iterate through the contacts and generate personalised messages
        # for contact in contacts:
        #     personalised_email = generate_personalised_email(contact)

        # ## adding contacts
        # contact_data = contacts_to_add(prompt, response)
        # create_contact(hubspot, contact_data)

        ## testing to update contact by giving contact name (returns only 1 exact match)
        contact_id = get_contact_id_by_name(hubspot, "test", "test")
            
        ## update contacts
        update_contact(contact_id, prompt, response)

    except ApiException as e:
        print(f"Exception when calling contacts API: {e}")
    
    
