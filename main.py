import os
import requests
from autogen import AssistantAgent, UserProxyAgent
from bs4 import BeautifulSoup

llm_config = {
    "config_list": [
        {
            "model": "gpt-4",
            "api_key": api
        }
    ]
}

assistant = AssistantAgent(
    "assistant", 
    system_message="You are a brilliant AI bot who can explain code from Github, manipulate code, create a Github repo, and provide steps to upload files in it. Additionally, you can fetch repository details and explore its contents.",
    llm_config=llm_config
)

user_proxy = UserProxyAgent("user_proxy", code_execution_config=False)

def list_github_folder(repo_owner, repo_name, folder_path, branch='main'):
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{folder_path}?ref={branch}'
    response = requests.get(url)

    if response.status_code == 200:
        contents = response.json()
        for item in contents:
            print(f"Name: {item['name']}")
            print(f"Type: {item['type']}")
            print(f"URL: {item['download_url']}\n")
            
            if item['type'] == 'file':
                file_response = requests.get(item['download_url'])
                if file_response.status_code == 200:
                    if(item['name']=="requirements.txt"):
                        print(f"Contents of {item['name']}:\n")
                        print(file_response.text)
                        
                        messages = [{"role": "system", "content": "You are a brilliant AI bot who can explain code."},
                                    {"role": "user", "content": f"Explain the following code:\n{file_response.text}"}]

                        explanation = assistant.generate_reply(messages)
                        print(f"Explanation: {explanation}\n")
                else:
                    print(f"Failed to download {item['name']}. Status code: {file_response.status_code}\n")
    else:
        print(f"Failed to fetch contents. Status code: {response.status_code}")

repo_owner = 'Sidesh07'
repo_name = 'Server'
folder_path = 'Task-1'
list_github_folder(repo_owner, repo_name, folder_path)

while True:
    question = input("Ask a question or type 'exit' to quit: ")
    if question.lower() == 'exit':
        break

    messages = [{"role": "system", "content": "You are a brilliant AI bot who can answer questions."},
                {"role": "user", "content": question}]
    
    answer = assistant.generate_reply(messages)
    print(f"Answer: {answer}\n")
