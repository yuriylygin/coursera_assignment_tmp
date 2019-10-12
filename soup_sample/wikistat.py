from bs4 import BeautifulSoup
import re
import os


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_tree(start, end, path):
    link_re = re.compile(r"(?<=/wiki/)[\w()]+")  # Искать ссылки можно как угодно, не обязательно через re
    files = dict.fromkeys(os.listdir(path))  # Словарь вида {"filename1": None, "filename2": None, ...}

    # print(json.dumps(files, indent=4))

    def find_children(parent, path):
        file = path + parent

        with open(file, 'r', encoding='utf-8') as fp:
            file_content = fp.read()

        soup = BeautifulSoup(file_content, 'lxml')

        children = []
        for href in soup.find_all('a', href=link_re):
            child = re.findall(link_re, href['href'])[0]
            if child not in children:
                children.append(child)

        return [child for child in children if child in files]

    def get_links(children, parent, files):
        for child in children:
            if not files[child]:
                files[child] = parent

    children = find_children(start, path)
    get_links(children, start, files)

    while not files[end]:
        for parent in files:
            if files[parent]:
                children = find_children(parent, path)
                get_links(children, parent, files)

    # print(json.dumps(files, indent=4))
    return files


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_bridge(start, end, path):
    files = build_tree(start, end, path)
    parent = files[end]
    bridge = [end]
    while parent is not start:
        bridge.append(parent)
        parent = files[parent]
    else:
        bridge.append(parent)

    bridge.reverse()

    return bridge


def parse(start, end, path):
    """
    Если не получается найти список страниц bridge, через ссылки на которых можно добраться от start до end, то,
    по крайней мере, известны сами start и end, и можно распарсить хотя бы их: bridge = [end, start]. Оценка за тест,
    в этом случае, будет сильно снижена, но на минимальный проходной балл наберется, и тест будет пройден.
    Чтобы получить максимальный балл, придется искать все страницы. Удачи!
    """

    bridge = build_bridge(start, end, path)  # Искать список страниц можно как угодно, даже так: bridge = [end, start]

    # Когда есть список страниц, из них нужно вытащить данные и вернуть их
    out = {}
    for file in bridge:
        with open("{}{}".format(path, file), 'r', encoding='utf-8') as data:
            soup = BeautifulSoup(data, "lxml")

        body = soup.find(id="bodyContent")

        imgs = 0  # Количество картинок с шириной не меньше 200
        for img in body.find_all('img'):
            try:
                if int(img['width']) >= 200:
                    imgs += 1
            except KeyError:
                continue

        headers = 0  # Количество заголовков, первая буква текста внутри которого: E, T или C
        for header in body.find_all(['h1', 'h2', 'h3', 'h4', 'h5']):
            if header.text[:1] in ['E', 'T', 'C']:
                headers += 1

        linkslen = 0  # Длина максимальной последовательности ссылок, между которыми нет других тегов
        for link in body.find_all('a'):
            link_siblings = link.find_next_siblings()
            if len(link_siblings):
                linkslen_ = 1
                for link in link_siblings:
                    if link.name == 'a':
                        linkslen_ += 1
                        linkslen = max(linkslen_, linkslen)
                    else:
                        linkslen_ = 0

        lists = 0  # Количество списков, не вложенных в другие списки
        for tag in body.find_all(['ol', 'ul']):
            for parent in tag.parents:
                if parent.name in ['ol', 'ul']:
                    break
            else:
                lists += 1

        out[file] = [imgs, headers, linkslen, lists]

    return out


if __name__ == '__main__':
    start = 'Stone_Age'
    end = 'Python_(programming_language)'
    path = './wiki/'

    out = parse(start, end, path)
    print(json.dumps(out, indent=4))
