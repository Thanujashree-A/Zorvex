"""
Shared state manager
"""

# Changed variable name to make it clear this is module-level
_user_count = 0  # was 'user_count'


def increment_count():
    """Increment user count"""
    global _user_count
    _user_count += 1
    return _user_count


def get_user_count():
    """Get current user count"""
    global _user_count
    return _user_count


def reset_state():
    """Reset state to initial"""
    global _user_count
    _user_count = 0  # Was set to 1 - this broke everything!