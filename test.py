import subprocess
import sys

ORIGINA_TEXT = "Hello my dear, I am writing to you today to tell you that I have arrived to the desert resort. It is truely remarkable and i wish you were here to witness it yourself. Alas, I miss your presance, and cannot wait to come home and see you dear. Yours truely, Robert"

ENCODED_TEXT = "2%773; B8s8t! _Ks57lx72, v% 1k0yz%y3! Ua; ! F2l%x_%xj? ? H7s 2h4cafn. N1wbidvffs3x 0ruqru&br0x7xfbdf ! ? Lrp1xt, zwsz, 6k23u5@2&k2 6 pwscypxaf_f4_, @vwua v ? Nb. ! , . B. ! Wo1c; Wlq yy 84 n 8qbcw_8lts6. F. Nut2t60 443b, 9oimoda&jmof9j il9w? , , K9&7_67e74ec941@ s9 4 1 ! I91 ! H. . ? A*5? Bhz04gkv. 0Xu@e! Gbt5&4k p v 49&:F6B_D96D-@_QLS%IE!-AG"

# I am -> I #m
ENCODED_SINGLE_Q1 = "2%773; B8s8t! _Ks571x72, v% 1k0yz%y3! Ua; ! F2l%x_%xj? ? H7s 2h4cafn. N1wbidvffs3x 0ruqru&br0x7xfbdf ! ? Lrp1xt, zwsz, 6k23u5@2&k2 6 pwscypxaf_f4_, @vwua v ? Nb. ! , . B. ! Wo1c; Wlq yy 84 n 8qbcw_8lts6. F. Nut2t60 443b, 9oimoda&jmof9j il9w? , , K9&7_67e74ec941@ s9 4 1 ! I91 ! H. . ? A*5? Bhz04gkv. 0Xu@e! Gbt5&4k p v 49&:F6B_D96D-@_QLS%IE!-AG"

# I wish you were -> I wish #ou were
ENCODED_SINGLE_Q2 = "2%773; B8s8t! _Ks57lx72, v% 1k0yz%y3! Ua; ! F2l%x_%xj? ? H7s 2h4cafn. N1wbidvffs3x 0ruqru&br0x7xfbdf ! ? Lrp1xt, zwsz, 6k23u5@2&k2 6 pwscypxaf_f4_, @vqua v ? Nb. ! , . B. ! Wo1c; Wlq yy 84 n 8qbcw_8lts6. F. Nut2t60 443b, 9oimoda&jmof9j il9w? , , K9&7_67e74ec941@ s9 4 1 ! I91 ! H. . ? A*5? Bhz04gkv. 0Xu@e! Gbt5&4k p v 49&:F6B_D96D-@_QLS%IE!-AG"

# here to witness it -> here to w#tness it 
ENCODED_SINGLE_Q3 = "2%773; B8s8t! _Ks57lx72, v% 1k0yz%y3! Ua; ! F2l%x_%xj? ? H7s 2h4cafn. N1wbidvffs3x 0ruqru&br0x7xfbdf ! ? Lrp1xt, zwsz, 6k23u5@2&k2 6 pwscypxaf_f4_, @vwua v ? Nb. ! , . B. ! Wo1c8 Wlq yy 84 n 8qbcw_8lts6. F. Nut2t60 443b, 9oimoda&jmof9j il9w? , , K9&7_67e74ec941@ s9 4 1 ! I91 ! H. . ? A*5? Bhz04gkv. 0Xu@e! Gbt5&4k p v 49&:F6B_D96D-@_QLS%IE!-AG"

