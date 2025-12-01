import os
import json
import zlib
import base64
import hashlib
import random
import string
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple


class AdvancedEncryptor:
    def __init__(self, password: str, compression_level: int = 9, encryption_rounds: int = 3):
        self.password = password
        self.compression_level = compression_level
        self.encryption_rounds = encryption_rounds
        self.chars = " " + string.punctuation + string.digits + string.ascii_letters
        self.key_seed = self._generate_key_from_password(password)
    
    def _generate_key_from_password(self, password: str) -> int:
        hash_obj = hashlib.sha256(password.encode())
        return int.from_bytes(hash_obj.digest(), byteorder='big')
    
    def _create_cipher_key(self, seed: int, round_num: int = 0) -> dict:
        random.seed(seed + round_num)
        chars_list = list(self.chars)
        key_list = chars_list.copy()
        random.shuffle(key_list)
        return dict(zip(chars_list, key_list))
    
    def _create_reverse_key(self, cipher_key: dict) -> dict:
        return {v: k for k, v in cipher_key.items()}
    
    def _substitute_encrypt(self, text: str, cipher_key: dict) -> str:
        return ''.join(cipher_key.get(char, char) for char in text)
    
    def _substitute_decrypt(self, text: str, reverse_key: dict) -> str:
        return ''.join(reverse_key.get(char, char) for char in text)
    
    def _compress_data(self, data: str) -> bytes:
        return zlib.compress(data.encode('utf-8'), level=self.compression_level)
    
    def _decompress_data(self, data: bytes) -> str:
        return zlib.decompress(data).decode('utf-8')
    
    def _add_checksum(self, data: str) -> str:
        checksum = hashlib.md5(data.encode()).hexdigest()
        return f"{checksum}::{data}"
    
    def _verify_checksum(self, data: str) -> Tuple[bool, str]:
        try:
            checksum, original_data = data.split('::', 1)
            calculated_checksum = hashlib.md5(original_data.encode()).hexdigest()
            return checksum == calculated_checksum, original_data
        except:
            return False, ""
    
    def encrypt(self, plaintext: str, use_compression: bool = True) -> str:
        if use_compression:
            compressed = self._compress_data(plaintext)
            data_to_encrypt = base64.b64encode(compressed).decode('utf-8')
        else:
            data_to_encrypt = plaintext
        
        encrypted_text = data_to_encrypt
        for round_num in range(self.encryption_rounds):
            cipher_key = self._create_cipher_key(self.key_seed, round_num)
            encrypted_text = self._substitute_encrypt(encrypted_text, cipher_key)
        
        encrypted_text = self._add_checksum(encrypted_text)
        
        metadata = {
            'compressed': use_compression,
            'rounds': self.encryption_rounds,
            'timestamp': datetime.now().isoformat()
        }
        
        metadata_str = json.dumps(metadata)
        metadata_encoded = base64.b64encode(metadata_str.encode()).decode('utf-8')
        
        return f"{metadata_encoded}||{encrypted_text}"
    
    def decrypt(self, ciphertext: str) -> Optional[str]:
        try:
            metadata_encoded, encrypted_data = ciphertext.split('||', 1)
            metadata_str = base64.b64decode(metadata_encoded.encode()).decode('utf-8')
            metadata = json.loads(metadata_str)
            
            is_valid, encrypted_data = self._verify_checksum(encrypted_data)
            if not is_valid:
                return None
            
            decrypted_text = encrypted_data
            for round_num in range(metadata['rounds'] - 1, -1, -1):
                cipher_key = self._create_cipher_key(self.key_seed, round_num)
                reverse_key = self._create_reverse_key(cipher_key)
                decrypted_text = self._substitute_decrypt(decrypted_text, reverse_key)
            
            if metadata['compressed']:
                compressed_data = base64.b64decode(decrypted_text.encode())
                plaintext = self._decompress_data(compressed_data)
            else:
                plaintext = decrypted_text
            
            return plaintext
        except:
            return None
    
    def encrypt_file(self, input_path: str, output_path: Optional[str] = None, use_compression: bool = True) -> bool:
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            encrypted = self.encrypt(content, use_compression)
            
            if output_path is None:
                output_path = f"{input_path}.encrypted"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(encrypted)
            
            return True
        except:
            return False
    
    def decrypt_file(self, input_path: str, output_path: Optional[str] = None) -> bool:
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                encrypted_content = f.read()
            
            decrypted = self.decrypt(encrypted_content)
            if decrypted is None:
                return False
            
            if output_path is None:
                output_path = input_path.replace('.encrypted', '.decrypted')
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(decrypted)
            
            return True
        except:
            return False


