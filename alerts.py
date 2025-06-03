def check_alerts(alerts):
    alert_messages = {}
    for alert in alerts:
        subject, body = create_alert_message(alert)
        alert_messages[subject] = body
    
    return alert_messages

def create_alert_message(alert):
    sender = alert["sender_name"]
    event = alert["event"]
    description = alert["description"]
    tags = alert["tags"]
    
    weather_conditions = ""
    
    if tags:
        for tag in tags:
            weather_conditions += tag
    
    alert_subject = f"Alert from {sender} for {event}"
    
    alert_body = f"""
    Hazardous Weather Conditions: {weather_conditions}
    Summary: {description}
    """
    
    return alert_subject, alert_body