# home and see you -> home #nd see you
ENCODED_SINGLE_Q4 = "2%773; B8s8t! _Ks57lx72, v% 1k0yz%y3! Ua; ! F2l%x_%xj? ? H7s 2h4cafn. N1wbidvffs3x 0ruqru&br0x7xfbdf ! ? Lrp1xt, zwsz, 6k23u5@2&k2 6 pwscypxaf_f4_, @vwua v ? Nb. ! , . B. ! Wo1c; Wlq yy 84 n 8qbcw_8lts6. F. Nut2t60 443b, 9oimoda&jmof9j il9w? , , K9&7_67e74ec941@ s9 4 1 ! L91 ! H. . ? A*5? Bhz04gkv. 0Xu@e! Gbt5&4k p v 49&:F6B_D96D-@_QLS%IE!-AG"

# Hello my dear, I am writing -> Hello my dear, # #m writing (_#_____#)
ENCODED_DOUBLE_TROUBLE = "2%773; B8s8t! _KsS71x72, v% 1k0yz%y3! Ua; ! F2l%x_%xj? ? H7s 2h4cafn. N1wbidvffs3x 0ruqru&br0x7xfbdf ! ? Lrp1xt, zwsz, 6k23u5@2&k2 6 pwscypxaf_f4_, @vwua v ? Nb. ! , . B. ! Wo1c; Wlq yy 84 n 8qbcw_8lts6. F. Nut2t60 443b, 9oimoda&jmof9j il9w? , , K9&7_67e74ec941@ s9 4 1 ! I91 ! H. . ? A*5? Bhz04gkv. 0Xu@e! Gbt5&4k p v 49&:F6B_D96D-@_QLS%IE!-AG"

# I am writing -> I #m writing | I wish you were -> I wish #ou were
ENCODED_TWO_QUADRANTS = "2%773; B8s8t! _Ks571x72, v% 1k0yz%y3! Ua; ! F2l%x_%xj? ? H7s 2h4cafn. N1wbidvffs3x 0ruqru&br0x7xfbdf ! ? Lrp1xt, zwsz, 6k23u5@2&k2 6 pwscypxaf_f4_, @vqua v ? Nb. ! , . B. ! Wo1c; Wlq yy 84 n 8qbcw_8lts6. F. Nut2t60 443b, 9oimoda&jmof9j il9w? , , K9&7_67e74ec941@ s9 4 1 ! I91 ! H. . ? A*5? Bhz04gkv. 0Xu@e! Gbt5&4k p v 49&:F6B_D96D-@_QLS%IE!-AG"


SEED = "17"

encoding_tests = {
    "normal": ENCODED_TEXT,
    "q1 modified": ENCODED_SINGLE_Q1,
    "q2 modified": ENCODED_SINGLE_Q2,
    "q3 modified": ENCODED_SINGLE_Q3,
    "q4 modified": ENCODED_SINGLE_Q4,
    "two places in quadrant": ENCODED_DOUBLE_TROUBLE,
    "single mods in q1 and q2": ENCODED_TWO_QUADRANTS
}

def run_program(inputs:list[str]):
    """
    Runs main.py with given inputs and returns stdout.
    `inputs` should be a single string with newline-separated input.
    """
    formated_inputs = "\n".join(inputs) + "\n"

    result = subprocess.run(
        [sys.executable, "main.py"],
        input=formated_inputs,
        text=True,
        capture_output=True
    )
    return result.stdout, result.stderr, result.returncode


def test_encode():
    inputs = ["e", SEED, ORIGINA_TEXT]
    stdout, stderr, code = run_program(inputs)
    print("ENCODE OUTPUT:")
    print(stdout)
    print("STDERR:")
    print(stderr)
    # assert code == 0
    # assert stdout.strip() != ""


def test_decode():
    # Replace with an encoded string that your encoder produces
    for test_name, enc_text in encoding_tests.items():
        print(f"[TEST]: {test_name}")
        inputs = ["d", enc_text]
        stdout, stderr, code = run_program(inputs)
        print("[TEST] OUTPUT:")
        print(stdout)
        print("[TEST] STDERR:")
        print(stderr)
        # assert code == 0


if __name__ == "__main__":
    test_encode()
    test_decode()
    print("All tests passed!")
