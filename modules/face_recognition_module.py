# modules/face_recognition_module.py

import cv2
import face_recognition
from modules.utils import get_known_faces
from config import HAAR_CASCADE_MODEL

class FaceRecognitionModule:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(HAAR_CASCADE_MODEL)
        self.known_face_names, self.known_face_encodings = get_known_faces()

    def detect_and_recognize(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        face_names = []

        for (x, y, w, h) in faces:
            face_frame = frame[y:y+h, x:x+w]
            rgb_face = cv2.cvtColor(face_frame, cv2.COLOR_BGR2RGB)
            face_encodings = face_recognition.face_encodings(rgb_face)

            name = "Unknown"
            if face_encodings:
                if self.known_face_encodings:  # Check if known faces exist
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encodings[0])
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encodings[0])
                    best_match_index = face_distances.argmin()
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                else:
                    print("No known faces to compare with.")
                    return ['Unknown', face_encodings[0]]
            else:
                print("Face encoding could not be generated.")
                return None
            face_names.append((name, (x, y, w, h)))
        return face_names

