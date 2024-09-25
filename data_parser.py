import re
import os
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def extract_data(details):
    if not details:
        return {}

    personal_details = details.get("personal_details", {}) or {}
    general_details = details.get("general_details", {}) or {}
    field_id = details.get("id", "")

    def get_phone_number():
        phone = personal_details.get("telekommunikation", {}).get("telefon", "")
        if phone:
            formatted_phone = f"{phone.get('internationaleVorwahl', '')} {phone.get('nationaleVorwahl', '')} {phone.get('rufnummer', '')}"
            return formatted_phone
        return ""

    def get_languages():
        languages = general_details.get("sprachkenntnisse", {}) or {}
        return ", ".join(
            [f"{level}: {', '.join(langs)}" for level, langs in languages.items()]
        )

    def get_education():
        edu_data = []
        for edu in general_details.get("bildung", []):
            bis = edu.get("bis", None)
            year = bis.split("-")[0] if bis else ""

            if edu.get("beschreibung", "") and edu.get("berufsbezeichnung", ""):
                edu_data.append(
                    f'{edu.get("beschreibung", "")} {edu.get("berufsbezeichnung", "")} {year}'.strip()
                )

        return ", ".join(edu_data)

    def get_experience():
        yoe = general_details.get("erfahrung", {}).get("gesamterfahrung", "")
        if not yoe:
            return ""
        years = re.search(r"P(\d+)Y", yoe)
        years = str(int(years.group(1)) - 1) if years else "0"
        months = re.search(r"P\d+Y(\d+)M", yoe)
        months = str(int(months.group(1)) - 1) if months else "0"
        days = re.search(r"P\d+Y\d+M(\d+)D", yoe)
        days = str(int(days.group(1)) - 1) if days else "0"
        return f"{years} years, {months} months, {days} days"

    def get_street():
        return f"{personal_details.get('adresse', {}).get('strasse', '')} {personal_details.get('adresse', {}).get('hausnummer', '')}"

    return {
        "Field ID": field_id,
        "Job Title": ", ".join(general_details.get("berufe", [])),
        "Years of experience": get_experience(),
        "Education (degrees)": get_education(),
        "Driving Licenses": ", ".join(
            general_details.get("mobilitaet", {}).get("fuehrerscheine", [])
        ),
        "Spoken Languages": get_languages(),
        "Salutation": personal_details.get("anrede", ""),
        "Name": personal_details.get("vorname", ""),
        "Surname": personal_details.get("nachname", ""),
        "Age": personal_details.get("alter", ""),
        "Email": personal_details.get("telekommunikation", {}).get("email", ""),
        "Phone": get_phone_number(),
        "Street": get_street(),
        "Zipcode": personal_details.get("adresse", {}).get("plz", ""),
        "City": personal_details.get("adresse", {}).get("ort", ""),
        "State": personal_details.get("adresse", {}).get("region", ""),
        "Country": personal_details.get("adresse", {}).get("land", ""),
    }


def extract_and_save_data(json_data, json_filepath, excel_filepath):
    extracted_data = [extract_data(details) for details in json_data]

    if not extracted_data:
        logger.warning("No data to save.")
        return

    df = pd.DataFrame(extracted_data)

    os.makedirs(os.path.dirname(json_filepath), exist_ok=True)
    os.makedirs(os.path.dirname(excel_filepath), exist_ok=True)

    df.to_json(json_filepath, indent=4)
    logger.info(f"Data saved to {json_filepath}")

    df.to_excel(excel_filepath, index=False)
    logger.info(f"Data saved to {excel_filepath}")
