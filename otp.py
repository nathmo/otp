import sys
import os
import random
import re
import math

def xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ k for b, k in zip(data, key)])

def read_text_file(filename: str) -> bytes:
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read().encode('utf-8')

def read_hex_file(filename: str) -> bytes:
    with open(filename, 'r') as f:
        content = f.read()
    hex_str = re.sub(r'\s+', '', content)
    if len(hex_str) % 2 != 0:
        print(f"Error: Hex data in '{filename}' has an odd number of characters.")
        sys.exit(1)
    try:
        return bytes.fromhex(hex_str)
    except ValueError:
        print(f"Error: '{filename}' contains invalid hex characters.")
        sys.exit(1)

def write_hex_file(filename: str, data: bytes):
    with open(filename, 'w') as f:
        f.write(data.hex().upper())

def write_text_file(filename: str, data: bytes):
    with open(filename, 'w', encoding='utf-8') as f:
        try:
            f.write(data.decode('utf-8'))
        except UnicodeDecodeError:
            print(f"Warning: Decrypted content may not be valid UTF-8.")
            f.write(data.decode('utf-8', errors='replace'))

def generate_random_bytes(length: int) -> bytes:
    return bytes([random.randint(0, 255) for _ in range(length)])

def list_current_files():
    print("Files in current folder are:")
    for fname in os.listdir('.'):
        if os.path.isfile(fname):
            print(f"  - {fname}")

def print_possible_grid_shapes(total_chars: int):
    print(f"Possible (lines, columns) for {total_chars} characters (with even columns):")
    found = False
    for cols in range(2, total_chars//2):  # only even columns
        if total_chars % cols == 0:
            rows = total_chars // cols
            print(f"  {rows} × {cols},  with size on paper of {rows*4} mm × {cols*4} mm")
            found = True
    if not found:
        print("  No even-column grid shape found.")
    print("With padding, the best square arrangements is : " + str(math.ceil(math.sqrt(total_chars))))
    print("and require a square with " + str(math.ceil(math.sqrt(total_chars)*4)) + " mm side")

def choose_file(prompt):
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    print(prompt)
    for i, f in enumerate(files):
        print(f"  {i}: {f}")
    while True:
        try:
            idx = int(input("Enter file number: "))
            if 0 <= idx < len(files):
                return files[idx]
            else:
                print("Invalid index. Try again.")
        except ValueError:
            print("Please enter a valid number.")


def main():
    print("simple XOR One time pad encryptor/decrypter")
    print("Usage:")
    print("  Encrypt: python otp.py encrypt input.txt [optional_pad.txt]")
    print("  Decrypt: python otp.py decrypt encrypted.txt pad.txt")
    print(" if no argument are provided or you run the .exe you will enter interactive mode.")
    
    if len(sys.argv) < 2:
        print("Mode not provided. Choose:")
        print("  0: Encrypt")
        print("  1: Decrypt")
        mode_input = input("Enter mode number: ").strip()
        mode = 'encrypt' if mode_input == '0' else 'decrypt'
        input_file = choose_file("Choose input file:")
        pad_file = choose_file("Choose One Time Pad file:")
    else:
        mode = sys.argv[1].lower()

    if mode not in ['encrypt', 'decrypt']:
        print("Mode must be 'encrypt' or 'decrypt'")
        sys.exit(1)

    if not os.path.isfile(input_file):
        print(f"File '{input_file}' not found.")
        list_current_files()
        sys.exit(1)

    if not os.path.isfile(input_file):
        print(f"File '{pad_file}' not found.")
        list_current_files()
        sys.exit(1)

    if mode == 'encrypt':
        data = read_text_file(input_file)

        if len(sys.argv) == 4:
            pad_file = sys.argv[3]
            if not os.path.isfile(pad_file):
                print(f"Pad file '{pad_file}' not found.")
                list_current_files()
                sys.exit(1)
            pad = read_hex_file(pad_file)
        else:
            pad = generate_random_bytes(len(data))

        if len(pad) != len(data):
            if len(pad) > len(data):
                print("Warning: Message is shorter than the pad. Padding message with 0x00.")
                print("This may indicate a retranscription error. Please verify both the message and the pad.")
                data += b'\x00' * (len(pad) - len(data))
            else:
                print("Warning: Pad is shorter than the message. Padding pad with 0x00.")
                print("This may indicate a retranscription error. Please verify both the pad and the message.")
                pad += b'\x00' * (len(data) - len(pad))

        encrypted = xor_bytes(data, pad)
        print_possible_grid_shapes(len(encrypted))
        write_hex_file("pad.txt", pad)
        write_hex_file("encrypted.txt", encrypted)
        print("Encryption complete. Files saved:")
        print("  pad.txt (hex)")
        print("  encrypted.txt (hex)")

    elif mode == 'decrypt':
        if len(sys.argv) != 4 and pad_file==None:
            print("Decrypt mode requires a pad file.")
            sys.exit(1)
        elif len(sys.argv) == 4:
            pad_file = sys.argv[3]

        encrypted = read_hex_file(input_file)
        pad = read_hex_file(pad_file)

        if len(pad) != len(encrypted):
            if len(pad) > len(encrypted):
                print("Warning: Encrypted message is shorter than the pad. Padding message with 0x00.")
                print("This may indicate a retranscription error. Please verify both files.")
                encrypted += b'\x00' * (len(pad) - len(encrypted))
            else:
                print("Warning: Pad is shorter than the encrypted message. Padding pad with 0x00.")
                print("This may indicate a retranscription error. Please verify both files.")
                pad += b'\x00' * (len(encrypted) - len(pad))

        decrypted = xor_bytes(encrypted, pad)
        write_text_file("decrypted.txt", decrypted)
        print("Decryption complete. Saved as 'decrypted.txt' (UTF-8 text).")

if __name__ == "__main__":
    main()
