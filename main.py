# main.py

import threading
import cv2
from modules.face_recognition_module import FaceRecognitionModule
from modules.speech_recognition_module import SpeechRecognitionModule
from modules.text_to_speech_module import TextToSpeechModule
from modules.mode_switching import ModeSwitching
from modules.utils import init_database, generate_random_access_key, add_user_entry_log
import time
from modules.assistant import GuardiaAssistant
from modules.user_registration import register_user

def main():
    init_database()
    face_recognition_module = FaceRecognitionModule()
    speech_recognition_module = SpeechRecognitionModule()
    text_to_speech_module = TextToSpeechModule()
    mode_switching = ModeSwitching()
    assistant = GuardiaAssistant()

    cap = None
    listening = False

    def video_stream():
        nonlocal cap, listening
        while True:
            if mode_switching.current_mode == 'security':
                cap = cv2.VideoCapture(0)
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    face_names = face_recognition_module.detect_and_recognize(frame)
                    if face_names is None:
                        continue
                    elif len(face_names) == 2 and face_names[0] == 'Unknown':
                        listening = True
                        handle_unknown_user(face_names[1])
                        listening = False
                    else:
                        handle_recognized_faces(face_names)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                    cap.release()
                    cv2.destroyAllWindows()
            else:
                if cap is not None:
                    cap.release()
                cv2.destroyAllWindows()

    def handle_unknown_user(face_encoding):
        text_to_speech_module.speak("You are not recognized. Please provide your name")
        while True:
            name, mobile = get_user_input()
            text_to_speech_module.speak(f"Thank you {name}. Your mobile number is {mobile}, is that correct?")
            response = speech_recognition_module.listen(cmd=True)
            if 'yes' in response or 'ya' in response or 'yeah' in response or 'correct' in response or 'haan' in response:
                if register_user(name, mobile, face_encoding):
                    accesskey = generate_random_access_key()
                    text_to_speech_module.speak(f"Hey {name}, your access key is {accesskey}")
                    add_user_entry_log(name, accesskey)
                    break
                else:
                    text_to_speech_module.speak("User registration failed")
            else:
                text_to_speech_module.speak("Please provide your name again")

    def handle_recognized_faces(face_names):
        for name, (x, y, w, h) in face_names:
            accesskey = generate_random_access_key()
            add_user_entry_log(name, accesskey)
            text_to_speech_module.speak(f"Hey {name}, your access key is {accesskey}")

    def get_user_input():
        name = speech_recognition_module.listen()
        text_to_speech_module.speak("Please provide your mobile number")
        mobile = speech_recognition_module.listen()
        return name, mobile

    def audio_processing():
        nonlocal listening
        while True:
            if listening:
                continue
            command = speech_recognition_module.listen(cmd=True)
            if 'assistant mode' in command:
                switch_to_assistant_mode()
            elif 'security mode' in command:
                mode_switching.switch_mode('security')
                text_to_speech_module.speak("Switched to security mode")
            elif mode_switching.current_mode == 'assistant':
                response = process_assistant_commands(command)
                text_to_speech_module.speak(response)

    def switch_to_assistant_mode():
        text_to_speech_module.speak("Please provide the password to switch to assistant mode")
        password = speech_recognition_module.listen(cmd=True)
        if password == 'password':
            mode_switching.switch_mode('assistant')
            text_to_speech_module.speak("Switched to assistant mode")
        else:
            text_to_speech_module.speak("Incorrect password")

    def process_assistant_commands(command):
        if 'time' in command:
            return f"The current time is {time.strftime('%I:%M %p')}"
        if command == '':
            return "I'm sorry, I didn't catch that"
        else:
            return assistant.chat(command)

    video_thread = threading.Thread(target=video_stream)
    audio_thread = threading.Thread(target=audio_processing)

    video_thread.start()
    audio_thread.start()

    video_thread.join()
    audio_thread.join()

if __name__ == '__main__':
    main()
