from math import ceil, log2
from lsfr import Cipher

GOOD_TAPS = {
    2: ( 0b11 ),
    3: ( 0b011 ),
    4: ( 0b0011 ),
    5: ( 0b00101, 0b10111, 0b11101, 0b11101 ),
    6: ( 0b000011, 0b100111, 0b101101 ),
    7: ( 0b0000011, 0b0001001, 0b0001111, 0b0011101,
         0b0111111, 0b1001011, 0b1010101, 0b1100101, 0b1110111 ),
    8: ( 0b00011101, 0b00101010, 0b01011111, 0b01100011,
         0b01100101, 0b01101001, 0b11000011, 0b11100111 ),
    9: ( 0b000010001, 0b000101101, 0b001011001, 0b001101111, 0b001110111,
         0b011011011, 0b100010011, 0b100110001, 0b101100001,
         0b101101011, 0b110000101, 0b110001111, 0b111100011, 0b111101001 ),
    10:( 0b0000001001, 0b0000011011, 0b0001101111, 0b0100001101, 0b0100011001,
         0b0100100011, 0b0100110001, 0b0111100101, 0b0111111011, 
         0b1000010011, 0b1001111111, 0b1101001101, 0b1101100011, 0b1111111001 )
}

ESCAPING_CHARACTERS={
    ":": "..",
}

def calulate_needed_bit_length(alphabet:str) -> int:
    return ceil( log2( len(alphabet) ) )


def get_taps(bits:int, seed:int):
    if bits not in GOOD_TAPS.keys():
        return 0

    taps = GOOD_TAPS[bits]
    return taps[ seed % len(taps) ]

def generate_shuffled_alphabet(engine:Cipher, aplhabet:str):
    al_len = len(aplhabet) -1
    scrambled = list(aplhabet)

    # shuffle characters from 1 to -1
    for i in range(1, al_len):
        cur = engine.nextStep() % (al_len-1)

        frame_len = al_len-i
        
        ind = cur if cur > i else ((cur % frame_len) + i)

        if ind == i: continue

        scrambled[i], scrambled[ind] = scrambled[ind], scrambled[i] 

    # last char shuffle
    ind = engine.nextStep() % (al_len-1) + 1
    scrambled[-1], scrambled[ind] = scrambled[ind], scrambled[-1] 

    return "".join(scrambled)


def normalise_text_for_encoding(text:str, block_size:int)->str:
    res = text
    for chr, esc in ESCAPING_CHARACTERS.items():
            res = res.replace(chr, esc)

    if len(res)%block_size != 0:
        res = res + "_"*( block_size - len(res)%block_size )

    return res.replace(" ", "_").upper()

def normalise_text_for_decoding(text:str, block_size:int)->str:
    return text.replace(" ", "").upper()

def style_encoded_output(eng:Cipher, txt:str)->str:
    res = ""
    cap = True
    count = eng.nextStream() & 0b1111 + 2

    for char in list(txt):

        if char.isalpha():
            res = res + ( char.upper() if cap else char.lower() )
            cap = False
        else:
            res = res + char
        
        if char in '.,;:!?':
            res = res + " "
            cap = cap or char in {'.' , ';', '!', '?'}
            count += 1
        elif count <= 0:
            res = res + " "
            count = eng.nextStream() & 0b1111 + 2
        else:
            count -= 1
        
    return res



"""
lrc := 0
for each byte b in the buffer do
    lrc := (lrc + b) and 0xFF
lrc := (((lrc XOR 0xFF) + 1) and 0xFF)
"""

def __generate_full_checksum(txt:str, alphabet:str, block_size:int):
    half_len = len(txt) // 2
    forth_len = len(txt) // 4 
    
    text = txt
    text2 = txt[:half_len]
    text4 = txt[:forth_len] + txt[half_len:(half_len+forth_len)]

    cf = __generate_checksum(text, alphabet, block_size)
    ch = __generate_checksum(text2, alphabet, block_size)
    cq = __generate_checksum(text4, alphabet, block_size)

    return cf + '-' + ch + '-' + cq

def __generate_checksum(txt:str, alphabet:str, block_size:int)->str:
    res = ""
    carry = 0

    for i in range(block_size-1, -1, -1):
        sum = carry
        for j in range(i, len(txt), block_size):
            sum += max(0, alphabet.find(txt[j]) )
        
        carry = sum // (len(alphabet)-1)
        sum = sum % (len(alphabet)-1)

        ind = ((len(alphabet)-1) - sum)
        res = alphabet[ind]  + res

    return res

def validate_checksum_verbose(txt: str, checksum: str, alphabet: str, block_size: int)-> tuple[bool, list[int], tuple[int]]:
    c_full, c_half, c_quart = checksum.split("-")

    """Validate checksum and report block-level errors."""
    block_errors = []

    carry = 0
    expected_chars = []

    for col in range(block_size - 1, -1, -1):
        s = carry
        
        for j in range(col, len(txt), block_size):
            s += max(0, alphabet.find(txt[j]))

        carry = s // (len(alphabet) - 1)
        s = s % (len(alphabet) - 1)

        ind = (len(alphabet) - 1) - s
        expected_char = alphabet[ind]
        expected_chars.append(expected_char)

        # Compare against provided checksum (mirrored position)
        actual = c_full[col]
        if actual != expected_char:
            block_errors.append(col)

    # no error found
    if len(block_errors) == 0:
        return len(block_errors) == 0, block_errors, ()

    # reduce what quadrant the error is in
    half_len = len(txt) // 2
    forth_len = len(txt) // 4 
    
    text_h = txt[:half_len]
    text_q = txt[:forth_len] + txt[half_len:(half_len+forth_len)]    

    half_correct = c_half == __generate_checksum(text_h, alphabet, block_size)
    qrtr_correct = c_quart == __generate_checksum(text_q, alphabet, block_size)
    
    if half_correct:
        bad_range = (half_len+forth_len, len(txt)) if qrtr_correct else (half_len, half_len+forth_len)
    else:
        bad_range = (forth_len, half_len) if qrtr_correct else (0, forth_len)

    lo_ind = (bad_range[0] // block_size)     * block_size
    hi_ind = (bad_range[1] // block_size + 1) * block_size
    
    return len(block_errors) == 0, block_errors, (lo_ind, hi_ind)

def __generate_seed_enc(seed:int, alphabet:str):
    res = ""

    tmp = seed
    cur = tmp % 10
    while tmp > 0:
        cur = tmp % 10
        tmp = tmp//10
        res = (alphabet[cur] if cur > 0 else '0') + res
    
    return res

def generate_marker(norm_txt:str, alphabet:str, seed:int, block_size:int)->str:
    return ":" + __generate_full_checksum(norm_txt, alphabet, block_size) + "-" + __generate_seed_enc(seed, alphabet)

def extract_metadata(metadata:str, alphabet:str):
    parts = metadata.split("-")
    checksum, seedstr = "-".join(parts[:-1]), parts[-1] 
    
    seed = 0
    for char in seedstr:
        cur = 0 if char == '0' else alphabet.find(char)
        seed = seed*10 + cur

    return checksum, max(1, seed) # seed should be 0!


def prittify_decoded_text(raw:str):
    res = raw.replace("_", " ")

    res = res.lower() 

    return res