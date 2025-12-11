# Simulated Scraper for stability
CACHED_DATASHEETS = {
    "NE555DR": {"manufacturer": "Texas Instruments", "logo_text": "Ti", "desc": "Precision Timer"},
    "LM7805": {"manufacturer": "Fairchild", "logo_text": "F", "desc": "Voltage Regulator"},
    "ATMEGA328P": {"manufacturer": "Microchip", "logo_text": "M", "desc": "8-bit AVR Microcontroller"}
}

def fetch_datasheet_info(part_number: str):
    clean_part = part_number.upper().strip()
    if clean_part in CACHED_DATASHEETS:
        return CACHED_DATASHEETS[clean_part]
    return {"manufacturer": "Unknown", "logo_text": "Unknown", "desc": "Not Found"}
