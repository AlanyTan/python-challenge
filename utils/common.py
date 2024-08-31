"""common utility functions"""
import json
from config import config

def challenge_details(challenge_id: str) -> dict:
    """read given problem desc of challenge_id from the challenges dir"""
    with open(f"{config.CHALLENGE_DIR}/{challenge_id}/{config.PROBLEM_FILENAME}",
                  encoding='utf-8') as f:
        challenge_data = json.load(f)
        return challenge_data
