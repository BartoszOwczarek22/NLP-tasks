import re
from collections import Counter, defaultdict


def replace_pair_with_token(list, pair):
    i = 0
    result = []
    while i < len(list):
        if i < len(list) - 1 and list[i] + list[i + 1] == pair:
            result.append(pair)
            i += 2
        else:
            result.append(list[i])
            i += 1
    return result


def create_bpe_tokenizer(text, max_vocab_length):
    clean_text = re.sub('[^a-zA-Z ]', '', text).lower()
    clean_text_list = list(clean_text)
    vocab = defaultdict(int)
    bigrams_count = Counter()
    for char in clean_text:
        vocab[char] += 1

    while len(vocab) < max_vocab_length:
        bigrams_count.clear()
        for i in range(len(clean_text_list) - 1):
            if clean_text_list[i].endswith(' ') and len(clean_text_list[i]) > 1:
                continue
            elif clean_text_list[i].startswith(' '):
                continue
            elif clean_text_list[i + 1].startswith(' ') and len(clean_text_list[i + 1]) > 1:
                continue
            else:
                bigram = clean_text_list[i] + clean_text_list[i + 1]
                bigrams_count[bigram] += 1

        most_common_bigram, bigram_freq = bigrams_count.most_common(1)[0]
        vocab[most_common_bigram] += bigram_freq

        for i in range(len(clean_text_list) - 1):
            if most_common_bigram == clean_text_list[i] + clean_text_list[i + 1]:
                vocab[clean_text_list[i]] -= 1
                vocab[clean_text_list[i + 1]] -= 1

        clean_text_list = replace_pair_with_token(clean_text_list, most_common_bigram)
    return vocab


def tokenize_text(text, tokenizer):
    words = re.sub('[^a-zA-Z ]', '', text).lower()
    splits = list(words)
    tokenized_result = []
    sorted_tokens = sorted(tokenizer.keys(), key=len, reverse=True)
    while True:
        merged = False
        i = 0
        while i < len(splits) - 1:
            current_pair = splits[i] + splits[i + 1]
            if current_pair in sorted_tokens:
                splits[i:i + 2] = [current_pair]
                merged = True
            else:
                i += 1
        if not merged:
            break
    tokenized_result.extend(splits)
    return tokenized_result


with open('story.txt', 'r') as f:
    txt = f.read()

bpe_tokenizer = create_bpe_tokenizer(txt, 500)
test_text = (
    "In the digital frontier, humanity can create new connections through innovative methods, merging exploration withlearning and creativity for all.")
tokenized_result = tokenize_text(test_text, bpe_tokenizer)
print(tokenized_result)