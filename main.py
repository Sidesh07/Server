import os
import requests
from autogen import AssistantAgent, UserProxyAgent
from bs4 import BeautifulSoup

# LLM Configuration
llm_config = {
    "config_list": [
        {
            "model": "gpt-4",
            "api_key": api
        }
    ]
}

# Initialize Git Assistant Agent (Git bot)
Git = AssistantAgent(
    "Git",
    system_message="You are a brilliant AI bot who can explain code from Github and do the manipulation in the code. You can also create a Github repo and provide steps to upload files in it. And also help the user to create a docker file for the code in the Github repo. Additionally, you can fetch repository details and explore its contents.",
    llm_config=llm_config,
    human_input_mode="ALWAYS"
)

# Initialize Helper User Proxy Agent
Helper = UserProxyAgent("Helper")

# Function to access and read website content
def fetch_website_code(url):
    try:
        # Send a GET request to fetch the HTML content of the website
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Return the raw HTML or extract specific parts (e.g., code, text)
        return soup.prettify()  # You can customize this to extract specific elements
    except requests.exceptions.RequestException as e:
        return f"Error fetching website: {e}"

# Function to fetch GitHub repository details
def fetch_github_repo_details(url):
    try:
        # GitHub API URL for fetching repository details
        repo_api_url = url.replace("github.com", "api.github.com/repos")
        response = requests.get(repo_api_url)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        
        # Parse the JSON response
        repo_data = response.json()
        
        # Extract relevant details (e.g., repo name, description, stars, forks)
        repo_details = {
            "name": repo_data.get("name", "N/A"),
            "description": repo_data.get("description", "No description available."),
            "stars": repo_data.get("stargazers_count", 0),
            "forks": repo_data.get("forks_count", 0),
            "language": repo_data.get("language", "N/A"),
            "url": repo_data.get("html_url", "N/A")
        }
        
        return repo_details
    except requests.exceptions.RequestException as e:
        return f"Error fetching GitHub repository details: {e}"

# Function to handle user input and process the URL or command
def handle_user_input():
    user_input = input("Please enter a URL or command: ").strip()
    
    if "github.com" in user_input:  # Check if the URL is a GitHub link
        print("Fetching GitHub repository content...")
        # Fetch the GitHub repository details
        repo_details = fetch_github_repo_details(user_input)
        
        # Display the repository details
        if isinstance(repo_details, dict):
            print(f"Repository Name: {repo_details['name']}")
            print(f"Description: {repo_details['description']}")
            print(f"Stars: {repo_details['stars']}")
            print(f"Forks: {repo_details['forks']}")
            print(f"Language: {repo_details['language']}")
            print(f"URL: {repo_details['url']}")
        
        # Debugging: Print available methods for Git bot
        print("\nChecking available methods for Git bot...")
        print(dir(Git))  # This will print all available methods and attributes of the Git bot
        
        # Assuming the method to interact with the Git bot is 'ask' or 'respond', 
        # replace the following line with the correct method once identified
        Git_response = Git.ask(f"Fetch the content of the repository at {user_input}")  # Example method
        print(Git_response)
    else:
        print("Executing command...")
        # Pass the command to the Helper agent (or perform some other action)
        response = Helper.respond(user_input)
        print(response)

# Call the function to handle user input
handle_user_input()
