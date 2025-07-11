import argparse
import sys
from des import DES

def main():
    parser = argparse.ArgumentParser(description="Decrypt a file using DES (ECB mode).")
    parser.add_argument("-k", "--key", required=True, help="8-byte DES key.")
    parser.add_argument("encrypted_filename", help="Path to the encrypted input file.")
    parser.add_argument("decrypted_filename", help="Path to the output file for decrypted content.")

    args = parser.parse_args()

    if len(args.key) != 8:
        print("Error: Key must be exactly 8 bytes long.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.encrypted_filename, 'rb') as f_in:
            encrypted_data = f_in.read()
    except FileNotFoundError:
        print(f"Error: Encrypted file '{args.encrypted_filename}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading encrypted file: {e}", file=sys.stderr)
        sys.exit(1)

    # Convert bytes to string for DES class (assuming ASCII or similar for key and data)
    # The des.py script expects string input for _string_to_bits
    # For binary data, we need to handle it carefully.
    # The current des.py implementation converts string to bits, then bits to string.
    # It's designed for text. For arbitrary binary data, we need to ensure
    # the byte values are preserved through the string conversion.
    # A simple way is to use latin-1 encoding which maps byte values directly to unicode codepoints 0-255.
    
    try:
        des = DES(args.key.encode('latin-1').decode('latin-1')) # Key as string
        
        # Decrypt in chunks if file is large, or all at once if small.
        # The des.py decrypt_ecb expects a string.
        # We need to convert the bytes read from file to a string that can be
        # converted back to bytes without loss. latin-1 is suitable for this.
        encrypted_str = encrypted_data.decode('latin-1')
        decrypted_str = des.decrypt_ecb(encrypted_str)
        decrypted_data = decrypted_str.encode('latin-1')

        with open(args.decrypted_filename, 'wb') as f_out:
            f_out.write(decrypted_data)
        
        print(f"File '{args.encrypted_filename}' decrypted to '{args.decrypted_filename}' successfully.")

    except Exception as e:
        print(f"Error during decryption: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
