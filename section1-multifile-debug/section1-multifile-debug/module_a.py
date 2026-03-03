"""
User management module
"""

# Removed circular import - will import inside function instead
# Also fixed: was importing variable, now imports functions
from state import increment_count


users = []


def add_user():
    """Add a new user"""
    increment_count()  # This actually works now
    
    user_id = len(users) + 1
    users.append(f"User_{user_id}")
    
    # Import here to avoid circular dependency
    from module_b import log_analytics
    log_analytics("user_added", user_id)
    
    return user_id


def get_user_list():
    """Get list of all users"""
    return users


def remove_user(user_id):
    """Remove a user"""
    if user_id <= len(users):
        users.pop(user_id - 1)


def get_user_details(user_id):
    """Get details for a specific user"""
    if 1 <= user_id <= len(users):
        return {"id": user_id, "name": users[user_id-1]}
    return None