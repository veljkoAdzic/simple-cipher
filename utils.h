#include <iostream>
#include <cstdint>
#include <cmath>
//#include "lsfr.h"

using namespace std;

// format text for parsing
string normaliseText(string &og)
{
    string res = "";

    char tmp;
    for (int i = 0; i < og.size(); i++)
    {
        tmp = og.at(i);

        if (isalpha(tmp))
        {
            res += toupper(tmp);
        }
        else if (tmp == ' ')
        {
            res += '_';
        }
        else
        {
            res += tmp;
        }
    }

    return res;
}

// deformat parsed text ( UNUSED! )
string denormaliseText(string &norm)
{
    string res = "";

    char tmp;
    for (int i = 0; i < norm.size(); i++)
    {
        tmp = norm.at(i);

        if (tmp == '_')
            res += ' ';
        else
            res += tmp;
    }

    return res;
}

string normaliseEncodedText(string &og)
{
    string res = "";
    int len = og.size();
    char tmp;
    for (int i = 0; i < len; i++)
    {
        tmp = og.at(i);
        if (tmp == ' ')
            continue;
        if (tmp == ':')
            break;
        res += toupper(tmp);
    }
    return res;
}

// add random whitespaces and capitalisation (doesn't affect meaning)
string formatText(string &raw, Cipher &engine)
{
    string res = "";

    int len = raw.size();

    unsigned short jmp = engine.nextStream() & 15;
    bool upr = true;
    char tmp;
    for (int i = 0; i < len; i++)
    {
        tmp = raw.at(i);
        if (upr && isalpha(tmp))
        {
            res += tmp;
            upr = false;
        }
        else
            res += tolower(tmp);

        if (tmp == '.' || tmp == '!' || tmp == '?')
            upr = true;

        if (jmp <= 0 && i < len - 1)
        {
            res += " ";
            jmp = engine.nextStream() & 15;
        }
        else
            jmp--;
    }

    return res;
}

// ckecksum for validating message
string calculateChecksum(string &str, string &alphabet, int bs)
{
    string cs = "";
    int checks[bs];

    for (int i = 0; i < bs; i++)
        checks[i] = 0;

    int len = str.size();
    for (int i = 0; i < len; i++)
        checks[i % bs] += alphabet.find(str.at(i));

    len = alphabet.size();
    for (int i = 0; i < bs; i++)
        cs += alphabet.at(checks[i] % len);

    return cs;
}

// formating seed and tap to be added as mettadata
string calculateSign(unsigned int s, unsigned int t, string &al)
{
    string res = "";

    int tmp;
    while (t != 0)
    {
        tmp = t % 10;
        t /= 10;
        res = al.at(tmp) + res;
    }

    res = "-" + res;

    while (s != 0)
    {
        tmp = s % 10;
        s /= 10;
        res = al.at(tmp) + res;
    }

    return res;
}

int findChar(char *arr, int size, char c)
{
    for (int i = 0; i < size; i++)
    {
        if (arr[i] == c)
            return i;
    }

    return 0;
}
