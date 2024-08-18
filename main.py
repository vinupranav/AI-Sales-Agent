import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from Tools import HubspotTool
import HubspotAPI
from hubspot_cat import contacts_by_job_title
from Leadconfig import lead_gen_config
from langchain_google_genai import ChatGoogleGenerativeAI
import certifi
from lead_gen import scrape_contacts

os.environ['SSL_CERT_FILE'] = certifi.where()

load_dotenv()

os.environ["GOOGLE_API_KEY"] = ""
os.environ["SERPER_API_KEY"] = ""

serperdev_instance = SerperDevTool()
hubspot_instance = HubspotTool(
    name="Hubspot",
    description="Automating lead scoring based on predefined criteria to prioritize high-quality leads.",
    api_key=os.getenv("HUBSPOT_API_KEY")
)

google_generative_ai = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

analysing_agent = Agent(
    role='Contact Analyser',
    goal='Analyze contact details and generate a detailed prompt for the personalized message generating agent for B2B sales.',
    backstory="Your role is to scrutinize contact information, extract key details, and formulate comprehensive prompts for personalized messages.",
    llm=google_generative_ai,
    config={},
    verbose=True,
    allow_delegation=False,
    max_iter=3,
    timeout=5,
)

message_personalising_agent = Agent(
    role='Message Generator',
    goal='Generate personalized messages for B2B leads based on detailed prompts.',
    backstory="Your role is to craft personalized messages for B2B leads based on detailed prompts.",
    tools=[serperdev_instance],
    llm=google_generative_ai,
    config=lead_gen_config,
    verbose=True,
    allow_delegation=False,
    timeout=5,
    max_iter = 3
)

contact_analysing_task = Task(
    description="Analyze the contact details and generate a detailed prompt for personalized message generation for B2B sales.",
    expected_output="A detailed prompt for the personalized message generating agent for each contact.",
    agent=analysing_agent
)

message_generation_task = Task(
    description="Generate personalized messages based on detailed prompts provided by the Contact Analyzer.",
    expected_output="A personalized message for each contact.",
    agent=message_personalising_agent
)

# takes the dictionary contact and processes it to generarte peronlaised messages based on the contact details
#it also updates contact info using hubspotAPI
def process_contact(contact,user_prompt):
    try:
        if contact is None:# checks if there are any contacts
            raise ValueError("Contact is None")
        # checks if firstname and lastnam if contact is present
        if 'firstname' not in contact or 'lastname' not in contact:
            raise ValueError("Contact data missing required fields")
        #uses the task to analyse the contact details and generate a prompt
        contact_analysing_task.description = f"Analyze the following contact details with this prompt in mind: {user_prompt}. Contact Details: Name: {contact['firstname']}, Last Name: {contact['lastname']}, Job Title: {contact['job_title']}, Company: {contact['company_name']}, Company Size: {contact['company_size']}, Bio: {contact['bio']}, LinkedIn: {contact['linkedin']}."
        crew = Crew(#here we use the agents and tasks needed to complete what we need
            #to process tasks sequentially with a verbosity of 2 for detailed logging
            agents=[analysing_agent],
            tasks=[contact_analysing_task],
            verbose=2,
            process=Process.sequential
        )
        prompt_response = crew.kickoff()# initiates the process of the crew tasks
        contact['prompt'] = prompt_response# here we store the prompts to the contact dictionary
        #checks if the prompt exists in contact and if so sets up a new task description.
        if 'prompt' in contact:
            message_generation_task.description = f"Generate a personalized message based on the following prompt: {contact['prompt']}"
            crew = Crew(
                agents=[message_personalising_agent],
                tasks=[message_generation_task],
                verbose=2,
                process=Process.sequential
            )
            message_response = crew.kickoff()
            contact['message'] = message_response
            #updates the contacts here by retreiving contact id then updating within hubspot
            contact_id = HubspotAPI.get_contact_id_by_name(contact['firstname'], contact['lastname'])
            HubspotAPI.update_contact(contact_id, contact['prompt'], contact['message'])
        return contact
    except Exception as e:
        logging.error(f"Error processing contact {contact.get('email', 'unknown')}: {e}")
        return None


def main(user_prompt):
    try:
        logging.debug("Starting main process...")

        contacts = scrape_contacts()
        logging.debug(f"Contacts fetched: {len(contacts)} contacts found")

        all_contacts = HubspotAPI.get_contacts()
        #logging.debug(f"Contacts fetched: {len(contacts)} contacts found.")
        # here we improve the runtime.

        # here we also equal categorised_contacts to contacts_by_job_title because we want to make categorised contacts a dictionary
        # this is so that there is faster data access so changing the data strucuture to a dictionary from a list is better for runtime.
        #Before categorising the contacts by job title into a dictionary, the contacts variable was a list of individual contact dictionaries.
        categorised_contacts = contacts_by_job_title(all_contacts)
        logging.debug("Contacts categorized successfully.")

        #here we batch process using threadpoolexecutor: helps with effficiency, Uses a loop with ThreadPoolExecutor to handle multiple contacts at once.
        # we also use multithreading : Performs tasks concurrently, reducing wait time for each task, Makes better use of CPU and network resources.
        with ThreadPoolExecutor() as executor:
            futures = []
            for job_title, contacts in categorised_contacts.items():
                for contact in contacts:
                    if contact.get('firstname') and contact.get('lastname'):
                        futures.append(executor.submit(process_contact, contact,user_prompt))
            # here we use as_completed to process data only when its needed,rather than all at once ,this can stop uneccassary computations that can slow down the runtime
            for future in as_completed(futures):
                result = future.result()
                if result:
                    logging.debug(f"Processed contact: {result.get('email', 'unknown')}")

        logging.debug("Main process completed successfully.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()











