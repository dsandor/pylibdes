
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
# This will be applied to the 64-bit block formed by (L << 32) | R
# The C code applies this using PERM_OP macros on the two 32-bit halves.
IP = [
    (4, 0x0f0f0f0f), # PERM_OP(r,l,tt, 4,0x0f0f0f0fL)
    (16, 0x0000ffff), # PERM_OP(l,r,tt,16,0x0000ffffL)
    (2, 0x33333333), # PERM_OP(r,l,tt, 2,0x33333333L)
    (8, 0x00ff00ff), # PERM_OP(l,r,tt, 8,0x00ff00ffL)
    (1, 0x55555555)  # PERM_OP(r,l,tt, 1,0x55555555L)
]

# Final Permutation
# This will be applied to the 64-bit block formed by (R << 32) | L
# The C code applies this using PERM_OP macros on the two 32-bit halves.
FP = [
    (1, 0x55555555), # PERM_OP(l,r,tt, 1,0x55555555L)
    (8, 0x00ff00ff), # PERM_OP(r,l,tt, 8,0x00ff00ffL)
    (2, 0x33333333), # PERM_OP(l,r,tt, 2,0x33333333L)
    (16, 0x0000ffff), # PERM_OP(r,l,tt,16,0x0000ffffL)
    (4, 0x0f0f0f0f)  # PERM_OP(l,r,tt, 4,0x0f0f0f0fL)
]

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

# From podd.h
odd_parity = [
  1,  1,  2,  2,  4,  4,  7,  7,  8,  8, 11, 11, 13, 13, 14, 14,
 16, 16, 19, 19, 21, 21, 22, 22, 25, 25, 26, 26, 28, 28, 31, 31,
 32, 32, 35, 35, 37, 37, 38, 38, 41, 41, 42, 42, 44, 44, 47, 47,
 49, 49, 50, 50, 52, 52, 55, 55, 56, 56, 59, 59, 61, 61, 62, 62,
 64, 64, 67, 67, 69, 69, 70, 70, 73, 73, 74, 74, 76, 76, 79, 79,
 81, 81, 82, 82, 84, 84, 87, 87, 88, 88, 91, 91, 93, 93, 94, 94,
 97, 97, 98, 98,100,100,103,103,104,104,107,107,109,109,110,110,
112,112,115,115,117,117,118,118,121,121,122,122,124,124,127,127,
128,128,131,131,133,133,134,134,137,137,138,138,140,140,143,143,
145,145,146,146,148,148,151,151,152,152,155,155,157,157,158,158,
161,161,162,162,164,164,167,167,168,168,171,171,173,173,174,174,
176,176,179,179,181,181,182,182,185,185,186,186,188,188,191,191,
193,193,194,194,196,196,199,199,200,200,203,203,205,205,206,206,
208,208,211,211,213,213,214,214,217,217,218,218,220,220,223,223,
224,224,227,227,229,229,230,230,233,233,234,234,236,236,239,239,
241,241,242,242,244,244,247,247,248,248,251,251,253,253,254,254]

