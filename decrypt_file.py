import argparse
import sys
from des import DES

def main():
    parser = argparse.ArgumentParser(description="Decrypt a file using DES (ECB mode).")
    parser.add_argument("-k", "--key", required=True, help="8-byte DES key.")
    parser.add_argument("encrypted_filename", help="Path to the encrypted input file.")
    parser.add_argument("decrypted_filename", help="Path to the output file for decrypted content.")
    parser.add_argument("--no-padding", action="store_true", help="Do not remove padding after decryption. Use if the encrypted file was not padded or uses a different padding scheme.")

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

    try:
        des = DES(args.key.encode('latin-1').decode('latin-1'))
        
        encrypted_str = encrypted_data.decode('latin-1')
        decrypted_str = des.decrypt_ecb(encrypted_str)

        if args.no_padding:
            # If no_padding is specified, return the raw decrypted string as bytes
            decrypted_data = decrypted_str.encode('latin-1')
        else:
            # Otherwise, attempt to remove padding as per des.py's decrypt_ecb logic
            # The decrypt_ecb method already handles padding removal internally.
            # We just need to ensure the output is converted back to bytes.
            padding_len = ord(decrypted_str[-1])
            if 0 < padding_len <= 8:
                decrypted_data = decrypted_str[:-padding_len].encode('latin-1')
            else:
                # If padding_len is suspicious, it might indicate no padding or corrupt padding.
                # In this case, we'll just return the raw decrypted data and let the user decide.
                print("Warning: Padding length seems invalid. Returning raw decrypted data.", file=sys.stderr)
                decrypted_data = decrypted_str.encode('latin-1')

        with open(args.decrypted_filename, 'wb') as f_out:
            f_out.write(decrypted_data)
        
        print(f"File '{args.encrypted_filename}' decrypted to '{args.decrypted_filename}' successfully.")

    except Exception as e:
        print(f"Error during decryption: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()