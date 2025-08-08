# Farmer AI Assistant — API and Module Reference


## Quickstart

- Requirements: Python 3.10+, `pip install -r requirements.txt`
- Environment:
  - Set Google GenAI credentials (one of):
    - `export GOOGLE_API_KEY=YOUR_KEY`
    - or Application Default Credentials on GCP
  - Optional: `export PORT=3000`
- Initialize memory store (once):
  - Create file `infra/MemoryStore/memory.json` with `{}` as content
- Run:
  - `python /workspace/main.py`


## REST API Endpoints (Flask)

Base URL: `http://<host>:<port>` (default port 3000)

### POST `/farm/agent/chat`
- Purpose: Multimodal chat (text + optional image) with routing to Market/Scheme/Navigate/Diagnosis/Standard agents
- Content-Type: `multipart/form-data`
- Form fields:
  - `user_name` (string, required)
  - `session_id` (string, required)
  - `question` (string, required)
  - `image` (file, optional; PNG/JPEG bytes)
- Response: `201 text/plain` (Gemini text)
- Errors: `400` (missing parameter), `500` (internal)
- cURL (text only):
  ```bash
  curl -X POST http://localhost:3000/farm/agent/chat \
    -F "user_name=farmer1" \
    -F "session_id=sess-123" \
    -F "question=What is tomato price in Mandya?"
  ```
- cURL (with image):
  ```bash
  curl -X POST http://localhost:3000/farm/agent/chat \
    -F "user_name=farmer1" \
    -F "session_id=sess-123" \
    -F "question=What disease is this?" \
    -F "image=@/path/leaf.png;type=image/png"
  ```

### POST `/farm/agent/audio`
- Purpose: Voice chat pipeline. Detects intent, generates audio reply, and stores transcript in memory
- Content-Type: `multipart/form-data`
- Form fields:
  - `user_name` (string, required)
  - `session_id` (string, required)
  - `audio` (file, required; PCM bytes, `audio/pcm`)
- Response: `201 audio/wav` with inline filename `audiov1.wav`
- Errors: `400`, `500`
- cURL:
  ```bash
  curl -X POST http://localhost:3000/farm/agent/audio \
    -F "user_name=farmer1" \
    -F "session_id=sess-123" \
    -F "audio=@/path/input.pcm;type=audio/pcm" \
    -o reply.wav
  ```

### GET `/farm/agent/cropLoss`
- Purpose: Summarize crop-loss related updates for Mandya (Gemini text)
- Response: `200 text/plain`
- cURL:
  ```bash
  curl http://localhost:3000/farm/agent/cropLoss
  ```

### GET `/farm/agent/marketComp`
- Purpose: Compare market prices for tomatoes and mangoes in districts near Mandya
- Response: `200 application/json` (stringified Gemini text). Note: returned JSON may be a JSON-encoded string
- cURL:
  ```bash
  curl http://localhost:3000/farm/agent/marketComp
  ```

### GET `/farm/agent/cropSubsidy`
- Purpose: List subsidies/relief schemes for tomato and mango farmers (Gemini text)
- Response: `200 text/plain`
- cURL:
  ```bash
  curl http://localhost:3000/farm/agent/cropSubsidy
  ```


## Python Modules and Public Functions

### `usecase/usecase_FarmerAgent.py`
- `farmerImageTextChat(message: dict) -> str`
  - Routes via intent to Market/Scheme/Navigate/Diagnosis/Standard
  - Input `message` keys:
    - `user_name`: str
    - `session_id`: str
    - `question`: str
    - `images`: bytes (optional PNG/JPEG)
  - Returns: Gemini text response
  - Side effects: Reads/writes chat history via `MemoryDBConnect`
  - Example:
    ```python
    from usecase.usecase_FarmerAgent import farmerImageTextChat

    resp = farmerImageTextChat({
        "user_name": "farmer1",
        "session_id": "sess-123",
        "question": "Nearest KVK in Mandya?"
    })
    print(resp)
    ```

- `farmerAudioChat(message: dict) -> bytes`
  - Detects intent from audio, generates audio reply, stores transcript (via text translation)
  - Input `message` keys:
    - `user_name`: str
    - `session_id`: str
    - `audio`: bytes (PCM)
  - Returns: WAV bytes
  - Example (writing output):
    ```python
    from usecase.usecase_FarmerAgent import farmerAudioChat

    with open("/path/input.pcm", "rb") as f:
        audio_pcm = f.read()

    wav_bytes = farmerAudioChat({
        "user_name": "farmer1",
        "session_id": "sess-123",
        "audio": audio_pcm,
    })

    with open("reply.wav", "wb") as out:
        out.write(wav_bytes)
    ```


