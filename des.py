
# Conversion of the C code to Python

# DES constants
# Permutation choice 1
PC1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]

# Permutation choice 2
PC2 = [14, 17, 11, 24, 1, 5,
       3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8,
       16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55,
       30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53,
       46, 42, 50, 36, 29, 32]

# Initial Permutation
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

# Final Permutation
FP = [40, 8, 48, 16, 56, 24, 64, 32,
      39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30,
      37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28,
      35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26,
      33, 1, 41, 9, 49, 17, 57, 25]

# Expansion D-box
E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

# S-boxes
S_BOX = [
    # S1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    # S2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    # S3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    # S4
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    # S5
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    # S6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    # S7
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    # S8
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]

# Permutation function
P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

# number of left shifts
SHIFT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

class DES:
    def __init__(self, key):
        self.key = key
        self.subkeys = self._generate_subkeys()

    def _string_to_bits(self, s):
        return [int(bit) for char in s for bit in bin(ord(char))[2:].zfill(8)]

    def _bits_to_string(self, b):
        return ''.join(chr(int(''.join(map(str, b[i:i+8])), 2)) for i in range(0, len(b), 8))

    def _permute(self, block, table):
        return [block[x-1] for x in table]

    def _xor(self, a, b):
        return [x ^ y for x, y in zip(a, b)]

    def _left_shift(self, bits, n):
        return bits[n:] + bits[:n]

    def _generate_subkeys(self):
        key_bits = self._string_to_bits(self.key)
        key_perm = self._permute(key_bits, PC1)

        left, right = key_perm[:28], key_perm[28:]

        subkeys = []
        for i in range(16):
            left = self._left_shift(left, SHIFT[i])
            right = self._left_shift(right, SHIFT[i])
            subkey = self._permute(left + right, PC2)
            subkeys.append(subkey)
        return subkeys

    def _s_box_lookup(self, bits):
        result = []
        for i in range(8):
            chunk = bits[i*6:(i+1)*6]
            row = int(str(chunk[0]) + str(chunk[5]), 2)
            col = int(''.join(map(str, chunk[1:5])), 2)
            result.extend(list(map(int, bin(S_BOX[i][row][col])[2:].zfill(4))))
        return result

    def _f_function(self, right, subkey):
        expanded = self._permute(right, E)
        xored = self._xor(expanded, subkey)
        s_box_out = self._s_box_lookup(xored)
        return self._permute(s_box_out, P)

    def _crypt(self, block, decrypt=False):
        block_bits = self._string_to_bits(block)
        permuted = self._permute(block_bits, IP)
        left, right = permuted[:32], permuted[32:]

        keys = self.subkeys[::-1] if decrypt else self.subkeys

        for subkey in keys:
            f_result = self._f_function(right, subkey)
            left, right = right, self._xor(left, f_result)

        # Swap one last time
        left, right = right, left

        return self._bits_to_string(self._permute(left + right, FP))

    def encrypt_ecb(self, plaintext):
        # Pad plaintext to be a multiple of 8 bytes
        padding_len = 8 - (len(plaintext) % 8)
        padding = chr(padding_len) * padding_len
        plaintext += padding

        ciphertext = ""
        for i in range(0, len(plaintext), 8):
            block = plaintext[i:i+8]
            ciphertext += self._crypt(block)
        return ciphertext

    def decrypt_ecb(self, ciphertext):
        plaintext = ""
        for i in range(0, len(ciphertext), 8):
            block = ciphertext[i:i+8]
            plaintext += self._crypt(block, decrypt=True)

        # Remove padding
        padding_len = ord(plaintext[-1])
        return plaintext[:-padding_len]

    def encrypt_cbc(self, plaintext, iv):
        # Pad plaintext to be a multiple of 8 bytes
        padding_len = 8 - (len(plaintext) % 8)
        padding = chr(padding_len) * padding_len
        plaintext += padding

        ciphertext = ""
        prev_block = iv
        for i in range(0, len(plaintext), 8):
            block = plaintext[i:i+8]
            xored_block = self._xor(self._string_to_bits(block), self._string_to_bits(prev_block))
            encrypted_block = self._crypt(self._bits_to_string(xored_block))
            ciphertext += encrypted_block
            prev_block = encrypted_block
        return ciphertext

    def decrypt_cbc(self, ciphertext, iv):
        plaintext = ""
        prev_block = iv
        for i in range(0, len(ciphertext), 8):
            block = ciphertext[i:i+8]
            decrypted_block_bits = self._string_to_bits(self._crypt(block, decrypt=True))
            xored_block = self._xor(decrypted_block_bits, self._string_to_bits(prev_block))
            plaintext += self._bits_to_string(xored_block)
            prev_block = block
        
        # Remove padding
        padding_len = ord(plaintext[-1])
        return plaintext[:-padding_len]

    def encrypt_cfb(self, plaintext, iv):
        ciphertext = ""
        prev_block = iv
        for i in range(0, len(plaintext), 8):
            block = plaintext[i:i+8]
            encrypted_block = self._crypt(prev_block)
            xored_block = self._xor(self._string_to_bits(block), self._string_to_bits(encrypted_block))
            ciphertext += self._bits_to_string(xored_block)
            prev_block = self._bits_to_string(xored_block)
        return ciphertext

    def decrypt_cfb(self, ciphertext, iv):
        plaintext = ""
        prev_block = iv
        for i in range(0, len(ciphertext), 8):
            block = ciphertext[i:i+8]
            encrypted_block = self._crypt(prev_block)
            xored_block = self._xor(self._string_to_bits(block), self._string_to_bits(encrypted_block))
            plaintext += self._bits_to_string(xored_block)
            prev_block = block
        return plaintext

    def encrypt_ofb(self, plaintext, iv):
        ciphertext = ""
        prev_block = iv
        for i in range(0, len(plaintext), 8):
            block = plaintext[i:i+8]
            encrypted_block = self._crypt(prev_block)
            xored_block = self._xor(self._string_to_bits(block), self._string_to_bits(encrypted_block))
            ciphertext += self._bits_to_string(xored_block)
            prev_block = encrypted_block
        return ciphertext

    def decrypt_ofb(self, ciphertext, iv):
        return self.encrypt_ofb(ciphertext, iv)  # OFB decryption is the same as encryption

    def encrypt_pcbc(self, plaintext, iv):
        # Pad plaintext to be a multiple of 8 bytes
        padding_len = 8 - (len(plaintext) % 8)
        padding = chr(padding_len) * padding_len
        plaintext += padding

        ciphertext = ""
        current_iv = iv
        for i in range(0, len(plaintext), 8):
            block = plaintext[i:i+8]
            xored_block_bits = self._xor(self._string_to_bits(block), self._string_to_bits(current_iv))
            encrypted_block = self._crypt(self._bits_to_string(xored_block_bits))
            ciphertext += encrypted_block
            current_iv_bits = self._xor(self._string_to_bits(block), self._string_to_bits(encrypted_block))
            current_iv = self._bits_to_string(current_iv_bits)
        return ciphertext

    def decrypt_pcbc(self, ciphertext, iv):
        plaintext = ""
        current_iv = iv
        for i in range(0, len(ciphertext), 8):
            block = ciphertext[i:i+8]
            decrypted_block_bits = self._string_to_bits(self._crypt(block, decrypt=True))
            plaintext_block_bits = self._xor(decrypted_block_bits, self._string_to_bits(current_iv))
            plaintext_block = self._bits_to_string(plaintext_block_bits)
            plaintext += plaintext_block
            current_iv_bits = self._xor(plaintext_block_bits, self._string_to_bits(block))
            current_iv = self._bits_to_string(current_iv_bits)

        # Remove padding
        padding_len = ord(plaintext[-1])
        return plaintext[:-padding_len]
