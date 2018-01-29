import sqlite3

import nltk
import re


def common_elements(list1, list2):
    return list(set(list1) & set(list2))


def lemmatize(tokens):
    lemmatizer = nltk.stem.WordNetLemmatizer()
    wnpos = lambda e: ('a' if e[0].lower() == 'j' else e[0].lower()) if e[0].lower() in ['n', 'r', 'v'] else 'n'
    words = [lemmatizer.lemmatize(word.lower(), wnpos(part)) for word, part in tokens if
             part[0].isalpha() and
             part in ['NN', 'NNS', 'NPP', 'NPPS'] and "'" not in word]
    return list(set(words))


if __name__ == '__main__':
    test1 = open('test1.txt').read()
    tokens = nltk.word_tokenize(test1)

    keywords = {'quals': ['required', 'requirements', 'skills', 'competency', 'competencies'],
                'resps': ['description', 'responsibilities', 'role'],
                'perks': ['offer', 'workplace']}
    indices = []
    for key in keywords:
        comms = common_elements(tokens, keywords[key])
        tmp = [tokens.index(c) for c in comms]
        indices.append((key, min(tmp) if tmp != [] else -1))
    indices = sorted(indices, key=lambda x: x[1])

    tmps = [0] * 3
    tmps[0] = indices[0][0], tokens[indices[0][1] + 1:indices[1][1]]
    tmps[1] = indices[1][0], tokens[indices[1][1] + 1:indices[2][1]]
    tmps[2] = indices[2][0], tokens[indices[2][1] + 1:] if indices[2][1] != -1 else []

    indices = [*zip(*indices)][0]
    resps = tmps[indices.index('resps')][1]
    quals = tmps[indices.index('quals')][1]
    # perks = tmps[indices.index('perks')][1]

    resps = nltk.pos_tag(resps)
    resps = lemmatize(resps)

    quals = nltk.pos_tag(quals)
    quals = lemmatize(quals)

    ## SALARY
    salary_txt = []
    for word in tokens:
        if word.lower() in ['salary', 'pay', 'payment']:
            ind = tokens.index(word)
            salary_txt = tokens[ind - 10:ind + 10]
            break
    salary_txt = nltk.pos_tag(salary_txt)
    salary = [int(s[0]) for s in salary_txt if s[1] == 'CD']
    if salary != []:
        currency_token = salary_txt[salary_txt.index((str(salary[-1]), 'CD')) + 1]
        currency = currency_token[0] if currency_token[1] == 'NNP' or currency_token[1] == 'NN' else ''
        salary_min = min(salary)
        salary_max = max(salary)
    else:
        currency = ''
        salary_min = ''
        salary_max = ''

    ## CONTRACT
    types = ['b2b', 'full-time', 'fixed-term', 'part-time', 'apprenticeship']
    p = re.compile('|'.join(types), re.IGNORECASE)
    contract_type = p.search(test1)
    contract_type = contract_type.group().lower() if contract_type is not None else ''

    ## RELOCATE
    p = re.compile('relocation|relocate|relocating')
    relocate = p.search(test1)
    relocate = int(relocate is not None)
    print(relocate)

    db = sqlite3.connect('parsed.db')
    cursor = db.cursor()

    job_id = 1  # TODO

    try:
        cursor.execute(
            'INSERT INTO Jobs (job_id, salary_low, salary_up, salary_currency, contract_type, relocate) VALUES (?,?,?,?,?,?)',
            (job_id, salary_min, salary_max, currency, contract_type, relocate)
        )
        db.commit()
    except:
        pass

    for r in resps:
        try:
            cursor.execute('INSERT INTO JobResps (job_id, resp) VALUES (?,?)', (job_id, r))
            db.commit()
        except:
            pass
    for q in quals:
        try:
            cursor.execute('INSERT INTO JobQuals (job_id, qual) VALUES (?,?)', (job_id, q))
            db.commit()
        except:
            pass

    db.close()