def interactive_menu():
    while True:
        print("\n" + "="*50)
        print("CipherForge - Advanced Encryption Tool")
        print("="*50)
        print("1. Encrypt Text")
        print("2. Decrypt Text")
        print("3. Encrypt File")
        print("4. Decrypt File")
        print("5. Exit")
        print("="*50)
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            password = input("Enter encryption password: ")
            rounds = int(input("Encryption rounds (1-10, default 3): ") or "3")
            compression = input("Use compression? (y/n, default y): ").lower() != 'n'
            
            text = input("\nEnter text to encrypt: ")
            
            encryptor = AdvancedEncryptor(password, encryption_rounds=rounds)
            encrypted = encryptor.encrypt(text, use_compression=compression)
            
            print("\n" + "-"*50)
            print("ENCRYPTED TEXT:")
            print("-"*50)
            print(encrypted)
            print("-"*50)
            
            save = input("\nSave to file? (y/n): ").lower()
            if save == 'y':
                filename = input("Enter filename: ")
                with open(filename, 'w') as f:
                    f.write(encrypted)
                print(f"Saved to {filename}")
        
        elif choice == "2":
            password = input("Enter decryption password: ")
            
            load = input("Load from file? (y/n): ").lower()
            if load == 'y':
                filename = input("Enter filename: ")
                with open(filename, 'r') as f:
                    encrypted_text = f.read()
            else:
                encrypted_text = input("\nEnter encrypted text: ")
            
            encryptor = AdvancedEncryptor(password)
            decrypted = encryptor.decrypt(encrypted_text)
            
            if decrypted:
                print("\n" + "-"*50)
                print("DECRYPTED TEXT:")
                print("-"*50)
                print(decrypted)
                print("-"*50)
            else:
                print("\nDecryption failed! Wrong password or corrupted data.")
        
        elif choice == "3":
            password = input("Enter encryption password: ")
            rounds = int(input("Encryption rounds (1-10, default 3): ") or "3")
            compression = input("Use compression? (y/n, default y): ").lower() != 'n'
            
            input_file = input("Enter input file path: ")
            output_file = input("Enter output file path (press Enter for auto): ").strip()
            if not output_file:
                output_file = None
            
            encryptor = AdvancedEncryptor(password, encryption_rounds=rounds)
            success = encryptor.encrypt_file(input_file, output_file, use_compression=compression)
            
            if success:
                print("\nFile encrypted successfully!")
            else:
                print("\nEncryption failed! Check file path.")
        
        elif choice == "4":
            password = input("Enter decryption password: ")
            
            input_file = input("Enter encrypted file path: ")
            output_file = input("Enter output file path (press Enter for auto): ").strip()
            if not output_file:
                output_file = None
            
            encryptor = AdvancedEncryptor(password)
            success = encryptor.decrypt_file(input_file, output_file)
            
            if success:
                print("\nFile decrypted successfully!")
            else:
                print("\nDecryption failed! Wrong password or corrupted file.")
        
        elif choice == "5":
            print("\nExiting... Stay secure!")
            break
        
        else:
            print("\nInvalid option. Please try again.")


if __name__ == "__main__":
    interactive_menu()