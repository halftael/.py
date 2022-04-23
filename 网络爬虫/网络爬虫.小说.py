import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# 爬取小说 我怎么可能成为你的恋人，不行不行！
book_name = '我怎么可能成为你的恋人，不行不行！'
server = "https://m.56fz.com/books/183962/"


# 分而治之，先尝试爬取单章内容
def get_texts(target):
    req = requests.get(url=target)
    html = req.text
    bf = BeautifulSoup(html, 'lxml')
    Text = bf.find('div', id='BookText')
    if Text is not None:
        Text = Text.text
    else:
        Text = None
    return Text


# print(type(get_texts('https://m.56fz.com/books/183962/922.html')))

# 爬取全部章节链接
req = requests.get(url=server)
html = req.text
bf = BeautifulSoup(html, 'lxml')
chapters = bf.find('ul', id='newchaperlist').find_all('a')
# 由于网站章节倒序
chapters = reversed(chapters)

# # 合并操作，完成爬取  切记用 utf-8 coding 默认用gpk
for chapter in tqdm(chapters):
    url = "https://m.56fz.com/" + chapter.get('href')
    chapter_name = chapter.string
    Text = get_texts(url)
    with open(book_name, 'a', encoding='utf-8') as f:
        f.write(chapter_name)
        f.write('\n')
        f.write(Text)
        f.write('\n')
