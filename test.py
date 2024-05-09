#%%
import os
import re
import fitz
import json
import datetime
import openai
import pytesseract
from PIL import Image
import csv

# Set the API key for OpenAI
openai.api_key = "YOUR_API_KEY"

# Configure the Tesseract executable path (adjust if necessary)
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

# Define the directory path for PDFs
directory_path = "./AI_CV_brigad_sales/to_shortlist_according_to_stephane_before_ai_analysis/"

# Define the must-have criteria
musthave = [
    {
        "value": "7 years of experience in sales",
        "weight": 7,
        "years": 7,
        "type": "calculation"
    }
]

# Initialize token usage
token_usage_details = {
    "gpt35": {"input": 0, "output": 0},
    "gpt4": {"input": 0, "output": 0}
}

token_usage = {"prompt_tokens": 0, "completion_tokens": 0}
results = []


def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()

    if len(text) > 100:
        return text
    else:
        images = []
        for page in doc:
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)

        extracted_text = ""
        for image in images:
            extracted_text += pytesseract.image_to_string(image, lang="eng")

        return extracted_text


def handle_step(prompt, criterion=None, model="gpt-3.5-turbo"):
    global token_usage, token_usage_details
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "tu es un assistant qui m'aide à évaluer un CV"},
            {"role": "user", "content": prompt},
        ]
    )
    content = response.choices[0].message.content

    if criterion and criterion.get("type") in ["calculation", "export"]:
        token_usage_details["gpt4"]["input"] += response.usage.prompt_tokens
        token_usage_details["gpt4"]["output"] += response.usage.completion_tokens
    else:
        token_usage_details["gpt35"]["input"] += response.usage.prompt_tokens
        token_usage_details["gpt35"]["output"] += response.usage.completion_tokens

    token_usage["prompt_tokens"] += response.usage.prompt_tokens
    token_usage["completion_tokens"] += response.usage.completion_tokens
    return content


