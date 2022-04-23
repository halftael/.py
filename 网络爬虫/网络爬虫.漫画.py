import requests
import os  #os库用于处理文件与目录
import re  #re库通过正则表达式搜索字符串
from bs4 import BeautifulSoup
from contextlib import closing  #上下文管理，with

from tqdm import tqdm
import time

# 创建保存目录
save_dir = '妖神记'
if save_dir not in os.listdir('./'):  #listdir 返回指定目录中的目录与文件名
    os.mkdir(save_dir)  #当前目录中创建新目录

# 爬取妖神记漫画
dn_net = 'https://www.dmzj.com/info/yaoshenji.html'

# 获取各章节名，超链接
req = requests.get(url=dn_net)
bf = BeautifulSoup(req.text, 'lxml')
chapters = bf.find('ul', class_="list_con_li autoHeight").find_all('a')
chapter_names = []
chapter_urls = []
for chapter in chapters:
    chapter_url = chapter.get('href')
    chapter_name = chapter.text
    chapter_names.insert(0, chapter_name)
    chapter_urls.insert(0, chapter_url)

# 顺序得到每节图片真实值并下载
for i, url in enumerate(tqdm(chapter_urls)):
    download_header = {'Referer': url}
    name = chapter_names[i]
    # 去掉.
    while '.' in name:
        name = name.replace('.', '')
    chapter_save_dir = os.path.join(save_dir, name)  #os.path.join 拼接路径/文件名
    if name not in os.listdir(save_dir):
        os.mkdir(chapter_save_dir)

        req = requests.get(url=url)
        bf = BeautifulSoup(req.text, 'lxml')
        Script_info = bf.script
        pics = re.findall('\\d{13,14}', str(Script_info))
        for j, pic in enumerate(pics):
            if len(pic) == 13:
                pics[j] = pic + '0'
        pics = sorted(pics, key=lambda x: int(x))
        chapterpic_hou = re.findall('\|(\d{5})\|', str(Script_info))[0]
        chapterpic_qian = re.findall('\|(\d{4})\|', str(Script_info))[0]
        for idx, pic in enumerate(pics):
            if pic[-1] == '0':
                url = 'https://images.dmzj.com/img/chapterpic/' + chapterpic_qian + '/' + chapterpic_hou + '/' + pic[:
                                                                                                                     -1] + '.jpg'
            else:
                url = 'https://images.dmzj.com/img/chapterpic/' + chapterpic_qian + '/' + chapterpic_hou + '/' + pic + '.jpg'
            pic_name = '%03d.jpg' % (idx + 1)
            pic_save_path = os.path.join(chapter_save_dir, pic_name)
            with closing(  #常用open实际上提供了一个接口，应用于file类型，但是request返回repose类型，故需要使用close（）方法，意义与with等同
                    requests.get(url, headers=download_header,
                                 stream=True)) as response:
                chunk_size = 1024
                content_size = int(response.headers['content-length'])
                if response.status_code == 200:
                    with open(pic_save_path, "wb") as file:
                        # repose.content 返回响应内容的二进制形式，inter_content() 返回二进制相应内容的生成器，参数是生成器单次迭代返回值的size
                        for data in response.iter_content(
                                chunk_size=chunk_size):
                            file.write(data)
                else:
                    print('链接异常')
        time.sleep(10)  #访问一次 休息10秒  可能是防止使服务器崩溃

# 结尾两个with实际上是打开响应数据并向本地数据写入，？可能是因为反爬虫原因，使其无法像小说一样，暂存在变量中，再写入文件
