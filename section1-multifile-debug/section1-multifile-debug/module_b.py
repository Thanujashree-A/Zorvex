"""
Analytics module
"""

# Removed top-level import to break circular dependency

analytics_log = []


def log_analytics(event_type, user_id):
    """Log analytics event"""
    entry = {
        "event": event_type,
        "user_id": user_id,
        "timestamp": "2026-02-16T14:26:00"
    }
    analytics_log.append(entry)


def get_analytics_summary():
    """Get summary of analytics"""
    # Import here to avoid circular dependency
    from module_a import get_user_list
    
    total_users = len(get_user_list())
    total_events = len(analytics_log)
    
    return {
        "total_users": total_users,
        "total_events": total_events
    }


def clear_analytics():
    """Clear analytics log"""
    global analytics_log
    analytics_log = []