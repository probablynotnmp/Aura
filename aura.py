import cohere
import azure.cognitiveservices.speech as speechsdk
import time

cohere_api_key = "8iC9J6oTj8M7O6x7H0wkzsnizOXecxx9i51Qtwoo"
speech_key = "c9098c43c280448c8f3c76065ce80847"
service_region = "centralindia"

co_client = cohere.Client(cohere_api_key)


def predefined_response(user_input):
    user_input = user_input.lower()

    intents = {
        "hey": "Hey there, I am Aura. How can I assist you today?",
        "hi": "Hey there, I am Aura. How can I assist you today?",
        "hello": "Hey there, I am Aura. How can I assist you today?",
        "hello what is your name": "My name is Aura. and I am a holographic virtual assistant made at Inker Robotics to help you at Robopark",
        "hi what is your name": "My name is Aura. and I am a holographic virtual assistant made at Inker Robotics to help you at Robopark",
        "what is your name": "My name is Aura. and I am a holographic virtual assistant made at Inker Robotics to help you at Robopark",
        "your name": "My name is Aura. and I am a holographic virtual assistant made at Inker Robotics to help you at Robopark",
        "who are you": "I am Aura, A holographic virtual assistant made at Inker Robotics to help you at Robopark. How can I assist you today?",
        "hi who are you": "I am Aura, A holographic virtual assistant made at Inker Robotics to help you at Robopark. How can I assist you today?",
        "hello who are you": "I am Aura, A holographic virtual assistant made at Inker Robotics to help you at Robopark. How can I assist you today?",
        "what are you": "I am a virtual assistant designed to help you explore Robopark. Feel free to ask me anything about the park!",
        "hi what are you": "I am a virtual assistant designed to help you explore Robopark. Feel free to ask me anything about the park!",
        "why were you created": "I am a virtual assistant designed by engineers at Inker Robotics to help you clear your doubts about Robopark. Feel free to ask me anything about the park!",
        "how can you help me": "I can guide you through the exhibits, answer questions about Robopark, and provide information on our latest attractions.",
        "hi how can you help me": "I can guide you through the exhibits, answer questions about Robopark, and provide information on our latest attractions.",
        "what is robo park": "Robopark is an interactive experience center initiative by Inker Robotics where you can explore the latest in robotics, AI, and smart technologies. Each exhibit is designed to be both informative and engaging."

    }

    inappropriate_keywords = ["retard", "hate", "stupid", "dumb", "fuck", "die", "kill", "bitch", "dick"]
    for word in inappropriate_keywords:
        if word in user_input:
            return "I'm here to help with any questions you have about Robopark, but let's keep the conversation respectful."

    for key in intents:
        if key in user_input:
            return intents[key]

    return None


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
    predefined = predefined_response(prompt)
    if predefined:
        return predefined

    try:
        response = co_client.generate(
            model='command-xlarge-nightly',
            prompt=prompt,
            max_tokens=300,
            temperature=0.7
        )
        return response.generations[0].text
    except cohere.error.CohereError as e:
        print(f"Cohere API error: {e}")
        return "Sorry, I'm having trouble connecting to my server right now."


def speak_text(text):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesis completed.")
    else:
        print(f"Speech synthesis failed: {result.reason}")


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
