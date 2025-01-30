
import logging


logging.basicConfig(filename="log/ai_suspect.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",)


def ai_suspect():
    logging.info("")
    logging.info("*******")
    logging.info(f"TITLE: {i['title']}")

    try:
        description = i['description']
    except KeyError as e:
        description = "None"

    if i['abstract'] == None or len(i['abstract']) <= len(description):
        abstract = i['description']
    else:
        abstract = i['abstract']
    abstract_response = chat_with_model_in_thread_ai(ai_unique_code, ai_unique_code, abstract)
    justification = abstract_response.json()['textResponse']
    logging.info(justification)
    logging.info("*******")
    logging.info("")

    try:
        ai_score = int(abstract_response.json()['textResponse'].partition("%")[0].strip())
        ai_justification = abstract_response.json()['textResponse'].partition("%")[2].strip()
    except:
        ai_score = int(abstract_response.json()['textResponse'].partition(".")[0].strip())
        ai_justification = abstract_response.json()['textResponse'].partition(".")[2].strip()
