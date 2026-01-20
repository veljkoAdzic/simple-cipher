from lsfr import Cipher
from utils import generate_shuffled_alphabet
from utils import normalise_text_for_encoding, style_encoded_output, generate_marker
from utils import extract_metadata, get_taps, normalise_text_for_decoding, validate_checksum, validate_checksum_verbose
BLOCK_SIZE = 8

def encode_text(engine:Cipher, alphabet:str, text:str, seed:int) -> str:
    scrambled = generate_shuffled_alphabet(engine, alphabet)

    norm = normalise_text_for_encoding(text, BLOCK_SIZE)

    res = ""

    for i in range(0, len(norm), BLOCK_SIZE):
        offset = engine.nextStep()

        for j in range(BLOCK_SIZE):
            og_ind = alphabet.find(norm[i + j], 1)

            if og_ind > 0:
                new_ind = (og_ind + offset) % (len(scrambled)-1) + 1
            else:
                new_ind = 0

            res = res + scrambled[new_ind]

    return style_encoded_output(engine, res) + generate_marker(norm, alphabet, seed, BLOCK_SIZE)

def decode_text(alphabet:str, bit_length:int, text:str) -> str:
    txt, metadata = text.split(":", 1)

    cheksum, seed = extract_metadata(metadata, alphabet)
    taps = get_taps(bit_length, seed)

    print(f"LSFR with seed={seed} taps={taps} and bit_length={bit_length} GIVES:")

    engine = Cipher(seed, taps, bit_length)
    #==========================================================#
    scrambled = generate_shuffled_alphabet(engine, alphabet)

    norm = normalise_text_for_decoding(txt, BLOCK_SIZE)
    res = ''

    for i in range(0, len(norm), BLOCK_SIZE):
        offset = engine.nextStep()

        for j in range(BLOCK_SIZE):
            og_ind = scrambled.find(norm[i + j], 1)

            if og_ind > 0:
                new_ind = (len(scrambled)-1 + og_ind - offset-2) % (len(scrambled)-1) + 1
            else:
                new_ind = 0

            res = res + alphabet[new_ind]

    valid, checksum_errors, bad_range = validate_checksum_verbose(res, cheksum, alphabet, BLOCK_SIZE)

    if not valid:
        print("[WARNING]: Checksum is invalid, content may be modified")
        err_indicator = list("-"*BLOCK_SIZE)
        for ind in checksum_errors:
            err_indicator[ind] = "v"
        
        bad_part = res[bad_range[0]:bad_range[1]]

        err_indicator = "".join(err_indicator)
        marker = err_indicator * (len(bad_part) // BLOCK_SIZE)

        print( marker )
        print(bad_part)

        

    return res