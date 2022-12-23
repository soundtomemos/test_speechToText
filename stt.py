import azure.cognitiveservices.speech as speechsdk
import time

# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").

# SPEECH_KEY, SPEECH_REGION には setx SPEECH_KEY your-key をコンソールで実行する必要がある
speech_key, service_region, language = "os.environ.get('SPEECH_KEY')", "os.environ.get('SPEECH_REGION')", "ja-JP"
speech_config = speechsdk.SpeechConfig(
    subscription=speech_key, region=service_region, speech_recognition_language=language)

# to text files
num = 0
while True:
    try:
        path_w = "text_data/from_audio/" + str(num) + ".txt"
        f = open(path_w, mode='x')
        break
    except:
        num += 1

# Creates a recognizer with the given settings
# Input from microphone
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

print("Say something...")

def recognized(evt):
    print('「{}」'.format(evt.result.text))
    # do something
    # to text file
    with open(path_w, mode="a", encoding="utf-8") as f:
        f.write(evt.result.text + "\n")

def start(evt):
    print('SESSION STARTED: {}'.format(evt))

def stop(evt):
    print('SESSION STOPPED {}'.format(evt))

speech_recognizer.recognized.connect(recognized)
speech_recognizer.session_started.connect(start)
speech_recognizer.session_stopped.connect(stop)

try:
    speech_recognizer.start_continuous_recognition()
    time.sleep(60)
except KeyboardInterrupt:
    print("bye.")
    speech_recognizer.recognized.disconnect_all()
    speech_recognizer.session_started.disconnect_all()
    speech_recognizer.session_stopped.disconnect_all()