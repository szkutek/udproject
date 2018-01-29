import pyodbc
import re
import nltk


def common_elements(list1, list2):
    return list(set(list1) & set(list2))


def lemmatize(tokens):
    lemmatizer = nltk.stem.WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word.lower(), 'n') for word, part in tokens if
             part[0].isalpha() and
             part in ['NN', 'NNS', 'NPP', 'NPPS'] and "'" not in word]
    return list(set(words))


def main(id, tekst):
    tokens = nltk.word_tokenize(tekst)

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

    # SALARY
    salary_txt = []
    for word in tokens:
        if word.lower() in ['salary', 'pay', 'payment']:
            ind = tokens.index(word)
            salary_txt = tokens[ind - 10:ind + 10]
            break
    salary_txt = nltk.pos_tag(salary_txt)
    salary_str = [s[0] for s in salary_txt if s[1] == 'CD']
    try:
        salary = [int(s.replace(',', '').replace('.', '')) for s in salary_str]
    except:
        salary = []
    if salary:
        currency_token = salary_txt[salary_txt.index((str(salary_str[-1]), 'CD')) + 1]
        currency = currency_token[0] if currency_token[1] == 'NNP' or currency_token[1] == 'NN' else None
        salary_min = min(salary)
        salary_max = max(salary)
    else:
        currency = None
        salary_min = None
        salary_max = None

    ## CONTRACT
    types = ['b2b', 'full-time', 'fixed-term', 'part-time', 'apprenticeship']
    p = re.compile('|'.join(types), re.IGNORECASE)
    contract_type = p.search(tekst)
    contract_type = contract_type.group().lower() if contract_type is not None else None

    ## RELOCATE
    p = re.compile('relocation|relocate|relocating')
    relocate = p.search(tekst)
    relocate = int(relocate is not None)
    print(relocate)

    ## TECHNOLOGIES
    technologies = ['Java', 'SAP', 'JavaScript', '\.NET', 'Angular', 'PHP', 'iOS', 'Anroid', 'C\+\+', 'Sharepoint',
                    'SQL', 'Linux', 'Big Data', 'DevOps', 'Test Automation']
    p = re.compile('|'.join(technologies), re.IGNORECASE)
    tech_res = p.findall(tekst)
    tech_res = frozenset([r.lower() for r in tech_res])

    server = 'ud-project.database.windows.net'
    database = 'UD_Project'
    username = ''
    password = ''

    db = pyodbc.connect(
        r'DRIVER={ODBC Driver 13 for SQL Server};'
        r'SERVER=' + server + ';'
                              r'DATABASE=' + database + ';'
                                                        r'UID=' + username + ';'
                                                                             r'PWD=' + password, autocommit=True)

    cursor = db.cursor()

    cursor.execute(
        'INSERT INTO Jobs (job_id, salary_low, salary_up, salary_currency, contract_type, relocate) VALUES (?,?,?,?,?,?)',
        (id, salary_min, salary_max, currency, contract_type, relocate))

    for r in resps:
        cursor.execute('INSERT INTO JobResps (job_id, resp) VALUES (?,?)', (id, r))
    for q in quals:
        cursor.execute('INSERT INTO JobQuals (job_id, qual) VALUES (?,?)', (id, q))
    for t in tech_res:
        cursor.execute('INSERT INTO JobTechs (job_id, tech) VALUES (?,?)', (id, t))
    db.close()
