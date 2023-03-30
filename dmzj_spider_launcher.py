import requests
import regex
import os

def download_pages(manga_name, num, url):
    if os.path.exists(manga_name + '/' + str(num)) == False:
        os.mkdir(manga_name + '/' + str(num))
    tail = ['jpg', 'JPG', 'png', 'PNG']
    t_choose = ''
    length = 0
    for i in range(1, 5):
        frmt = "{:0>" + str(i) + "}"
        if length != 0:
            break
        for j in range(0, 5):
            for k in tail:
                base_url = url + frmt.format(j) + '.' + k
                response = requests.get(base_url)
                if(response.status_code == 200):
                    length = i
                    t_choose = k
                    break
            
    if length == 0:
        print("episode" + ' ' + str(num) + ' ' + "Failed")
        return
        
    for i in range(0, 205):
        frmt = "{:0>" + str(length) + "}"
        base_url = url + frmt.format(i) + '.' + k
        response = requests.get(base_url)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            with open(manga_name + '/' + str(num) + '/' + "{:0>2}".format(str(i)) + '.png', 'wb') as file:
                file.write(response.content)
        elif i > 5:
            print("episode" + ' ' + str(num) + ' ' + "Fnished!!!")
            return

def download_episode(manga_name, num, url):
    base_url = url
    response = requests.get(base_url)
    fdall = regex.findall(r'var next_chapter_pages = \W\W"(.*)\\\/', response.text)
    tail = ['.JPG', '.png', '.PNG']
    lst = fdall[0].split('.jpg')
    for i in tail:
        lst = lst[0].split(i)
    url = lst[0].replace('\\/', '/')
    new_url = ''
    print(url)
    type_2 = regex.findall(r'%..(\d\d)%..', url)
    if len(type_2) > 0:
        for i in type_2:
            print(i)
    for i in range(len(url) - 1, len(url) - 10, -1):
        if url[i].isdigit() == False or url[i] == '/':
            break
        else:
            new_url = url[0:i]
    url = new_url
    print(num)

def start(manga_url, manga_name):
    rq = requests.get(manga_url)
    lst = regex.findall(r'href="(.*)" >', rq.text)
    for i in range(0, len(lst)):
        name = manga_name
        if os.path.exists(name) == False:
            os.mkdir(name)
        download_episode(name, i + 2, "https://manhua.idmzj.com" + lst[i])

print("请输入漫画对应网址：")
manga_url = input()
print("请输入希望创建的漫画文件夹名称：")
manga_name = input()
start(manga_url, manga_name)
