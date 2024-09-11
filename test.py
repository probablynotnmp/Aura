import anthropic
import azure.cognitiveservices.speech as speechsdk
import time

# Set your API keys
anthropic_api_key = "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"
speech_key = "c9098c43c280448c8f3c76065ce80847"
service_region = "centralindia"

# Initialize the Anthropic client
client = anthropic.Client(api_key=anthropic_api_key)

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

def generate_response(prompt):
    try:
        # Use the Claude 3 Haiku model
        response = client.completions.create(
            model="claude-3-haiku",
            prompt=f"\n\nHuman: {prompt}\n\nAssistant:",
            max_tokens_to_sample=300,
            temperature=0.7
        )
        return response.completion
    except anthropic.APIError as e:
        print(f"Anthropic API error: {e}")
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
