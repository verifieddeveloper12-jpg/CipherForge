A professional grade encryption tool with multi-layer encryption, compression, and integrity verification.

![Python Version] 3.7+

![License] Free to use, modify, and distribute

![Status] Active & Production Ready - Zero dependencies, fully functional encryption tool

**Author**: Original work - Not forked, copied, or skidded from any source  

**Created**: 2025

**Type**: 100% Original Implementation

Features

Multi-layer encryption with configurable rounds (1-10 layers)  

Built-in zlib compression for smaller encrypted outputs  

MD5 checksum verification ensures data integrity  

SHA-256 password-based key derivation  

Support for both text and file encryption  

Interactive command-line interface  

Embedded metadata in encrypted output

Installation

git clone https://github.com/yourusername/CipherForge.git

cd CipherForge

python main.py

Usage

Interactive Mode

python main.py

Programmatic Usage

python

from main import AdvancedEncryptor

encryptor = AdvancedEncryptor(

    password="your_secure_password",

    compression_level=9,

    encryption_rounds=3

)

encrypted = encryptor.encrypt("Secret message", use_compression=True)

decrypted = encryptor.decrypt(encrypted)

encryptor.encrypt_file("document.txt", "document.encrypted")

encryptor.decrypt_file("document.encrypted", "document.decrypted")

Password gets hashed with SHA-256 to create encryption seed  

Pseudo-random substitution cipher keys generated per round  

Optional zlib compression applied before encryption  

Text passes through multiple substitution layers  

MD5 checksum added for integrity verification  

Metadata embedded with encryption settings

password: Your encryption password (string)  

compression_level: 0-9 (default: 9)  

encryption_rounds: 1-10 (default: 3)

Security Notes

Use strong, unique passwords for best security  

More encryption rounds provide stronger encryption  

Checksums detect data tampering  

Suitable for personal encryption needs  

For high-security applications, consider industry-standard algorithms

Original Work Statement

This project was designed and implemented from scratch. The encryption algorithm, architecture, and implementation are 100% original work. No code was copied, forked, or derived from existing projects. All logic and features were independently developed.