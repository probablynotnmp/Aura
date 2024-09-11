import azure.cognitiveservices.speech as speechsdk
import openai
import time
import tiktoken

openai.api_key = "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"

speech_key = "c9098c43c280448c8f3c76065ce80847"
service_region = "centralindia"

def num_tokens_from_string(string: str, model: str = "gpt-4o-mini"):
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def recognize_speech():
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Listening...")
    result = recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"You: {result.text}")
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized.")
        return None
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech Recognition canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")
        return None

def predefined_response(user_input):
    user_input = user_input.lower()
    intents = {
        "Hey": "Hey there, I am Aura. How can I assist you today?",
        "Hi": "Hey there, I am Aura. How can I assist you today?",
        "Hello": "Hey there, I am Aura. How can I assist you today?",
        "who are you": "I am Aura, your holographic assistant at Robopark. How can I assist you today?",
        "what are you": "I am a virtual assistant designed to help you explore Robopark. Feel free to ask me anything about the park!",
        "why were you created": "I am a virtual assistant designed by engineers at Inker Robotics to help you clear your doubts about Robopark. Feel free to ask me anything about the park!",
        "how can you help me": "I can guide you through the exhibits, answer questions about Robopark, and provide information on our latest attractions.",
        "what is robopark": "Robopark is an interactive experience center initiative by Inker Robotics where you can explore the latest in robotics, AI, and smart technologies. Each exhibit is designed to be both informative and engaging."
    }

    inappropriate_keywords = ["retard", "hate", "stupid", "dumb", "fuck", "die", "kill", "bitch", "dick"]
    for word in inappropriate_keywords:
        if word in user_input:
            return "I'm here to help with any questions you have about Robopark, but let's keep the conversation respectful."

    return intents.get(user_input, None)

def generate_response(prompt):
    predefined = predefined_response(prompt)
    if predefined:
        return predefined

    token_limit = 1000
    tokens_used = num_tokens_from_string(prompt)

    if tokens_used > token_limit:
        print(f"Token limit exceeded. Input tokens used: {tokens_used}, limit is {token_limit}.")
        return "Sorry, your input is too long. Please simplify your question."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content']
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return "Sorry, I'm having trouble connecting to my server right now."

def speak_text(text):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    synthesizer.speak_text_async(text)

def main():
    print("Aura is ready to talk with you.")
    while True:
        user_input = recognize_speech()
        if user_input is None:
            continue
        if user_input.lower() in ['exit', 'quit', 'stop']:
            print("Goodbye!")
            speak_text("Goodbye!")
            break

        response = generate_response(user_input)
        print(f"Aura: {response}")
        speak_text(response)
        time.sleep(1)

if __name__ == "__main__":
    main()
