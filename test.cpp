#include <iostream>
#include <string>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <sstream>

using namespace std;

// Runs a command with simulated stdin input (via a temp file) and returns stdout as a string
string runProgram(const string &exe, const string &input) {
    // create a temporary input file
    const string tmp = "tmp_input_for_test.txt";
    {
        ofstream ofs(tmp, ios::binary);
        if (!ofs) {
            cerr << "Failed to open temp input file\n";
            exit(1);
        }
        ofs << input;
    }

    // run the program redirecting stdin from the temp file and capture stdout+stderr
    string command =  exe + " < " + tmp + " 2>&1";
    FILE *pipe = popen(command.c_str(), "r");
    if (!pipe) {
        perror("popen failed");
        remove(tmp.c_str());
        exit(1);
    }

    char buffer[256];
    string result;
    while (fgets(buffer, sizeof(buffer), pipe)) {
        result += buffer;
    }

    int rc = pclose(pipe);
    (void)rc; // ignore but could be checked

    // remove the temporary file
    remove(tmp.c_str());
    return result;
}

int main(int argc, char **argv) {
    string exe = "program";   // <-- change to your compiled executable name if needed

    // -----------------------------------------------------
    // 1. FIXED TEST INPUTS
    // -----------------------------------------------------
    string seed = "";     // empty → use default
    string taps = "";
    string len = "";
    string block = "";
    string alphabet = "";
    string original_text = "";
    

    if (argc < 2)
        original_text = "THE QUICK BROWN FOX JUMPS!"; // IT JUMPED OVER THE LAZY DOG";
    else 
        original_text = argv[1];

    // INPUT FOR ENCODING RUN
    string encode_input =
        seed + "\n" +
        taps + "\n" +
        len + "\n" +
        block + "\n" +
        alphabet + "\n" +
        "e\n"           // choose encode
        + original_text + "\n";

    // -----------------------------------------------------
    // 2. RUN ENCODING
    // -----------------------------------------------------
    cout << "=== Running ENCODE ===\n";
    string encoded_output = runProgram(exe, encode_input);
    cout << encoded_output << "\n";

    // safer: extract encoded message that appears before the last ':' on the last output line
    string encoded_message;
    size_t colon = encoded_output.rfind(':');
    if (colon != string::npos) {
        // find start of the line that contains the colon
        size_t lineStart = encoded_output.rfind('\n', colon == string::npos ? encoded_output.size() : colon);
        if (lineStart == string::npos) lineStart = 0; else lineStart++;
        // substring between lineStart and colon is the scrambled text + maybe leading prompts; trim spaces
        if (colon > lineStart)
            encoded_message = encoded_output.substr(lineStart, colon - lineStart);
        else
            encoded_message = encoded_output.substr(0, colon);
    } else {
        // fallback: use entire output
        encoded_message = encoded_output;
    }

    // Trim whitespace/newlines around encoded_message
    auto trim = [](string &s){
        while (!s.empty() && (s.back() == '\n' || s.back() == '\r' || s.back() == ' ' || s.back() == '\t')) s.pop_back();
        size_t i = 0;
        while (i < s.size() && (s[i] == '\n' || s[i] == '\r' || s[i] == ' ' || s[i] == '\t')) ++i;
        if (i) s = s.substr(i);
    };
    trim(encoded_message);

    cout << "Extracted encoded_message: [" << encoded_message << "]\n";

    // -----------------------------------------------------
    // 3. PREPARE DECODE INPUT (same settings, user picks 'd')
    // -----------------------------------------------------
    string decode_input =
        seed + "\n" +
        taps + "\n" +
        len + "\n" +
        block + "\n" +
        alphabet + "\n" +
        "d\n"         // choose decode
        + encoded_message + "\n";

    // -----------------------------------------------------
    // 4. RUN DECODING
    // -----------------------------------------------------
    cout << "=== Running DECODE ===\n";
    string decoded_output = runProgram(exe, decode_input);
    cout << decoded_output << "\n";

    // -----------------------------------------------------
    // 5. COMPARE RESULTS
    // -----------------------------------------------------
    cout << "\n=== TEST RESULT ===\n";

    istringstream iss(decoded_output);
    string s;
    string final_out = "";
    while( getline(iss, s, '\n') ) {
        if(s.length() > 0)
            final_out = s;
    }

    if(final_out.find(original_text) != string::npos){
        cout << "PASS: Decoded text matches original.\n";
    } else {
        cout << "####  FAIL  ####\n";
    }

    cout << "EXPECTED: '" << original_text  << "'"<< endl;
    cout << "GOT:      '" << final_out      << "'"<< endl;

    return 0;
}
