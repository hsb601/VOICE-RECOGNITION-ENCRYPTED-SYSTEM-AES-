from flask import Flask, render_template, jsonify, request
from Crypto.Cipher import AES
import base64
import os
import numpy as np
import plotly.express as px
import sounddevice as sd
import random
import string
from pydub import AudioSegment
from werkzeug.utils import secure_filename 
import wave
from scipy.io import wavfile

app = Flask(__name__)

# Fixed AES Key and IV
AES_KEY = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(32))
AES_IV = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16))
print("AES Key is ", AES_KEY)

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling the encryption request
@app.route('/encrypt', methods=['GET'])
def encrypt():

    # Read the original audio file
    audio_path = 'C:/Users/PCS/Downloads/Recorded.wav'
    audio_segment = AudioSegment.from_file(audio_path, format='wav')
    channels = audio_segment.channels
    sample_width = audio_segment.sample_width
    frame_rate = audio_segment.frame_rate

    print(f"Number of channels: {channels}")
    print(f"Sample width: {sample_width} bytes")
    print(f"Frame rate: {frame_rate} Hz")
    # Play the original audio
    sd.play(np.array(audio_segment.get_array_of_samples()), audio_segment.frame_rate)

    # Encrypt the contents of the original audio file
    contents = audio_segment.raw_data
    encryptor = AES.new(AES_KEY.encode("utf-8"), AES.MODE_CFB, AES_IV.encode("utf-8"))
    encrypted_audio = encryptor.encrypt(contents)

    # Save the encrypted audio to a WAV file
    encrypted_wav_path = 'F:/CE8D,haseeb javed, 129/(CE-408) Cryptography and Network Security/finalproject/encrypted_audio.wav'
    with wave.open(encrypted_wav_path, 'wb') as wav_file:
        wav_file.setnchannels(audio_segment.channels)
        wav_file.setsampwidth(audio_segment.sample_width)
        wav_file.setframerate(audio_segment.frame_rate)
        wav_file.writeframes(encrypted_audio)

    print(f"A file titled 'encrypted_audio_file.wav' is generated, which is the encrypted audio to be communicated")
    print("AES Key is ", AES_KEY)
    return jsonify({'success': True, 'message': 'Audio encrypted successfully.'})

# Route for handling the decryption request
@app.route('/decrypt', methods=['GET'])
def decrypt():
    # Read the encrypted audio file
    encrypted_wav_path = 'F:/CE8D,haseeb javed, 129/(CE-408) Cryptography and Network Security/finalproject/encrypted_audio.wav'
    with wave.open(encrypted_wav_path, 'rb') as wav_file:
        contents = wav_file.readframes(wav_file.getnframes())

    # Prompt the user for the decryption key
    user_key = request.args.get('key')
    
    # Check if the user-provided key matches the encryption key
    if user_key == AES_KEY:
        # Decrypt the audio file
        decryptor = AES.new(AES_KEY.encode("utf-8"), AES.MODE_CFB, AES_IV.encode("utf-8"))
        decrypted_audio = decryptor.decrypt(contents)

        # Save the decrypted audio to a WAV file
        decrypted_wav_path = 'F:/CE8D,haseeb javed, 129/(CE-408) Cryptography and Network Security/finalproject/decrypted_audio.wav'
        with wave.open(decrypted_wav_path, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Set the number of channels according to your audio
            wav_file.setsampwidth(2)  # Set the sample width according to your audio
            wav_file.setframerate(48000)  # Set the frame rate according to your audio
            wav_file.writeframes(decrypted_audio)

        # Read the decrypted audio file
        audio_segment = AudioSegment.from_file(decrypted_wav_path, format='wav')
        sd.play(np.array(audio_segment.get_array_of_samples()), audio_segment.frame_rate)


        return jsonify({'success': True, 'message': 'Audio decrypted successfully.'})
    else:
        return jsonify({'success': False, 'message': 'Invalid key. Please provide the correct decryption key.'})

if __name__ == '__main__':
    app.run(debug=True)
