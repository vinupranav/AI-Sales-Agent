from jsonref import requests
from tabulate import tabulate

import pandas as pd


def extract_contact_info(contact):
    return {
        'firstname': contact.properties.get('firstname', ''),
        'lastname': contact.properties.get('lastname', ''),
        'email': contact.properties.get('email', ''),
        'bio': contact.properties.get('bio', ''),
        'linkedin': contact.properties.get('linkedin', ''),
        'job_title': contact.properties.get('jobtitle', ''),
        'company_name': contact.properties.get('company', ''),
        'company_size': contact.properties.get('company_size', '')
    }



def contacts_by_job_title(contacts):
    categorised_contacts = {}
    for contact in contacts:
        contact_info = extract_contact_info(contact)
        job_title = contact_info['job_title']
        if job_title not in categorised_contacts:
            categorised_contacts[job_title] = []
        categorised_contacts[job_title].append(contact_info)
    return categorised_contacts

def format_vertically(categorised_contacts):
    for job_title, contacts in categorised_contacts.items():
        for contact in contacts:
            print("Name:", contact['firstname'])
            print("Last Name:", contact['lastname'])
            print("Email:", contact['email'])
            print("Bio:", contact['bio'])
            print("LinkedIn:", contact['linkedin'])
            print("Job Title:", contact['job_title'])
            print("Company Name:", contact['company_name'])
            print("Company Size:", contact['company_size'])
            print("-" * 40)

# # Example Usage
# contacts = HubspotAPI.get_contacts()
# categorised_contacts = contacts_by_job_title(contacts)
# format_vertically(categorised_contacts)



# def generate_personalised_messages(categorized_contacts, llm):
#     messages = []
#
#     for job_title, contacts in categorized_contacts.items():
#         for contact in contacts:
#             name = contact.get('name', 'N/A')
#             email = contact.get('email', 'N/A')
#             prompt = f"Create a personalized message for a {job_title} named {name}."
#             ai_message = llm.chat(prompt)  # Assuming `llm` is your AI instance
#
#             message = f"""
#             Dear {name},
#
#             {ai_message}
#
#             Looking forward to connecting with you.
#
#             Best Regards,
#             Your Company
#             """
#             messages.append({
#                 'name': name,
#                 'email': email,
#                 'job_title': job_title,
#                 'message': message
#             })
#
#     return messages


# def generate_personalised_messages(categorized_contacts):
#     messages = []
#
#     for job_title, contacts in categorized_contacts.items():
#         for contact in contacts:
#             name = contact.get('name', 'N/A')
#             email = contact.get('email', 'N/A')
#             message = f"""
#             Dear {name},
#
#             As a {job_title}, we thought you might be interested in our latest offerings tailored specifically for your role.
#             Looking forward to connecting with you.
#
#             Best Regards,
#             Your Company
#             """
#             messages.append({
#                 'name': name,
#                 'email': email,
#                 'job_title': job_title,
#                 'message': message
#             })
#
#     return messages


# def print_personalised_messages(messages):
#     df = pd.DataFrame(messages)
#     print(tabulate(df, headers='keys', tablefmt='pretty'))
#
#
#     # Generate and print personalszed messages
#     messages = generate_personalised_messages(categorised_contacts)
#     print_personalised_messages(messages)


