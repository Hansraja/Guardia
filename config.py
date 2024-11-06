# config.py

import argparse
import os

DATABASE = {
    'host': '172.105.42.216',
    'user': 'college1_guardia',
    'password': 'Guardia@sss3',
    'database': 'college1_guardia'
}
HAAR_CASCADE_MODEL = 'resources/haarcascade_frontalface_default.xml'
API_KEY = "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" # os.environ.get('API_KEY')
SPEECH_KEY = 'EMTL0Hqwht6OrTiiNNfKau9hmToD5IqYSPgdyzLE1t17TjKAd0JUJQQJ99AKACYeBjFXJ3w3AAAYACOGzeyH' # os.environ.get('SPEECH_KEY')
SPEECH_REGION = 'eastus' # os.environ.get('SPEECH_REGION')
SPEECH_LANG = 'en-IN'
SPEECH_VOICE = 'en-IN-AashiNeural' # 'en-US-AvaMultilingualNeural'
FACE_DISTANCE = 1 # in meters
APP_SECRET_KEY = "96b1031590dfb8ed5429aa840ec152355ef995ad4976b4fd2de227077b3fc660"

def parse_arguments():
    parser = argparse.ArgumentParser(description='Command portal for the application.')
    parser.add_argument('--web', action='store_true', help='Run the web server')
    parser.add_argument('--ai', action='store_true', help='Run the AI engine')
    parser.add_argument('--cs_user', action='store_true', help='Create a super user')
    parser.add_argument('--update_super_user', action='store_true', help='Update a super user')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    if args.web:
        from web.app import app
        print("Starting the web server...")
        app.run(debug=True)
    
    if args.ai:
        from modules.assistant import assistant
        print("Starting the AI engine...")
        assistant()
        
    if args.cs_user:
        from modules.utils import create_super_user
        email = input("Enter Email: ")
        password = input("Enter password: ")
        res = create_super_user(email, password)
        print(res)

    if args.update_super_user:
        # from modules.user_management import update_super_user
        username = input("Enter username: ")
        new_password = input("Enter new password: ")
        # update_super_user(username, new_password)
        print("Super user updated successfully.")