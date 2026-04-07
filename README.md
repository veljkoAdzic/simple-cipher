# Simple cipher

This is a project made to test out a simple though experiment: What would a cipher look like in the old days if they had more modern encription techniques?

## How it works

The core of the project is the LSFR algorithm that generates pseudo-random numbers in a deterministic way. Given a non-zero seed number (and other hyperparameters that get automatically calculated) the algorithm can generate a sequence of random numbers or a stream of random bits.

A static character set (referred as `alphabet` in the code) gets shuffled and generates a new shuffled alphabet.

After the input text is parsed and properly formatted, in 8 character chunks the characters get changed to the new shuffled alphabet characters at their position. For every block there is also a looping offset applied to the character lookup, that is determined from the LSFR algorithm. This technique makes it harder to crack the encryption.

Finally, there is a metadata string generated that contains the encoded starting seed, as well as a checksum that allows the decrypting end to find errors. This metadata string is appended at the end of the encoded text.