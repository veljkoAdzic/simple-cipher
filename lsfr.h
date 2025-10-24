struct Pair 
{
    unsigned int step;
    unsigned short stream;
};

class Cipher
{
    unsigned short seed;
    unsigned short taps;
    int length;

    unsigned short curr;
    unsigned short stream;

public:
    Cipher(unsigned short seed, unsigned short taps, int length)
    {
        this->seed = seed;
        this->taps = taps;
        this->length = length;

        curr = seed;
        stream = curr & 1;
    }

    void calculate()
    {
        unsigned short tmp = 0;
        for (int j = 0; j < length; j++)
        { // XOR with taps
            if ((taps >> j) & 1)
                tmp ^= (curr >> j) & 1;
        }

        curr = (curr >> 1) | (tmp << (length - 1)); // new bit added
        stream = (stream << 1) | (curr & 1);        // new bit to stream
    }

    unsigned short nextStep()
    { // get next number
        short res = curr;
        calculate();
        return res;
    }

    unsigned short nextStream()
    { // get next stream bits
        unsigned short res = stream;
        calculate();

        res = res & ((1 << length) - 1);
        return res;
    }

    Pair nextPair()
    { // get next number and stream bits
        Pair res = {curr, stream};
        calculate();
        return res;
    }
};
