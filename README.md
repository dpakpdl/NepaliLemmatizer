# NepaliLemmatizer
Lemmatization of Nepali Text based on TRIE and Hybrid approach

## Steps to Run:
- Goto cloned repo: `cd NepaliLemmatizer`
- Export python path: `export PYTHONPATH=$PYTHONPATH:$(pwd)`
- Run: `python Lemmatization/lemmatizer.py -m <<trie or hybrid>> -t <<Nepali Text>>`

Example: `python Lemmatization/lemmatizer.py -m trie -t निर्माणको`

### Arguments to be supplied
- `-m` method name which can be either `trie` or `hybrid`
- `-t` nepali text
- `--help` for help text