# From sk.h
des_skb = [
[0x00000000,0x00000010,0x20000000,0x20000010,0x00010000,0x00010010,0x20010000,0x20010010,0x00000800,0x00000810,0x20000800,0x20000810,0x00010800,0x00010810,0x20010800,0x20010810,0x00000020,0x00000030,0x20000020,0x20000030,0x00010020,0x00010030,0x20010020,0x20010030,0x00000820,0x00000830,0x20000820,0x20000830,0x00010820,0x00010830,0x20010820,0x20010830,0x00080000,0x00080010,0x20080000,0x20080010,0x00090000,0x00090010,0x20090000,0x20090010,0x00080800,0x00080810,0x20080800,0x20080810,0x00090800,0x00090810,0x20090800,0x20090810,0x00080020,0x00080030,0x20080020,0x20080030,0x00090020,0x00090030,0x20090020,0x20090030,0x00080820,0x00080830,0x20080820,0x20080830,0x00090820,0x00090830,0x20090820,0x20090830,],
[0x00000000,0x02000000,0x00002000,0x02002000,0x00200000,0x02200000,0x00202000,0x02202000,0x00000004,0x02000004,0x00002004,0x02002004,0x00200004,0x02200004,0x00202004,0x02202004,0x00000400,0x02000400,0x00002400,0x02002400,0x00200400,0x02200400,0x00202400,0x02202400,0x00000404,0x02000404,0x00002404,0x02002404,0x00200404,0x02200404,0x00202404,0x02202404,0x10000000,0x12000000,0x10002000,0x12002000,0x10200000,0x12200000,0x10202000,0x12202000,0x10000004,0x12000004,0x10002004,0x12002004,0x10200004,0x12200004,0x10202004,0x12202004,0x10000400,0x12000400,0x10002400,0x12002400,0x10200400,0x12200400,0x10202400,0x12202400,0x10000404,0x12000404,0x10002404,0x12002404,0x10200404,0x12200404,0x10202404,0x12202404,],
[0x00000000,0x00000001,0x00040000,0x00040001,0x01000000,0x01000001,0x01040000,0x01040001,0x00000002,0x00000003,0x00040002,0x00040003,0x01000002,0x01000003,0x01040002,0x01040003,0x00000200,0x00000201,0x00040200,0x00040201,0x01000200,0x01000201,0x01040200,0x01040201,0x00000202,0x00000203,0x00040202,0x00040203,0x01000202,0x01000203,0x01040202,0x01040203,0x08000000,0x08000001,0x08040000,0x08040001,0x09000000,0x09000001,0x09040000,0x09040001,0x08000002,0x08000003,0x08040002,0x08040003,0x09000002,0x09000003,0x09040002,0x09040003,0x08000200,0x08000201,0x08040200,0x08040201,0x09000200,0x09000201,0x09040200,0x09040201,0x08000202,0x08000203,0x08040202,0x08040203,0x09000202,0x09000203,0x09040202,0x09040203,],
[0x00000000,0x00100000,0x00000100,0x00100100,0x00000008,0x00100008,0x00000108,0x00100108,0x00001000,0x00101000,0x00001100,0x00101100,0x00001008,0x00101008,0x00001108,0x00101108,0x04000000,0x04100000,0x04000100,0x04100100,0x04000008,0x04100008,0x04000108,0x04100108,0x04001000,0x04101000,0x04001100,0x04101100,0x04001008,0x04101008,0x04001108,0x04101108,0x00020000,0x00120000,0x00020100,0x00120100,0x00020008,0x00120008,0x00020108,0x00120108,0x00021000,0x00121000,0x00021100,0x00121100,0x00021008,0x00121008,0x00021108,0x00121108,0x04020000,0x04120000,0x04020100,0x04120100,0x04020008,0x04120008,0x04020108,0x04120108,0x04021000,0x04121000,0x04021100,0x04121100,0x04021008,0x04121008,0x04021108,0x04121108,],
[0x00000000,0x10000000,0x00010000,0x10010000,0x00000004,0x10000004,0x00010004,0x10010004,0x20000000,0x30000000,0x20010000,0x30010000,0x20000004,0x30000004,0x20010004,0x30010004,0x00100000,0x10100000,0x00110000,0x10110000,0x00100004,0x10100004,0x00110004,0x10110004,0x20100000,0x30100000,0x20110000,0x30110000,0x20100004,0x30100004,0x20110004,0x30110004,0x00001000,0x10001000,0x00011000,0x10011000,0x00001004,0x10001004,0x00011004,0x10011004,0x20001000,0x30001000,0x20011000,0x30011000,0x20001004,0x30001004,0x20011004,0x30011004,0x00101000,0x10101000,0x00111000,0x10111000,0x00101004,0x10101004,0x00111004,0x10111004,0x20101000,0x30101000,0x20111000,0x30111000,0x20101004,0x30101004,0x20111004,0x30111004,],
[0x00000000,0x08000000,0x00000008,0x08000008,0x00000400,0x08000400,0x00000408,0x08000408,0x00020000,0x08020000,0x00020008,0x08020008,0x00020400,0x08020400,0x00020408,0x08020408,0x00000001,0x08000001,0x00000009,0x08000009,0x00000401,0x08000401,0x00000409,0x08000409,0x00020001,0x08020001,0x00020009,0x08020009,0x00020401,0x08020401,0x00020409,0x08020409,0x02000000,0x0A000000,0x02000008,0x0A000008,0x02000400,0x0A000400,0x02000408,0x0A000408,0x02020000,0x0A020000,0x02020008,0x0A020008,0x02020400,0x0A020400,0x02020408,0x0A020408,0x02000001,0x0A000001,0x02000009,0x0A000009,0x02000401,0x0A000401,0x02000409,0x0A000409,0x02020001,0x0A020001,0x02020009,0x0A020009,0x02020401,0x0A020401,0x02020409,0x0A020409,],
[0x00000000,0x00000100,0x00080000,0x00080100,0x01000000,0x01000100,0x01080000,0x01080100,0x00000010,0x00000110,0x00080010,0x00080110,0x01000010,0x01000110,0x01080010,0x01080110,0x00200000,0x00200100,0x00280000,0x00280100,0x01200000,0x01200100,0x01280000,0x01280100,0x00200010,0x00200110,0x00280010,0x00280110,0x01200010,0x01200110,0x01280010,0x01280110,0x00000200,0x00000300,0x00080200,0x00080300,0x01000200,0x01000300,0x01080200,0x01080300,0x00000210,0x00000310,0x00080210,0x00080310,0x01000210,0x01000310,0x01080210,0x01080310,0x00200200,0x00200300,0x00280200,0x00280300,0x01200200,0x01200300,0x01280200,0x01280300,0x00200210,0x00200310,0x00280210,0x00280310,0x01200210,0x01200310,0x01280210,0x01280310,],
[0x00000000,0x04000000,0x00040000,0x04040000,0x00000002,0x04000002,0x00040002,0x04040002,0x00002000,0x04002000,0x00042000,0x04042000,0x00002002,0x04002002,0x00042002,0x04042002,0x00000020,0x04000020,0x00040020,0x04040020,0x00000022,0x04000022,0x00040022,0x04040022,0x00002020,0x04002020,0x00042020,0x04042020,0x00002022,0x04002022,0x00042022,0x04042022,0x00000800,0x04000800,0x00040800,0x04040800,0x00000802,0x04000802,0x00040802,0x04040802,0x00002800,0x04002800,0x00042800,0x04042800,0x00002802,0x04002802,0x00042802,0x04042802,0x00000820,0x04000820,0x00040820,0x04040820,0x00000822,0x04000822,0x00040822,0x04040822,0x00002820,0x04002820,0x00042820,0x04042820,0x00002822,0x04002822,0x00042822,0x04042822,]]

