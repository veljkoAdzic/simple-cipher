#include <iostream>
#include <cstdint>
#include <cmath>
#include "lsfr.h"
#include "utils.h"

using namespace std;

/*
void printStream(short seed, short taps){
    cout << left << setw(5) << setfill(' ') << "No.";
    cout << left << setw(7) << setfill(' ') << "Bin.";
    cout << left << setw(6) << setfill(' ') << "Curr";
    cout << left << setw(5) << setfill(' ') << "Out" << endl;

    //lfsr
    short curr = seed;
    bool bit = curr & 1;
    int i = 0;


    do{
        std::bitset<LENGTH> b_cur(curr);
        cout << left << setw(5) << setfill(' ') << (i++);
        cout << left << setw(7) << setfill(' ') << b_cur;
        cout << left << setw(6) << setfill(' ') << curr;
        cout << left << setw(5) << setfill(' ') << bit << endl;

        unsigned short tmp = 0;
        for(int j = 0; j < LENGTH; j++){
            if((taps >> j) & 1){
                tmp ^= (curr >> j) & 1;
            }
        }


        curr = (curr >> 1) | (tmp << (LENGTH-1));
        bit = curr  & 1 ;


    } while(curr != seed && i <= (1 << LENGTH));
}
*/

inline void decode(unsigned short &seed, unsigned short &taps, short &BLOCK_SIZE, Cipher &engine, string &alphabet, char *chi_abc)
{
    string original;

    cout << "Input text for decoging:\n";
    cin.ignore();
    getline(cin, original);

    string norm = normaliseEncodedText(original);

    string scrambled = "";
    for (int i = 0; i < norm.size(); i += BLOCK_SIZE)
    {
        string block = norm.substr(i, BLOCK_SIZE);
        unsigned short shift = engine.nextStream();
        for (int j = 0; j < BLOCK_SIZE; j++)
        {
            // chi_abc.find(norm.at(i + j)) - shift)
            // int index = ((alphabet.size() - 1) + findChar(chi_abc, alphabet.size() - 1, norm.at(i + j)) + shift) % (alphabet.size() - 1) - 1;
            // cout << endl
            //      << "TEST: " << findChar(chi_abc, alphabet.size(), norm.at(i + j)) << " " << (findChar(chi_abc, alphabet.size() - 1, norm.at(i + j)) - shift + (alphabet.size() - 1)) << " " << (findChar(chi_abc, alphabet.size() - 1, norm.at(i + j)) - shift + (alphabet.size() - 1)) % (alphabet.size()) << endl;

            int index = (findChar(chi_abc, alphabet.size() - 1, block.at(j)) - shift + (alphabet.size() - 1)) % (alphabet.size());

            // int index = (findChar(chi_abc, alphabet.size(), norm.at(i + j)) - shift + (alphabet.size())) % (alphabet.size());
            scrambled += alphabet[index];
        }
    }

    // string checksum = calculateChecksum(norm, alphabet, BLOCK_SIZE);
    // string sign = calculateSign(seed, taps, alphabet);

    // cout << formatText(scrambled, engine) << ":" << checksum << "-" << sign;
    cout << denormaliseText(scrambled);
}

inline void encode(unsigned short &seed, unsigned short &taps, short &BLOCK_SIZE, Cipher &engine, string &alphabet, char *chi_abc)
{
    string original;

    cout << "Input text for encoging:\n";
    cin.ignore();
    getline(cin, original);

    string norm = normaliseText(original);

    while (norm.size() % BLOCK_SIZE != 0)
        norm += '_';

    string scrambled = "";
    for (int i = 0; i < norm.size(); i += BLOCK_SIZE)
    {
        string block = norm.substr(i, BLOCK_SIZE);
        unsigned short shift = engine.nextStream();
        for (int j = 0; j < BLOCK_SIZE; j++)
        {
            int index = (alphabet.find(norm.at(i + j)) + shift) % (alphabet.size()) + 1;
            scrambled += chi_abc[index];
        }
    }

    string checksum = calculateChecksum(norm, alphabet, BLOCK_SIZE);
    string sign = calculateSign(seed, taps, alphabet);

    cout << formatText(scrambled, engine) << ":" << checksum << "-" << sign;
}

int main()
{
    unsigned short seed = 0b10001;
    unsigned short taps = 0b00101;
    int LENGTH = 5;
    short BLOCK_SIZE = 8;

    string alphabet = "-ABCDEFGHIJKLMNOPQRSTUVWXYZ_.,!?";
    // string alphabet = "-_ETIANMSURWDKGOHVFLPJBXCYZQ.,!?";
    // string alphabet = "-ABCD_EFGHIJKLMNOPQRSTUVWXYZ.,!?";

    cout << "   WELCOME TO LFSR scrabler!\n\n";

    string s_seed, s_taps, s_len, s_bs, s_alphabet;
    cout << " Input seed [" << seed << "]:";
    // cin >> s_seed;
    getline(cin, s_seed);
    cout << " Input taps [" << taps << "]:";
    // cin >> s_taps;
    getline(cin, s_taps);
    cout << " Input bit depth [" << LENGTH << "]:";
    // cin >> s_len;
    getline(cin, s_len);
    cout << " Input block size [" << BLOCK_SIZE << "]:";
    // cin >> s_bs;
    getline(cin, s_bs);
    cout << " Input alphabet [" << alphabet << "]:";
    // cin >> s_alphabet;
    getline(cin, s_alphabet);

    if (s_seed.size() != 0)
    {
        try
        {
            seed = stoi(s_seed);
        }
        catch (const invalid_argument &e)
        {
            cout << "> Invalid seed! using default " << seed;
        }
    }

    if (s_taps.size() != 0)
    {
        try
        {
            taps = stoi(s_taps);
        }
        catch (const invalid_argument &e)
        {
            cout << "> Invalid taps! using default " << taps;
        }
    }

    if (s_len.size() != 0)
    {
        try
        {
            LENGTH = stoi(s_len);
        }
        catch (const invalid_argument &e)
        {
            cout << "> Invalid bit depth! using default " << LENGTH;
        }
    }

    if (s_bs.size() != 0)
    {
        try
        {
            BLOCK_SIZE = stoi(s_bs);
        }
        catch (const invalid_argument &e)
        {
            cout << "> Invald block size! using default " << BLOCK_SIZE;
        }
    }

    if (s_alphabet.size() < (1 << LENGTH))
        cout << "> Invalid alphabet! using default " << alphabet;
    else
        alphabet = s_alphabet;

    char chi_abc[alphabet.size() - 1];
    Cipher engine(seed, taps, LENGTH);

    // Fisher–Yates shuffle
    int len = alphabet.size();
    for (int i = 0; i < len; i++)
        chi_abc[i] = alphabet.at(i);

    unsigned short index;
    char tmp;
    for (int i = len - 1; i > 0; i--)
    {
        index = engine.nextStep() % (i) + 1;
        tmp = chi_abc[i];
        chi_abc[i] = chi_abc[index];
        chi_abc[index] = tmp;
    }

    cout << "TEST: ";
    for (int i = 0; i < len; i++)
        cout << chi_abc[i];
    cout << endl;

    string original;

    char MODE;
    cout << " Encode or decode message? [e/d]: ";
    cin >> MODE;

    if (tolower(MODE) == 'e')
        encode(seed, taps, BLOCK_SIZE, engine, alphabet, chi_abc);
    else
        decode(seed, taps, BLOCK_SIZE, engine, alphabet, chi_abc);

    return 0;
}
