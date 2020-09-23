import os

THIS_DIR = os.path.abspath(os.path.dirname(__file__))


def get_current_directory():
    return THIS_DIR


def get_data_path():
    return os.path.join(os.path.dirname(THIS_DIR), 'data')


def get_root_pos_rule_csv_path():
    data_path = get_data_path()
    return os.path.join(data_path, 'root_pos_rules.csv')


def get_nepali_dict_path():
    return os.path.join(get_data_path(), 'original', 'ne_NP_original.dic')


def get_nepali_rules_path():
    return os.path.join(get_data_path(), 'affix', 'ne_NP.aff')


def get_evaluation_data_path():
    return os.path.join(get_data_path(), 'evaluation')


def get_evaluation_files():
    return os.path.join(get_evaluation_data_path(), 'all_words_v2.txt')
    # return os.path.join(get_data_path(), 'all_words.txt')
    # return os.path.join(get_data_path(), 'all_words_for_evaluation.txt')


def get_manually_annotated_corpus_file():
    return os.path.join(get_data_path(), 'manually_annotated_corpus', 'gold_data.txt')


def get_morphology_path():
    data_path = get_data_path()
    return os.path.join(data_path, 'morphology')


def get_suffix_path():
    return os.path.join(get_morphology_path(), 'suffix.txt')


def get_stop_word_path():
    return os.path.join(get_morphology_path(), 'stop_words.txt')


def get_prefix_path():
    return os.path.join(get_morphology_path(), 'prefix.txt')
