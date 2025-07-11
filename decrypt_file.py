import argparse
import sys
from des import DES

def main():
    parser = argparse.ArgumentParser(description="Decrypt a file using DES (ECB mode).")
    parser.add_argument("-k", "--key", required=True, help="8-byte DES key.")
    parser.add_argument("encrypted_filename", help="Path to the encrypted input file.")
    parser.add_argument("decrypted_filename", help="Path to the output file for decrypted content.")
    parser.add_argument("--debug", action="store_true", help="Enable debug output for intermediate values.")

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
        des = DES(args.key.encode('latin-1').decode('latin-1'), debug_mode=args.debug)
        
        encrypted_str = encrypted_data.decode('latin-1')
        decrypted_str = des.decrypt_ecb(encrypted_str)

        # For this specific test, we assume no padding and exactly 8 bytes.
        decrypted_data = decrypted_str.encode('latin-1')

        with open(args.decrypted_filename, 'wb') as f_out:
            f_out.write(decrypted_data)
        
        print(f"File '{args.encrypted_filename}' decrypted to '{args.decrypted_filename}' successfully.")

    except Exception as e:
        print(f"Error during decryption: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
