# File: agents/agent_tag_utils.py
import time
import re

def extract_tag_content(response, tag):
    pattern = f"<{tag}>(.*?)</{tag}>"
    match = re.search(pattern, response, re.DOTALL)
    return match.group(1).strip() if match else response.strip()

def extract_thought_process(response):
    return extract_tag_content(response, "agentThinking")

def extract_final_output(response):
    return extract_tag_content(response, "finalOutput")

def extract_time_completed(response):
    return extract_tag_content(response, "timeCompleted")

def extract_time_completed(response):
    """Extract the current time in the specified format."""
    return time.strftime('%Y-%m-%d %H:%M:%S')
