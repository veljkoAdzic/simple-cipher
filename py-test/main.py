
from utils import get_taps, calulate_needed_bit_length, prittify_decoded_text
from lsfr import Cipher
from scrambler import encode_text, decode_text

ALPHABET = '-ABCDEFGHIJKLMNOPQRSTUVWXYZ_.,!?0123456789;@%&*'

if __name__ == '__main__':
    bit_length = calulate_needed_bit_length(ALPHABET)

    encode = input("Select mode [e/d]: ").lower() == 'e'
    
    if encode:    
        seed = int(input("Input starting seed: "))

        if  2 > bit_length > 10 :
            print("no <3")
            exit()

        taps = get_taps(bit_length, seed)

        print(f"LSFR with seed={seed} taps={taps} and bit_length={bit_length} GIVES:")

        engine = Cipher(seed, taps, bit_length)

        text = input("Input text to encode:\n")

        print(encode_text(engine, ALPHABET, text, seed))
    else:
        text = input("Input text to decode:\n")
        print("\n")
        
        raw_decoded = decode_text(ALPHABET, bit_length, text)
        decoded = prittify_decoded_text(raw_decoded)
        print("\nDecoded:\n " + decoded)
