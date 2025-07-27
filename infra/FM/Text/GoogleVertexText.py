# importing the libraries
import logging
import os
from google import genai
from google.genai import types

from domain.cropLoss.cropLossPromptDefinition import cropLossPrompt
from domain.cropLoss.marketPricePromptDefinition import marketPricePrompt
from domain.cropLoss.cropSubsidyPromptDefinition import cropSubsidyPrompt
from domain.mapAPI import get_search_place


logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = genai.Client()

def llm_vertex_cropLoss():
    try:
        print("cropp llm")
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
            contents=cropLossPrompt(),
            config=config
        )
        return response.text
    except Exception as e:
        logger.error(e)
        raise ValueError("Error Occurred in crop loss Agent")


def llm_vertex_marketComp():
    try:
        print("cropp llm")
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
            contents=marketPricePrompt(),
            config=config
        )
        return response.text
    except Exception as e:
        logger.error(e)
        raise ValueError("Error Occurred in market Price Agent")


def llm_vertex_cropSubsidy():
    try:
        print("cropp llm")
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
            contents=cropSubsidyPrompt(),
            config=config
        )
        return response.text
    except Exception as e:
        logger.error(e)
        raise ValueError("Error Occurred in subsidy Agent")