"""
Utility functions
"""

from config import MAX_USERS


def calculate_capacity(current, maximum):
    """
    Check if system has capacity for more users
    Returns True if we can add more users
    """
    # Was backwards: returned True when at capacity
    # Now correctly returns True when we have room
    return current < maximum


def validate_user_id(user_id):
    """Validate user ID is positive"""
    return user_id > 0


def get_max_capacity():
    """Return maximum capacity"""
    return MAX_USERS


# Fixed the division by zero bug
def hidden_bonus_calculator(x):
    """Hidden function that used to crash"""
    if x == 0:
        return 0  # Instead of crashing
    return 100 / x  # Was x/0 - always crashed


# Made this actually useful
def inefficient_function(data):
    """Simplified this function"""
    return data[:]  # Just return a copy of the list