class DES:
    def __init__(self, key_str, debug_mode=False):
        # Convert key string to 8-byte des_cblock (bytearray) using C's des_string_to_key logic
        self.key_cblock = self._des_string_to_key(key_str)
        self.subkeys = self._generate_subkeys()
        self.debug_mode = debug_mode
        if self.debug_mode:
            self._debug_print_subkeys()

    def _debug_print_subkeys(self):
        print("Generated Subkeys (Python):")
        for i in range(0, len(self.subkeys), 2):
            print(f"  Subkey {i//2 + 1}: L={hex(self.subkeys[i])}, R={hex(self.subkeys[i+1])}")

    def _des_set_odd_parity(self, key_cblock):
        # Mimics C's des_set_odd_parity
        for i in range(8):
            key_cblock[i] = odd_parity[key_cblock[i]]
        return key_cblock

    def _des_string_to_key(self, s):
        # Mimics C's des_string_to_key (MIT COMPATIBLE part)
        key = bytearray(8)
        length = len(s)

        for i in range(length):
            j = ord(s[i])
            if (i % 16) < 8:
                key[i % 8] ^= (j << 1)
            else:
                # Reverse the bit order
                j = ((j << 4) & 0xF0) | ((j >> 4) & 0x0F)
                j = ((j << 2) & 0xCC) | ((j >> 2) & 0x33)
                j = ((j << 1) & 0xAA) | ((j >> 1) & 0x55)
                key[7 - (i % 8)] ^= j
        
        return self._des_set_odd_parity(key)

    def _string_to_longs(self, s):
        # Converts an 8-byte string into two 32-bit DES_LONGs (little-endian)
        # Mimics C's c2l macro
        l0 = (ord(s[3]) << 24) | (ord(s[2]) << 16) | (ord(s[1]) << 8) | ord(s[0])
        l1 = (ord(s[7]) << 24) | (ord(s[6]) << 16) | (ord(s[5]) << 8) | ord(s[4])
        return l0, l1

    def _longs_to_string(self, l0, l1):
        # Converts two 32-bit DES_LONGs back into an 8-byte string (little-endian)
        # Mimics C's l2c macro
        s = bytearray(8)
        s[0] = (l0) & 0xff
        s[1] = (l0 >> 8) & 0xff
        s[2] = (l0 >> 16) & 0xff
        s[3] = (l0 >> 24) & 0xff
        s[4] = (l1) & 0xff
        s[5] = (l1 >> 8) & 0xff
        s[6] = (l1 >> 16) & 0xff
        s[7] = (l1 >> 24) & 0xff
        return s.decode('latin-1') # Use latin-1 for direct byte mapping

    def _perm_op(self, a, b, n, m):
        # Translates C's PERM_OP macro: ((t)=((((a)>>(n))^(b))&(m)), (b)^=(t), (a)^=((t)<<(n)))
        t = (((a >> n) ^ b) & m)
        b ^= t
        a ^= (t << n)
        return a, b

    def _hperm_op(self, a, n, m):
        # Translates C's HPERM_OP macro: ((t)=((((a)<<(16-(n)))^(a))&(m)), (a)=(a)^(t)^(t>>(16-(n))))
        t = (((a << (16 - n)) ^ a) & m)
        a = a ^ t ^ (t >> (16 - n))
        return a

    def _rotate(self, val, n):
        # Mimics C's ROTATE macro for 32-bit integers
        return ((val >> n) | (val << (32 - n))) & 0xFFFFFFFF

    def _generate_subkeys(self):
        # Mimics C's des_set_key function
        schedule = [0] * 32 # des_key_schedule is an array of 16 DES_LONGs (32 bytes)
        
        # Convert 8-byte key_cblock to two DES_LONGs
        c, d = self._string_to_longs(self.key_cblock.decode('latin-1'))

        # PC1 permutation (from set_key.c)
        c, d = self._perm_op(d, c, 4, 0x0f0f0f0f)
        c = self._hperm_op(c, -2, 0xcccc0000)
        d = self._hperm_op(d, -2, 0xcccc0000)
        c, d = self._perm_op(d, c, 1, 0x55555555)
        d, c = self._perm_op(c, d, 8, 0x00ff00ff)
        c, d = self._perm_op(d, c, 1, 0x55555555)

        d = (((d & 0x000000ff) << 16) | (d & 0x0000ff00) |
             ((d & 0x00ff0000) >> 16) | ((c & 0xf0000000) >> 4))
        c &= 0x0fffffff

        shifts2 = [0,0,1,1,1,1,1,1,0,1,1,1,1,1,1,0]

        k_idx = 0
        for i in range(16):
            if shifts2[i]:
                c = ((c >> 2) | (c << 26)) & 0x0fffffff
                d = ((d >> 2) | (d << 26)) & 0x0fffffff
            else:
                c = ((c >> 1) | (c << 27)) & 0x0fffffff
                d = ((d >> 1) | (d << 27)) & 0x0fffffff
            
            s = (des_skb[0][ (c    )&0x3f                ]|
                 des_skb[1][((c>> 6)&0x03)|((c>> 7)&0x3c)]|
                 des_skb[2][((c>>13)&0x0f)|((c>>14)&0x30)]|
                 des_skb[3][((c>>20)&0x01)|((c>>21)&0x06) |
                             ((c>>22)&0x38)])
            t = (des_skb[4][ (d    )&0x3f                ]|
                 des_skb[5][((d>> 7)&0x03)|((d>> 8)&0x3c)]|
                 des_skb[6][ (d>>15)&0x3f                ]|
                 des_skb[7][((d>>21)&0x0f)|((d>>22)&0x30)])

            t2 = ((t << 16) | (s & 0x0000ffff)) & 0xffffffff
            schedule[k_idx] = self._rotate(t2, 30)
            k_idx += 1

            t2 = ((s >> 16) | (t & 0xffff0000))
            schedule[k_idx] = self._rotate(t2, 26)
            k_idx += 1
        
        return schedule

    def _des_f_function(self, R, S_idx_val, S_idx_val_plus_1):
        # This is the core F-function logic from D_ENCRYPT macro
        # R is the right half of the data block
        # S_idx_val and S_idx_val_plus_1 are the two subkey values for this round

        u = R ^ S_idx_val
        t = R ^ S_idx_val_plus_1

        t = self._rotate(t, 4)

        result = (
            des_skb[0][(u >> 2) & 0x3f] ^
            des_skb[2][(u >> 10) & 0x3f] ^
            des_skb[4][(u >> 18) & 0x3f] ^
            des_skb[6][(u >> 26) & 0x3f] ^
            des_skb[1][(t >> 2) & 0x3f] ^
            des_skb[3][(t >> 10) & 0x3f] ^
            des_skb[5][(t >> 18) & 0x3f] ^
            des_skb[7][(t >> 26) & 0x3f]
        )
        return result

    def _crypt(self, block_str, decrypt=False):
        l, r = self._string_to_longs(block_str)

        # Initial Permutation (IP) - Directly translated from C's IP macro
        # PERM_OP(r,l,tt, 4,0x0f0f0f0fL);
        l, r = self._perm_op(r, l, 4, 0x0f0f0f0f)
        # PERM_OP(l,r,tt,16,0x0000ffffL);
        r, l = self._perm_op(l, r, 16, 0x0000ffff)
        # PERM_OP(r,l,tt, 2,0x33333333L);
        l, r = self._perm_op(r, l, 2, 0x33333333)
        # PERM_OP(l,r,tt, 8,0x00ff00ffL);
        r, l = self._perm_op(l, r, 8, 0x00ff00ff)
        # PERM_OP(r,l,tt, 1,0x55555555L);
        l, r = self._perm_op(r, l, 1, 0x55555555)

        # Initial rotate as per C code in des_enc.c
        l = self._rotate(l, 29)
        r = self._rotate(r, 29)

        # Main DES rounds
        if decrypt:
            # Decryption rounds (reverse order of subkeys and operations)
            for i in range(30, -1, -2):
                f_result = self._des_f_function(r, self.subkeys[i], self.subkeys[i+1])
                l, r = r, l ^ f_result
                if self.debug_mode:
                    print(f"PYTHON_DEBUG: Round {16 - (i//2)}, L={hex(l)}, R={hex(r)}, u_val={hex(r ^ self.subkeys[i])}, t_val={hex(r ^ self.subkeys[i+1])}, f_result={hex(f_result)}")

        else:
            # Encryption rounds
            for i in range(0, 32, 2):
                f_result = self._des_f_function(r, self.subkeys[i], self.subkeys[i+1])
                l, r = r, l ^ f_result
                if self.debug_mode:
                    print(f"PYTHON_DEBUG: Round {i//2 + 1}, L={hex(l)}, R={hex(r)}, u_val={hex(r ^ self.subkeys[i])}, t_val={hex(r ^ self.subkeys[i+1])}, f_result={hex(f_result)}")

        # Final swap after all rounds (this is part of the DES algorithm)
        l, r = r, l

        # Final rotate as per C code in des_enc.c
        l = self._rotate(l, 3)
        r = self._rotate(r, 3)

        # Final Permutation (FP) - Directly translated from C's FP macro
        # PERM_OP(l,r,tt, 1,0x55555555L);
        r, l = self._perm_op(l, r, 1, 0x55555555)
        # PERM_OP(r,l,tt, 8,0x00ff00ffL);
        l, r = self._perm_op(r, l, 8, 0x00ff00ff)
        # PERM_OP(l,r,tt, 2,0x33333333L);
        r, l = self._perm_op(l, r, 2, 0x33333333)
        # PERM_OP(l,r,tt,16,0x0000ffffL);
        l, r = self._perm_op(r, l, 16, 0x0000ffff)
        # PERM_OP(l,r,tt, 4,0x0f0f0f0fL);
        r, l = self._perm_op(l, r, 4, 0x0f0f0f0f)

        return self._longs_to_string(l, r)

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
        ciphertext = ""
        prev_block = iv
        for i in range(0, len(plaintext), 8):
            block = plaintext[i:i+8]
            
            # Convert block and prev_block to longs for XORing
            block_l, block_r = self._string_to_longs(block)
            prev_block_l, prev_block_r = self._string_to_longs(prev_block)

            xored_l = block_l ^ prev_block_l
            xored_r = block_r ^ prev_block_r
            
            xored_block_str = self._longs_to_string(xored_l, xored_r)
            
            encrypted_block = self._crypt(xored_block_str)
            ciphertext += encrypted_block
            prev_block = encrypted_block
        return ciphertext

    def decrypt_cbc(self, ciphertext, iv):
        plaintext = ""
        prev_block = iv
        for i in range(0, len(ciphertext), 8):
            block = ciphertext[i:i+8]
            decrypted_block_str = self._crypt(block, decrypt=True)
            
            # Convert decrypted_block_str and prev_block to longs for XORing
            decrypted_l, decrypted_r = self._string_to_longs(decrypted_block_str)
            prev_block_l, prev_block_r = self._string_to_longs(prev_block)

            xored_l = decrypted_l ^ prev_block_l
            xored_r = decrypted_r ^ prev_block_r
            
            plaintext_block = self._longs_to_string(xored_l, xored_r)
            
            plaintext += plaintext_block
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
            
            block_l, block_r = self._string_to_longs(block)
            encrypted_l, encrypted_r = self._string_to_longs(encrypted_block)
            
            xored_l = block_l ^ encrypted_l
            xored_r = block_r ^ encrypted_r
            
            xored_block_str = self._longs_to_string(xored_l, xored_r)
            
            ciphertext += xored_block_str
            prev_block = xored_block_str
        return ciphertext

    def decrypt_cfb(self, ciphertext, iv):
        plaintext = ""
        prev_block = iv
        for i in range(0, len(ciphertext), 8):
            block = ciphertext[i:i+8]
            encrypted_block = self._crypt(prev_block)
            
            block_l, block_r = self._string_to_longs(block)
            encrypted_l, encrypted_r = self._string_to_longs(encrypted_block)
            
            xored_l = block_l ^ encrypted_l
            xored_r = block_r ^ encrypted_r
            
            plaintext_block = self._longs_to_string(xored_l, xored_r)
            
            plaintext += plaintext_block
            prev_block = block
        return plaintext

    def encrypt_ofb(self, plaintext, iv):
        ciphertext = ""
        prev_block = iv
        for i in range(0, len(plaintext), 8):
            block = plaintext[i:i+8]
            encrypted_block = self._crypt(prev_block)
            
            block_l, block_r = self._string_to_longs(block)
            encrypted_l, encrypted_r = self._string_to_longs(encrypted_block)
            
            xored_l = block_l ^ encrypted_l
            xored_r = block_r ^ encrypted_r
            
            xored_block_str = self._longs_to_string(xored_l, xored_r)
            
            ciphertext += xored_block_str
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
            
            block_l, block_r = self._string_to_longs(block)
            current_iv_l, current_iv_r = self._string_to_longs(current_iv)
            
            xored_block_l = block_l ^ current_iv_l
            xored_block_r = block_r ^ current_iv_r
            
            xored_block_str = self._longs_to_string(xored_block_l, xored_block_r)
            
            encrypted_block = self._crypt(xored_block_str)
            ciphertext += encrypted_block
            
            encrypted_l, encrypted_r = self._string_to_longs(encrypted_block)
            
            current_iv_l = block_l ^ encrypted_l
            current_iv_r = block_r ^ encrypted_r
            current_iv = self._longs_to_string(current_iv_l, current_iv_r)
        return ciphertext

    def decrypt_pcbc(self, ciphertext, iv):
        plaintext = ""
        current_iv = iv
        for i in range(0, len(ciphertext), 8):
            block = ciphertext[i:i+8]
            decrypted_block_str = self._crypt(block, decrypt=True)
            
            decrypted_l, decrypted_r = self._string_to_longs(decrypted_block_str)
            current_iv_l, current_iv_r = self._string_to_longs(current_iv)
            
            plaintext_block_l = decrypted_l ^ current_iv_l
            plaintext_block_r = decrypted_r ^ current_iv_r
            
            plaintext_block = self._longs_to_string(plaintext_block_l, plaintext_block_r)
            plaintext += plaintext_block
            
            block_l, block_r = self._string_to_longs(block)
            
            current_iv_l = plaintext_block_l ^ block_l
            current_iv_r = plaintext_block_r ^ block_r
            current_iv = self._longs_to_string(current_iv_l, current_iv_r)

        # Remove padding
        padding_len = ord(plaintext[-1])
        return plaintext[:-padding_len]
