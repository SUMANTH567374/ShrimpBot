def get_tank_disinfection_info(query: str) -> str:
    keywords = ["disinfect", "tank", "chlorine", "clean", "disease", "outbreak"]
    if any(kw in query.lower() for kw in keywords):
        return (
            "After a disease outbreak, apply 100ppm chlorine for 30 minutes. "
            "Ensure tanks are rinsed and dried before refilling."
        )
    return ""


def get_water_quality_info(query: str) -> str:
    keywords = ["ph", "ammonia", "water quality", "water", "parameter"]
    if any(kw in query.lower() for kw in keywords):
        return (
            "Maintain water pH between 7.8 and 8.3. If pH drops below 7.5, use lime to correct. "
            "Keep ammonia levels below 0.5 ppm."
        )
    return ""


def get_feeding_guidelines_info(query: str) -> str:
    keywords = ["feed", "feeding", "survival", "rate", "shrimp"]
    if any(kw in query.lower() for kw in keywords):
        return (
            "Reduce feeding rate by 20% if shrimp survival drops below 70%. "
            "Observe shrimp behavior twice daily for adjustments."
        )
    return ""


def get_temperature_control_info(query: str) -> str:
    keywords = ["temperature", "heat", "cold", "climate"]
    if any(kw in query.lower() for kw in keywords):
        return (
            "Maintain optimal water temperature between 27°C and 30°C. "
            "Gradually adjust if needed, avoiding rapid fluctuations."
        )
    return ""


def get_disease_control_info(query: str) -> str:
    keywords = ["vibrio", "white spot", "disease", "outbreak", "infection"]
    if any(kw in query.lower() for kw in keywords):
        return (
            "Isolate affected tanks immediately. Use probiotics and maintain biosecurity protocols. "
            "Increase aeration during outbreaks."
        )
    return ""
