# Simple in-memory logger for the hackathon
# In production, this would write to a DB
analytics_log = {
    "TAX": 0,
    "PERMIT": 0,
    "SOCIAL": 0,
    "GENERAL": 0
}

def log_query_category(category: str):
    key = category.upper()
    if key in analytics_log:
        analytics_log[key] += 1
    elif "TAX" in key: analytics_log["TAX"] += 1
    elif "PERMIT" in key: analytics_log["PERMIT"] += 1
    elif "SOCIAL" in key: analytics_log["SOCIAL"] += 1
    else: analytics_log["GENERAL"] += 1