### `usecase/usercase_cropLossAgent.py`
- `cropLossAgent() -> str`
- `cropLossMarketPriceComp() -> Any` (JSON-encoded text)
- `cropLossSubsidy() -> str`


### `infra/FM/ImageText/GoogleVertexImageText.py`
- `llm_vertex_intent(message: dict) -> str`
  - Uses `intentDefinition(question, history)`; supports optional `images`
- `llm_vertex_diag(message: dict) -> str`
  - Uses Google Search tool grounding + optional image
- `llm_vertex_market(message: dict) -> str`
- `llm_vertex_navigate(message: dict) -> str`
- `llm_vertex_std(message: dict) -> str`
- `llm_vertex_scheme(message: dict) -> str`
- Common `message` keys: `question: str`, `history: list[dict]`, optional `images: bytes`

Example:
```python
from infra.FM.ImageText.GoogleVertexImageText import llm_vertex_market
resp = llm_vertex_market({"question": "Tomato price in Mandya?", "history": []})
```


### `infra/FM/Audio/GoogleVertexAudio.py`
- `llm_vertex_audio_intent(message: dict) -> str` (intent + transcript)
- `llm_vertex_audio_market(message: dict) -> bytes` (async)
- `llm_vertex_audio_scheme(message: dict) -> bytes` (async)
- `llm_vertex_audio_navigation(message: dict) -> bytes` (async)
- `llm_vertex_audio_cropDiag(message: dict) -> bytes` (async)
- `llm_vertex_audio_trans(message: bytes) -> str` (transcribe PCM to text)
- `llm_vertex_audio_stdResponse(message: dict) -> bytes` (async)
- Common `message` keys: `question: str`, `history: list[dict]`

Async usage example:
```python
import asyncio
from infra.FM.Audio.GoogleVertexAudio import llm_vertex_audio_market

async def main():
    audio = await llm_vertex_audio_market({"question": "Tomato price?", "history": []})
    with open("reply.wav", "wb") as f:
        f.write(audio)

asyncio.run(main())
```


### `infra/FM/Text/GoogleVertexText.py`
- `llm_vertex_cropLoss() -> str`
- `llm_vertex_marketComp() -> str`
- `llm_vertex_cropSubsidy() -> str`


### `infra/MemoryStore/MemoryStoreJson.py`
- `class MemoryDBConnect`
  - `get_history(keys: dict) -> list`
    - Expects `keys["session_id"]`; returns conversation list or `[]`
  - `put_history(keys: dict) -> None`
    - Expects: `session_id`, `question`, `response`
    - Appends to `infra/MemoryStore/memory.json`
  - Notes:
    - File path: `infra/MemoryStore/memory.json`
    - Ensure the file exists and is writable; initialize with `{}`

Example:
```python
from infra.MemoryStore.MemoryStoreJson import MemoryDBConnect

db = MemoryDBConnect()
chat = db.get_history({"session_id": "sess-123"})
db.put_history({
    "session_id": "sess-123",
    "question": "What is MSP for paddy?",
    "response": "₹2183/quintal (example)"
})
```


### `domain/mapAPI.py`
- `get_search_place(query: str) -> str`
  - Thin wrapper around Google Places Text Search API
  - Note: You must supply an API key in the URL template or via environment; current implementation leaves key empty


### Domain Prompt Modules
- `domain/PromptDefinition.py`, `domain/PromptAudioDefinition.py` and `domain/cropLoss/*`
  - Provide system prompts and templates consumed by the FM modules
  - Not intended as direct public APIs but useful for customization


## Error Handling and Status Codes
- REST endpoints return `400` for missing parameters and `500` for internal errors
- FM wrappers raise `ValueError` with contextual messages that surface to the endpoints


## Notes on Google GenAI Client
- Library: `google-genai` (see `requirements.txt`)
- Client initialization uses `genai.Client()`; ensure credentials are available in environment
- Models used include `gemini-2.5-flash` and `gemini-2.5-flash-preview-native-audio-dialog`


## Versioning
- This reference documents the current code in `controller/app.py`, `usecase/*`, `infra/*`, and `domain/*` as of this repository state.