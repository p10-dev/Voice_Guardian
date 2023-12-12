import base64
import hashlib
import os
import wave
from Crypto.Cipher import AES
from Crypto import Random
import wave

def encrypt(keyStr, audio_file_path):
    private_key = hashlib.sha256(keyStr.encode()).digest()

    with wave.open(audio_file_path, 'rb') as audio_file:
        audio_data = audio_file.readframes(audio_file.getnframes())

    rem = len(audio_data) % 16
    padded = audio_data + (b'\0' * (16 - rem)) if rem > 0 else audio_data

    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CFB, iv, segment_size=128)
    enc = cipher.encrypt(padded)[:len(audio_data)]
    return base64.b64encode(iv + enc).decode()

def encrypt_and_save(keyStr, audio_file_path):
    encrypted_data = encrypt(keyStr, audio_file_path)

    # Get the base name of the input file (without the path)
    input_file_name = os.path.basename(audio_file_path)

    # Create the encrypted file name by adding ".enc" extension
    encrypted_file_name = os.path.splitext(input_file_name)[0] + '.enc'

    # Save the encrypted data to the file
    with open(encrypted_file_name, 'w') as encrypted_file:
        encrypted_file.write(encrypted_data)

    print(f'Encrypted file saved as: {encrypted_file_name}')


# def main():
#     audio_file_path = 'evi.wav'
#     encrypted_file_path = 'evi.enc'
#     decrypted_file_path = 'e.wav'

#     encrypted = encrypt('SecretKey', audio_file_path)
#     with open(encrypted_file_path, 'w') as file:
#         file.write(encrypted)

#     decrypt('SecretKey', encrypted, decrypted_file_path)

# if __name__ == '__main__':
#     main()