def process_cvs():
    global token_usage, token_usage_details
    cvs = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith(".pdf")]

    for cv_path in cvs:
        cv_filename = os.path.basename(cv_path)
        main(cv_path, cv_filename)

    keys = list(results[0].keys())
    with open("b_output_20240408.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)


def main(cv_path, cv_filename):
    global token_usage, token_usage_details
    cv_text = extract_text_from_pdf(cv_path)

    identity_prompt = f"""
    Consigne : extrait les informations suivantes d'un CV que je vais te fournir.
    Voici le CV à analyser: {cv_text}.
    Identifie les informations personnelles du candidat (ne renvoie que ces éléments comme suit):
    - nom et prénom
    - email
    - téléphone
    - localisation
    """
    identity = handle_step(identity_prompt)
    anonymization_prompt = f"""
    Consigne : anonymise le CV en supprimant les informations personnelles.
    Voici le CV à anonymiser: {cv_text}.
    Supprime les informations suivantes (et conserve bien tout le reste):
    - nom et prénom
    - email
    - téléphone
    - nationalité
    - genre
    - âge ou date de naissance
    - références faites à d'autres personnes (y compris leur nom, prénom, poste, entreprise, téléphone et mail)
    """
    cv_anonymized = handle_step(anonymization_prompt)

    criteria = []
    today = datetime.datetime.today().strftime("%Y-%m-%d")

    for must_have in musthave:
        criteria_prompt = ""
        if must_have["type"] == "search":
            criteria_prompt = f"""
            Consigne : recherche le critère suivant dans le CV anonymisé.
            Voici le CV à analyser: {cv_anonymized}.
            Voici le score maximal à attribuer: {must_have["weight"]}
            Voici les étapes à suivre:
            -Recherche le critère suivant : {must_have["value"]}
            -Si le candidat valide le critère à évaluer, mets lui la note de {must_have["weight"]}, 0 sinon.
            """
        elif must_have["type"] == "calculation":
            criteria_prompt = f"""
            Consigne : calcule la durée d'expérience en lien avec le critère suivant.
            Voici le CV à analyser: {cv_anonymized}.
            Calcule la durée d'expérience pour le critère suivant : {must_have["value"]}
            Voici le score maximal à attribuer: {must_have["weight"]}
            Pour cela, tu suivras les instructions suivantes:
            -liste l'intégralité des expériences du candidat directement liées au critère recherché avec leurs périodes (si deux expériences ont des périodes qui se chevauchent, garde la plus longue des deux ou celle ayant le poste le plus prestigieux)
            -A partir des périodes des expériences concernées par le critère, calcule la durée de chaque expérience sachant que la date du jour est le: {today}
            -Fais la somme des durées calculées pour chaque expérience
            -Attribue une note au candidat: {must_have["weight"]} s'il vérifie le critère. S'il ne vérifie pas le critère mais qu'il dispose de plusieurs expériences pertinentes, attribue lui la note suivante: nombre d'années calculées / {must_have["years"]} * {must_have["weight"]}.
            S'il n'y a rien dans son CV qui matche avec le critère recherché, attribue lui la note de 0.
            """
        elif must_have["type"] == "interpretation":
            criteria_prompt = f"""
            Consigne : interprète les expériences en lien avec le critère suivant.
            Voici le CV à analyser: {cv_anonymized}.
            Interprète les expériences pour le critère suivant : {must_have["value"]}
            Voici le score maximal à attribuer: {must_have["weight"]}
            Pour cela, tu suivras les instructions suivantes:
            -Liste les expériences en lien avec le critère recherché et les missions mentionnées les plus susceptibles d'avoir un lien avec le critère recherché
            -Si le candidat valide le critère à évaluer, mets lui la note de {must_have["weight"]}, 0 sinon.
            """
        elif must_have["type"] == "sector":
            criteria_prompt = f"""
            Consigne : vérifie si le candidat a travaillé dans le secteur suivant: {must_have["value"]}
            Voici le CV à analyser: {cv_anonymized}.
            Voici le score maximal à attribuer: {must_have["weight"]}
            Voici les étapes à suivre:
            -Liste les expériences du candidat en vérifiant qu'elles sont en lien avec le secteur recherché (oui ou non).
            -Si le candidat valide le critère à évaluer, mets lui la note de {must_have["weight"]}, 0 sinon.
            """

        criteria_i = handle_step(criteria_prompt, must_have)
        criteria.append(criteria_i)

    eval_list = ",\n".join(criteria)
    summary_comment_prompt = f"""
    Voici les évaluations: {eval_list}.
    Consigne : fais un commentaire d'évaluation (50 tokens maximum) et un résumé du CV (50 tokens maximum) et renvoie les sous forme de 2 listes à puce.
    """
    summary_comment = handle_step(summary_comment_prompt)
    criteria_keys = ", ".join([criterion["value"] for criterion in musthave])
    step4_prompt_template = f"""
    Consigne: regroupe les informations relatives au candidat dans un format JSON parfaitement formaté (avec des brackets et virgules). Tout le contenu JSON doit être en français.
    Voici les informations relatives à l'identité du candidat: {identity}
    Voici les informations relatives à l'évaluation par critère du candidat: {eval_list}
    Voici le commentaire et le résumé: {summary_comment}
    Tu ne renverras que le JSON au format qui suit (en remplaçant "nom et prénom trouvés", "email trouvé", "téléphone trouvé", "ton commentaire d'évaluation" et "ton résumé du CV" par par ceux fournis précédemment. De même pour les scores, en remplaçant par les valeurs respectives fournies précédemment) :
    {{
        "fullname": "nom et prénom trouvés",
        "email": "email si trouvé",
        "phone": "téléphone si trouvé",
        "comment": "ton commentaire d'évaluation (70 tokens maximum)",
        "summary": "ton résumé du CV (70 tokens maximum)"
    }}
    Tu reprendras les clés {criteria_keys} comme clés du JSON précédent avec les notes attribuées pour chaque critère d'évaluation correspondant.
    Rappel: tu ne renverras que le JSON, c'est à dire tout le contenu de la chaîne de caractère débutant par {{ et terminant par }} exclusivement.
    """
    step4_response = handle_step(step4_prompt_template, "export")
    json_pattern = r"{[\s\S]*}"
    match = re.search(json_pattern, step4_response)
    if match:
        json_string = match.group(0)
        try:
            parsed_response = json.loads(json_string)
            parsed_response["cvFileName"] = cv_filename
            parsed_response["sum input gpt3.5"] = token_usage_details["gpt35"]["input"]
            parsed_response["sum output gpt3.5"] = token_usage_details["gpt35"]["output"]
            parsed_response["sum input gpt4"] = token_usage_details["gpt4"]["input"]
            parsed_response["sum output gpt4"] = token_usage_details["gpt4"]["output"]
            results.append(parsed_response)
            token_usage_details = {
                "gpt35": {"input": 0, "output": 0},
                "gpt4": {"input": 0, "output": 0}
            }
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")

    token_usage["prompt_tokens"] = 0
    token_usage["completion_tokens"] = 0


if __name__ == "__main__":
    process_cvs()
