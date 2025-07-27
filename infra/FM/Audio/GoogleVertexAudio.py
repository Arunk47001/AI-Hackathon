# importing the libraries
import logging
import os
from google import genai
from google.genai import types
import wave

from domain.PromptAudioDefinition import intentaudioDefinition, marketaudioDefinition, navigationaudioDefinition, cropDiagnosisaudioPrompt, schemeaudioDefinition, standardaudioResponse
from domain.mapAPI import get_search_place


logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = genai.Client()


def llm_vertex_audio_intent(message):
    print("intent llm")
    generation_config = types.GenerateContentConfig(
        temperature=0.0,
        top_p=0.05,
        candidate_count=1,
    )
    response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[intentaudioDefinition(),
                      types.Part.from_bytes(data=message['audio'], mime_type="audio/pcm")],
            config=generation_config
        )
    return response.text


async def llm_vertex_audio_market(message):
    print("market llm")
    model = "gemini-2.5-flash-preview-native-audio-dialog"
    config = {
        "response_modalities": ["AUDIO"],
        "system_instruction": marketaudioDefinition(message['history']),
    }
    async with client.aio.live.connect(model=model, config=config) as session:
        await session.send_client_content(
            turns={"role": "user", "parts": [{"text": message['question']}]}, turn_complete=True
        )
        wf = wave.open("audioMarket.wav", "wb")
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        async for response in session.receive():
            if response.data is not None:
                wf.writeframes(response.data)
        wf.close()
    with open("audioMarket.wav", "rb") as f:
        audio_bytes = f.read()
    return audio_bytes

async def llm_vertex_audio_scheme(message):
    model = "gemini-2.5-flash-preview-native-audio-dialog"
    config = {
        "response_modalities": ["AUDIO"],
        "system_instruction": schemeaudioDefinition(message['history']),
    }
    async with client.aio.live.connect(model=model, config=config) as session:
        await session.send_client_content(
            turns={"role": "user", "parts": [{"text": message['question']}]}, turn_complete=True
        )
        wf = wave.open("audioScheme.wav", "wb")
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        async for response in session.receive():
            if response.data is not None:
                wf.writeframes(response.data)
        wf.close()
    with open("audioScheme.wav", "rb") as f:
        audio_bytes = f.read()
    return audio_bytes


async def llm_vertex_audio_navigation(message):
    model = "gemini-2.5-flash-preview-native-audio-dialog"
    config = {
        "response_modalities": ["AUDIO"],
        "system_instruction": navigationaudioDefinition(message['history']),
    }
    async with client.aio.live.connect(model=model, config=config) as session:
        await session.send_client_content(
            turns={"role": "user", "parts": [{"text": message['question']}]}, turn_complete=True
        )
        wf = wave.open("audioNavigation.wav", "wb")
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        async for response in session.receive():
            if response.data is not None:
                wf.writeframes(response.data)
        wf.close()
    with open("audioNavigation.wav", "rb") as f:
        audio_bytes = f.read()
    return audio_bytes


async def llm_vertex_audio_cropDiag(message):
    model = "gemini-2.5-flash-preview-native-audio-dialog"
    config = {
        "response_modalities": ["AUDIO"],
        "system_instruction": cropDiagnosisaudioPrompt(message['history']),
    }
    async with client.aio.live.connect(model=model, config=config) as session:
        await session.send_client_content(
            turns={"role": "user", "parts": [{"text": message['question']}]}, turn_complete=True
        )
        wf = wave.open("audioCropDiag.wav", "wb")
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        async for response in session.receive():
            if response.data is not None:
                wf.writeframes(response.data)
    wf.close()
    with open("audioCropDiag.wav", "rb") as f:
        audio_bytes = f.read()
    return audio_bytes

def llm_vertex_audio_trans(message):
    generation_config = types.GenerateContentConfig(
        temperature=0.0,
        top_p=0.05,
        candidate_count=1,
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[intentaudioDefinition(),
                  types.Part.from_bytes(data=message, mime_type="audio/pcm")],
        config=generation_config
    )
    return response.text


async def llm_vertex_audio_stdResponse(message):
    model = "gemini-2.5-flash-preview-native-audio-dialog"
    config = {
        "response_modalities": ["AUDIO"],
        "system_instruction": standardaudioResponse(),
    }
    async with client.aio.live.connect(model=model, config=config) as session:
        await session.send_client_content(
            turns={"role": "user", "parts": [{"text": message['question']}]}, turn_complete=True
        )
        wf = wave.open("audiostdResponse.wav", "wb")
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        async for response in session.receive():
            if response.data is not None:
                wf.writeframes(response.data)
        wf.close()
    with open("audiostdResponse.wav", "rb") as f:
        audio_bytes = f.read()
    return audio_bytes