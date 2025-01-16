

## Integrating OpenAI and Voice Cloning APIs

import openai
import requests

openai.api_key = "your_openai_api_key"

# Generate script
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a stock analyst."},
        {"role": "user", "content": "Write an engaging 30-second script for Ashoka Buildcon stock."}
    ]
)

script = response['choices'][0]['message']['content']
print("Generated Script: ", script)


###########################################################################################
## Voice Cloning & Text-to-Speech


elevenlabs_api = "your_elevenlabs_api_key"
url = "https://api.elevenlabs.io/v1/text-to-speech"

headers = {
    "xi-api-key": elevenlabs_api,
    "Content-Type": "application/json"
}

data = {
    "text": script,  # From OpenAI
    "voice_settings": {
        "voice_id": "your_cloned_voice_id_here",  # Your voice ID after cloning
        "stability": 0.75,
        "similarity_boost": 0.90
    }
}

response = requests.post(url, headers=headers, json=data)
# Save the audio response
with open("output.mp3", "wb") as audio_file:
    audio_file.write(response.content)
