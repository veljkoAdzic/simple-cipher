
"""
Pseudo code that the checksum is based of:

lrc := 0
for each byte b in the buffer do
    lrc := (lrc + b) and 0xFF
lrc := (((lrc XOR 0xFF) + 1) and 0xFF)
"""

def calulate_column(index:int, txt:str, alphabet:str, stride:int)->str:
    """
    Calculates the character of the checksum at `index`
    
    :param index: Index of character of the checksum, ie. the column 
    :type index: int
    :param txt: Text on which the cecksum is caluclated 
    :type txt: str
    :param alphabet: Character set avalable
    :type alphabet: str
    :param stride: Size of block, ie. the number of columns
    :type stride: int
    :return: Character from checksum at index
    :rtype: str
    """
    sum = 0
    base = len(alphabet)-1

    for j in range(index, len(txt), stride):
        sum += max(0, alphabet.find(txt[j]) )
    
    sum = sum % base

    ind = (base - sum)
    
    return alphabet[ind]

def generate_full_checksum(txt:str, alphabet:str, block_size:int):
    """
    Generates the full checksum that goes in the marker
    
    :param txt: Text from which to generate the checksum
    :type txt: str
    :param alphabet: Character set avalable
    :type alphabet: str
    :param block_size: Size of block
    :type block_size: int
    :return: Full checksum string
    :rtype: str
    """
    # half_len = len(txt) // 2
    # forth_len = len(txt) // 4 
    
    # text = txt
    # text2 = txt[:half_len]
    # text4 = txt[:forth_len] + txt[half_len:(half_len+forth_len)]

    # cf = __generate_checksum(text, alphabet, block_size)
    # ch = __generate_checksum(text2, alphabet, block_size)
    # cq = __generate_checksum(text4, alphabet, block_size)

    # return cf + '-' + ch + '-' + cq
    return __generate_checksum(txt, alphabet, block_size) + '-' + __generate_checksum(txt, alphabet, block_size+1)

def __generate_checksum(txt:str, alphabet:str, block_size:int)->str:
    """
    HELPER FUNCTION!\n
    Generate checksum from text
    
    :param txt: Text from which the checksum is generated
    :type txt: str
    :param alphabet: Character set avalable
    :type alphabet: str
    :param block_size: Size of blocks, ie. number of columns
    :type block_size: int
    :return: Checksum string
    :rtype: str
    """
    res = ""

    for i in range(block_size-1, -1, -1):
        res = calulate_column(i, txt, alphabet, block_size) + res

    return res

def validate_checksum_verbose(txt: str, checksum: str, alphabet: str, block_size: int)-> tuple[bool, list[int], tuple[int]]:
    """
    Validates the checksum and returns localised error
    
    :param txt: Decoded text to check checksum on
    :type txt: str
    :param checksum: Checksum from marker
    :type checksum: str
    :param alphabet: Character set avalable
    :type alphabet: str
    :param block_size: Size of blocks, ie. number of columns
    :type block_size: int
    :return: Tuple of (if checksum valid, column indexes of errors, error range in text) 
    :rtype: tuple[bool, list[int], tuple[int]]
    """    
    c1, c2 = checksum.split("-")

    block_errors_c1 = []
    block_errors_c2 = []

    for col in range(block_size - 1, -1, -1):
        calc_char = calulate_column(col, txt, alphabet, block_size)
        # Compare against provided checksum (mirrored position)
        if c1[col] != calc_char:
            block_errors_c1.append(col)

    for col in range(block_size, -1, -1):
        calc_char = calulate_column(col, txt, alphabet, block_size+1)
        if c2[col] != calc_char:
            block_errors_c2.append(col)

    # no error found
    if not block_errors_c1 and not block_errors_c2:
        return True, [], ()

    # bad checksum
    if not block_errors_c1 or not block_errors_c2:
        return True, [], ()    

    errors = set()
    txt_len = len(txt)

    for r1 in block_errors_c1:
     for r2 in block_errors_c2:
         for i in range(r1, txt_len, block_size):
            if i % (block_size+1) == r2:
                errors.add(i)
                break
    
    if len(errors) == 0:
        [errors.add(r1) for r1 in block_errors_c1]
        [errors.add(r2) for r2 in block_errors_c2]
    
    lo_ind = (min(errors) // block_size)     * block_size
    hi_ind = (max(errors) // block_size + 1) * block_size
    
    inds = [er % block_size for er in errors]

    return False, inds, (lo_ind, hi_ind)
    



    # # multiple errors
    # if len(block_errors_c1) > 1 or len(block_errors_c2) > 1:
    #     return False, block_errors_c1+block_errors_c2, (0, len(txt))

    # r1 = block_errors_c1[0]
    # r2 = block_errors_c2[0]

    # ind = None
    # txt_len = len(txt)

    # for i in range(r1, txt_len, block_size):
    #     if i % (block_size+1) == r2:
    #         ind = i
    #         break
    
    # if ind == None:
    #     lo_ind = (r1 // block_size)     * block_size
    #     hi_ind = (r2 // block_size + 1) * block_size

    #     return False, [r1, r2], (lo_ind, hi_ind)
    
    # lo_ind = (ind // block_size)     * block_size
    # hi_ind = (ind // block_size + 1) * block_size

    # return False, [ind%block_size], (lo_ind, hi_ind)

    # # reduce what quadrant the error is in
    # half_len = len(txt) // 2
    # forth_len = len(txt) // 4 
    
    # text_h = txt[:half_len]
    # text_q = txt[:forth_len] + txt[half_len:(half_len+forth_len)]    

    # half_correct = c_half == __generate_checksum(text_h, alphabet, block_size)
    # qrtr_correct = c_quart == __generate_checksum(text_q, alphabet, block_size)
    
    # if half_correct:
    #     bad_range = (half_len+forth_len, len(txt)) if qrtr_correct else (half_len, half_len+forth_len)
    # else:
    #     bad_range = (forth_len, half_len) if qrtr_correct else (0, forth_len)

    # lo_ind = (bad_range[0] // block_size)     * block_size
    # hi_ind = (bad_range[1] // block_size + 1) * block_size
    
    # return len(block_errors) == 0, block_errors, (lo_ind, hi_ind)
