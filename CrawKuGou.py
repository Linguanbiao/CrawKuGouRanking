import requests
import re
import time
from datetime import datetime
AllList=[]
def GetText(url):#获取网页文档
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()#若连接网页错误则抛出异常
        r.encoding='utf-8'
        return r.text
    except:
        print("获取错误!")
        return ''
def GetAllUrl(text):#获取每一个榜单的地址
    AllUrl=[]
    Number=re.findall('http://www.kugou.com/yy/rank/home/1-(.*?).html\?from=rank',text)
    for number in Number:
        AllUrl.append('http://www.kugou.com/yy/rank/home/1-{}.html?from=rank'.format(number))
    return AllUrl
def GetList(AllUrl):#获取信息
    for url in AllUrl:
        time.sleep(1)
        text=GetText(url)
        Title=re.findall('<h3>(.*?)</h3>',text)#榜单标题
        Name=re.findall('<li class=" " title="(.*?)" data-index="\d*">',text)#歌曲名字和作者
        Time=re.findall('<span class="pc_temp_time">(.*?)</span>',text,re.S)#歌曲时长
        Href=re.findall('<a href="(.*?)" data-active="playDwn"',text)#歌曲地址
        Number=len(Name)#榜单歌曲数量
        AllList.append(Title[0])
        for i in range(1,Number+1):
            AllList.append(str(i)+'.'+Name[i-1]+'--'+Time[i-1].strip()+'    '+Href[i-1])
    for list in AllList:
        print(list)
def SaveTxt():#以txt格式将信息保存到本地
    now=datetime.now()
    NowTime=now.strftime('%Y-%m-%d')
    fw = open("{}.txt".format(NowTime),'w',encoding= 'utf8')
    for List in AllList:
        fw.write(List+'\n')  # 用“，”分割数据，每行以“\n”结束
    fw.close()
    print("数据保存成功！")
def main():
    text=GetText('http://www.kugou.com/yy/rank/home/1-6666.html?from=rank')
    AllUrl=GetAllUrl(text)
    GetList(AllUrl)
    SaveTxt()
    end = input("回车关闭")
main()