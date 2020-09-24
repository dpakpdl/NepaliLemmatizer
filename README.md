# NepaliLemmatizer
Lemmatization of Nepali Text based on TRIE and Hybrid approach

## Steps to Run:
- Goto cloned repo: `cd NepaliLemmatizer`
- Make virtual environment: `python3 -m venv my-env`
- Activate virtual environment: `source my-env/bin/activate`
- Install dependent packages: `pip install -r requirements.txt`
- Export python path: `export PYTHONPATH=$PYTHONPATH:$(pwd)`
- Run: `python Lemmatization/lemmatizer.py -m <<trie or hybrid>> -t <<Nepali Text>>`

### Arguments to be supplied
- `-m` method name which can be either `trie` or `hybrid`
- `-t` nepali text
- `--help` for help text


Example: `python Lemmatization/lemmatizer.py -m trie -t निर्माणको`

Output: 

![Output](/output/out.png)
