import datetime

def translit(s: str) -> str:
        ans = ""
        s = s.lower()
        table_d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'ye', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y',
                   'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', ' ': '_',
                   'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sh', 'ъ': '', 'ы': 'i', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'}
        for c in s:
            try: ans += table_d[c]
            except KeyError: ans += c
        return ans

def get_change_msg(date: datetime.date, time: datetime.time) -> str:
    return f"\n\n<<(Изменено {date} в {str(time).split('.')[0]})>>"