import csv

def from_txt(way_to_file="./users.txt") -> list:
    try: f = open(way_to_file, encoding="utf-8")
    except FileNotFoundError: return []
    s = f.read()
    f.close()
    l = s.split('\n')
    rs = []
    for i in l:
        tmp = clean_input(i.split(' '))
        if tmp: rs.append({"f": tmp[0], "i": tmp[1], "o": tmp[2], 'n': int(tmp[3]), 'g': tmp[4],})
        else: break
    return rs

def from_csv(way_to_file="./users.csv", sep=";") -> list:
    try: f = open(way_to_file)
    except FileNotFoundError: return []
    s = csv.reader(f, delimiter=sep)
    rs = []
    for i in s:
        tmp = clean_input(i)
        if tmp: rs.append({"f": tmp[0], "i": tmp[1], "o": tmp[2], 'n': int(tmp[3]), 'g': tmp[4],})
        else: break
    f.close()
    return rs

def clean_input(l: list) -> list:
    rs = [i for i in l if i != '']
    if len(rs) == 0: return None
    if len(rs) < 2: rs = '\t'.join(rs).split('\t')
    if len(rs) < 2: raise ValueError
    if len(rs) == 2: rs.append('None')
    if len(rs) == 3: rs.append(0)
    if len(rs) == 4: rs.append('None')
    match rs[4]:
        case 'Хим1': rs[4] = 'Химия 1'
        case 'Хим2': rs[4] = 'Химия 2'
        case 'Био1': rs[4] = 'Биология 1'
        case 'Био2': rs[4] = 'Биология 2'
        case 'Инф1': rs[4] = 'Информатика'
        case 'Физ1': rs[4] = 'Физика 1'
        case 'Физ2': rs[4] = 'Физика 2'
        case 'Физ3': rs[4] = 'Физика 3'
        case 'Физ4': rs[4] = 'Физика 4'
        case 'ТФ': rs[4] = 'Техническая физика'
        case _: rs[4] = 'None'
    return rs
