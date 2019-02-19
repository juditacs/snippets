#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2019 Judit Acs <judit@sch.bme.hu>
#
# Distributed under terms of the MIT license.

from argparse import ArgumentParser
import pandas as pd
import os
from collections import defaultdict

from pytorch_pretrained_bert import BertTokenizer


def parse_args():
    p = ArgumentParser()
    p.add_argument('input_dirs', nargs='+', type=str)
    p.add_argument('--output-tsv', type=str, default="output.tsv")
    return p.parse_args()


tokenizer = BertTokenizer.from_pretrained(
    'bert-base-multilingual-cased', do_lower_case=False)


def read_sentences(stream):
    comments = []
    sent = []
    for line in stream:
        if line.startswith("#"):
            comments.append(line)
            continue
        if not line.strip():
            if sent:
                yield comments, sent
            sent = []
            comments = []
        else:
            sent.append(line.rstrip("\n"))
    if sent:
        yield comments, sent


def get_real_tokens(sentence):
    real = []
    idx = 0
    while idx < len(sentence):
        id_ = sentence[idx].split("\t")[0]
        real.append(sentence[idx])
        if '-' in id_:
            src, tgt = id_.split('-')
            diff = int(tgt) - int(src) + 1
            idx += diff
        else:
            idx += 1
    return real


def compute_stats(fn):
    cnt = defaultdict(int)
    bert_token_len = defaultdict(int)
    token_len = defaultdict(int)
    bert_sent_len = defaultdict(int)
    sent_len = defaultdict(int)
    with open(fn) as f:
        for comments, sentence in read_sentences(f):
            full_sent = None
            for cline in comments:
                if cline.startswith('# text = '):
                    full_sent = cline[len('# text ='):]
            if full_sent is None:
                bert_tokens = []
                for line in sentence:
                    token = line.split("\t")[1]
                    bert_tokens.extend(tokenizer.tokenize(token))
                cnt['no_full_text'] += 1
            else:
                bert_tokens = tokenizer.tokenize(full_sent)
            cnt['sent_i'] += 1
            cnt['token_no'] += len(sentence)
            sent_len[len(sentence)] += 1
            cnt['bert_token_no'] += len(bert_tokens)
            real_tokens = []
            sentence = get_real_tokens(sentence)
            for line in sentence:
                token = line.split("\t")[1]
                token_len[len(token)] += 1
                real_tokens.append(token)

            bert_token_len[len(bert_tokens[0])] += 1
            for b in bert_tokens[1:]:
                if b.startswith('##'):
                    cnt['continuation'] += 1
                    b = b[2:]
                bert_token_len[len(b)] += 1
            bert_sent_len[len(bert_tokens)] += 1
            cnt['bert_maxlen'] = max(len(bert_tokens), cnt['bert_maxlen'])
            cnt['sent_maxlen'] = max(len(sentence), cnt['sent_maxlen'])

    stat = {
        'token_no': cnt['token_no'],
        'bert_token_no': cnt['bert_token_no'],
        'avg_bert_gain': cnt['bert_gain'] / cnt['sent_i'],
        'sentence_no': cnt['sent_i'],
        'sentence_maxlen': cnt['sent_maxlen'],
        'bert_sentence_maxlen': cnt['bert_maxlen'],
        'no_full_text': cnt['no_full_text'],
        'continuation': cnt['continuation'],
    }
    for l, fr in bert_token_len.items():
        stat['bert_len_{}'.format(l)] = fr
    for l, fr in token_len.items():
        stat['token_len_{}'.format(l)] = fr
    for l, fr in sent_len.items():
        stat['sent_len_{}'.format(l)] = fr
    for l, fr in bert_sent_len.items():
        stat['bert_sent_len_{}'.format(l)] = fr
    return stat


def is_ok(dirname):
    data_files = find_conllu_files(dirname)
    if len(data_files) < 1:
        return False
    with open(os.path.join(dirname, data_files[0])) as f:
        sent = next(read_sentences(f))[1]
        tcnt = 0
        for line in sent:
            tcnt += line.split("\t")[1] == "_"
        if tcnt >= len(sent) // 2:
            return False
    return True


def find_conllu_files(dirname):
    return list(filter(lambda l: l.endswith("train.conllu"), os.listdir(dirname))) + \
              list(filter(lambda l: l.endswith("dev.conllu"), os.listdir(dirname))) + \
              list(filter(lambda l: l.endswith("test.conllu"), os.listdir(dirname)))


def main():
    args = parse_args()
    stats = []
    for dirname in args.input_dirs:
        if not is_ok(dirname):
            continue
        print(dirname)
        for fn in find_conllu_files(dirname):
            full_fn = os.path.join(dirname, fn)
            st = compute_stats(full_fn)
            st['filename'] = os.path.realpath(full_fn)
            stats.append(st)
    stats = pd.DataFrame(stats)
    stats.to_csv(args.output_tsv, sep="\t")

if __name__ == '__main__':
    main()
