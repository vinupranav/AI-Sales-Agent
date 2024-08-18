# AI-Sales-Agent

<img src="https://cdn.prod.website-files.com/624ac40503a527cf47af4192/65a8e037a9cf99aabbe9e385_ai-gif-generator-7.gif" style="width: 100%; height: auto;">

## Welcome to the Sales AutoPilot repository! This project leverages multiple AI agents to streamline and optimize sales workflows, from lead generation to customer engagement and sales analytics.

### Overview

This repository contains a lead generation bot that automates the process of collecting potential leads for your business. The bot scrapes specified websites, extracts relevant information, and saves it to HubSpot’s CRM. The contacts are then analyzed by CrewAI to generate personalized messages using Google Gemini, which are then added to HubSpot.

Efficient lead generation and personalised customer engagement are crucial for business success.This lead generation bot can be very helpful to businesses as it addresses critical needs such as efficient lead collection, seamless CRM integration, and personalised customer engagement. This repository includes:

Automated Web Scraping: Collect leads from specified websites without manual effort. The bot navigates web pages, extracts relevant contact information, and compiles it for further processing.

Seamless Integration with HubSpot: Directly export the gathered leads into HubSpot's CRM, ensuring that your sales team has immediate access to up-to-date contact information.

AI-powered Personlaistion: uses AI technologies such as crew ai and google gemini to analyse the lead data and create personalised messages, These personalised messages can substantially boost interaction rates.

### Features

Web Scraping from Specified Sources: The bot scrapes contacts from specified websites, collecting valuable lead information such as names, job titles, email addresses, and company details.

Exporting Leads to HubSpot: The extracted contacts are automatically exported to HubSpot CRM for efficient lead management and tracking.

Personalised Message Generation: Leveraging CrewAI and Google Gemini, the bot generates personalised messages for each contact to enhance engagement and conversion rates.

CSV Export: The contacts are also saved in a CSV file for backup and additional processing.

### Output

The bot will scrape contacts from your specified website and add them to HubSpot. It will then generate personalised messages for each contact. These messages will be saved in HubSpot under the columns “AI agent prompts” and “AI agent prompt response”.

### Troubleshooting

ChromeDriver Issues: Verify that ChromeDriver is installed and its path is correctly set in your system and script.
