import azure.cognitiveservices.speech as speechsdk
import time

# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
speech_key, service_region, language = "3b12ccebd5ba4fadbdf187bbe8de9289", "eastasia", "ja-JP"
speech_config = speechsdk.SpeechConfig(
    subscription=speech_key, region=service_region, speech_recognition_language=language)

# to text files
num = 0
while True:
    try:
        path_w = "text_data/from_microphone/" + str(num) + ".txt"
        f = open(path_w, mode='x')
        #print("書き込めた")
        break
    except:
        num += 1
        #print("書き込めなかった")
#print("抜けた")

# Creates a recognizer with the given settings
# Input from microphone
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

print("Say something...")

def recognized(evt):
    print('「{}」'.format(evt.result.text))
    # do something
    # to text file
    with open(path_w, mode="a") as f:
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