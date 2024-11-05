import argparse

# config.py

DATABASE_PATH = 'database/guardia.db'
# FACE_LANDMARKS_MODEL = 'resources/shape_predictor_68_face_landmarks.dat'
HAAR_CASCADE_MODEL = 'resources/haarcascade_frontalface_default.xml'
API_KEY = "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"

def parse_arguments():
    parser = argparse.ArgumentParser(description='Command portal for the application.')
    parser.add_argument('--web', action='store_true', help='Run the web server')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    if args.web:
        from web.app import app
        print("Starting the web server...")
        app.run(debug=True)
        # Add code to start the web server here