# importing the libraries
import asyncio
from infra.MemoryStore.MemoryStoreJson import MemoryDBConnect

from infra.FM.ImageText.GoogleVertexImageText import llm_vertex_diag,llm_vertex_market,llm_vertex_intent,llm_vertex_std,llm_vertex_navigate, llm_vertex_scheme
from infra.FM.Audio.GoogleVertexAudio import llm_vertex_audio_intent, llm_vertex_audio_market, llm_vertex_audio_cropDiag, llm_vertex_audio_navigation, llm_vertex_audio_scheme, llm_vertex_audio_trans, llm_vertex_audio_stdResponse

def farmerImageTextChat(message):
    try:
        print("farmerChat")
        mem = MemoryDBConnect()
        history = mem.get_history(message)
        message['history'] = history
        intent_response = llm_vertex_intent(message)
        if 'Scheme' in intent_response:
            scheme_response = llm_vertex_scheme(message)
            message['response'] = scheme_response
            mem.put_history(message)
            return scheme_response
        elif 'Market' in intent_response:
            market_response = llm_vertex_market(message)
            message['response'] = market_response
            mem.put_history(message)
            return market_response
        elif 'Navigate' in intent_response:
            navigate_response = llm_vertex_navigate(message)
            message['response'] = navigate_response
            mem.put_history(message)
            return navigate_response
        elif 'Diagnosis' in intent_response:
            diagnosis_response = llm_vertex_diag(message)
            message['response']= diagnosis_response
            mem.put_history(message)
            return diagnosis_response
        else:
            std_response = llm_vertex_std(message)
            return std_response
    except ValueError as err:
        print(err)
        raise ValueError("Error in farmerChat")


def farmerAudioChat(message):
    try:
        print("farmerChat")
        mem = MemoryDBConnect()
        history = mem.get_history(message)
        message['history'] = history
        intent_response = llm_vertex_audio_intent(message)
        message['question'] = intent_response
        if "market" in intent_response.lower():
            market_response = asyncio.run(llm_vertex_audio_market(message))
            message['response']=llm_vertex_audio_trans(market_response)
            mem.put_history(message)
            return market_response
        elif "scheme" in intent_response.lower():
            scheme_response = asyncio.run(llm_vertex_audio_scheme(message))
            message['response']=llm_vertex_audio_trans(scheme_response)
            mem.put_history(message)
            return scheme_response
        elif "navigate" in intent_response.lower():
            navigate_response = asyncio.run(llm_vertex_audio_navigation(message))
            message['response']=llm_vertex_audio_trans(navigate_response)
            mem.put_history(message)
            return navigate_response
        elif "diagnosis" in intent_response.lower():
            diagnosis_response = asyncio.run(llm_vertex_audio_cropDiag(message))
            message['response']=llm_vertex_audio_trans(diagnosis_response)
            mem.put_history(message)
            return diagnosis_response
        else:
            std_response = asyncio.run(llm_vertex_audio_stdResponse(message))
            return std_response
    except ValueError as err:
        print(err)
        raise ValueError("Error in farmerAudioChat")