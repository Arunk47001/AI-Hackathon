# importing the libraries
import logging
import os
from google import genai
from google.genai import types

from domain.PromptDefinition import intentDefinition, schemeDefinition, navigationDefinition, standardResponse, cropDiagnosisPrompt, marketDefinition
from domain.mapAPI import get_search_place


logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = genai.Client()

def llm_vertex_intent(message):
    try:
        print("intent llm")
        generation_config = types.GenerateContentConfig(
            temperature=0.0,
            top_p=0.05,
            candidate_count=1,
        )
        if "images" in message:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[intentDefinition(message['question'],message['history']), types.Part.from_bytes(data=message['images'], mime_type="image/png")],
                config = generation_config
            )
        else:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=intentDefinition(message['question'], message['history']),
                config=generation_config
            )
        return response.text
    except Exception as e:
        logger.error(e)
        raise ValueError("Error Occurred in Intent Agent")


def llm_vertex_diag(message):
    try:
        print("diag llm")
        grounding_tool = types.Tool(
            google_search=types.GoogleSearch()
        )
        config = types.GenerateContentConfig(
            tools=[grounding_tool],
            temperature = 0.0,
            top_p = 0.05,
            candidate_count = 1,
        )
        if 'images' in message:
            response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[cropDiagnosisPrompt(message['question'], message['history']), types.Part.from_bytes(data=message['images'], mime_type="image/png")],
            config = config
            )
        else:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=cropDiagnosisPrompt(message['question'], message['history']),
                config=config
            )
        return response.text
    except Exception as e:
        logger.error(e)
        raise ValueError("Error Occurred in Diag Agent")


def llm_vertex_market(message):
    try:
        print("market llm")
        grounding_tool = types.Tool(
            google_search=types.GoogleSearch(),
        )
        config = types.GenerateContentConfig(
            tools=[grounding_tool],
            temperature=0.0,
            top_p=0.05,
            candidate_count=1
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=marketDefinition(message['question'], message['history']),
            config=config
        )
        return response.text
    except Exception as e:
        logger.error(e)
        raise ValueError("Error Occurred in Market Agent")


def llm_vertex_navigate(message):
    try:
        print("navigate llm")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=navigationDefinition(message['question'], message['history']),
            config=types.GenerateContentConfig(
                tools=[get_search_place],
                temperature=0.0,
                top_p=0.05,
                candidate_count=1
            )
        )
        return response.text
    except Exception as e:
        logger.error(e)
        raise ValueError("Error Occurred in Navigate Agent")


def llm_vertex_std(message):
    try:
        print("stand llm")
        generation_config = types.GenerateContentConfig(
            temperature=0.0,
            top_p=0.05,
            candidate_count=1,
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=standardResponse(message['question']),
            config = generation_config
        )
        return response.text
    except Exception as e:
        logger.error(e)
        raise ValueError("Error Occurred in Standard Agent")


def llm_vertex_scheme(message):
    try:
        print("scheme llm")
        grounding_tool = types.Tool(
            google_search=types.GoogleSearch()
        )
        config = types.GenerateContentConfig(
            tools=[grounding_tool],
            temperature = 0.0,
            top_p = 0.05,
            candidate_count = 1,
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=schemeDefinition(message['question'], message['history']),
            config = config
            )
        return response.text
    except Exception as e:
        logger.error(e)
        raise ValueError("Error Occurred in Scheme Agent")