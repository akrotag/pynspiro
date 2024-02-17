import requests as req
import json

def generate_sentences() -> list:
    """
        Generates 3 motivational sentences from inspirobot.me api
    """
    sess_id = req.get("https://inspirobot.me/api?getSessionID=1").text

    sentences_resp = req.get(f"https://inspirobot.me/api?generateFlow=1&sessionID={sess_id}")
    sentences_json = json.loads(sentences_resp.text)['data']
    sentences = []
    for i in range(1, len(sentences_json), 2):
        sentences.append(sentences_json[i]['text'])
    return sentences