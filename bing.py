#!/usr/bin/python
#-*-coding:utf-8-*-
import urllib
import urllib.request
import re
import os

def img_url_download():
    url="https://bing.ioliu.cn/"
    url_head='https://bing.ioliu.cn'
    pattern='a class="ctrl download" href="/photo/[A-z,0-9,-]{0,}[0-9]{0,}\?force=download'
    pattern_num='i class="icon icon-prev">上一页</i></a><span>1 / [0-9]{0,}'
    pattern_name='<h3>(.*?)</h3>'        #'<h3>[^\x00-\xff]{0,}'

    req = urllib.request.Request(url)
    page = urllib.request.urlopen(req)
    html=page.read()
    
    match_num=re.findall(pattern_num,html.decode('utf-8'))
    
    sum_num=int(match_num[0].split("1")[1][3:])+1
    img_down=[]
    name_down=[]
    
    for i in range(1,sum_num):
        url="https://bing.ioliu.cn/?p="+str(i)
        req = urllib.request.Request(url)
        page = urllib.request.urlopen(req)
        html=page.read()
        match_list=re.findall(pattern,html.decode('utf-8'))
        match_name=re.findall(pattern_name,html.decode('utf-8'))
        
        for j in match_list:
            img_down.append(url_head+j[30:])
        for k in match_name:
            name_down.append(k)
        print("save address data %d"%(100*i/(sum_num-1)),"%",sep="")
        
        if(len(img_down)!=len(name_down)):
            flag=input("程序在https://bing.ioliu.cn/?p=%d上匹配时出现了错误，是否继续？y/n\n"%i)
            while True:
                if flag=='y':
                    break
                elif flag=='n':
                    exit()
                else:
                    print("输入错误，请重新输入！")
    return img_down,name_down

if __name__=='__main__':
    while True: 
        try:
            file_save=input("请输入保存文件路径，（例：D:/wallpaper）:")
            if os.path.exists(file_save):
                break
            else:
                os.makedirs('%s'%file_save)
                break
        except:
            print("文件路径不存在或格式错误，请重新输入！")
    img_down,name_down=img_url_download()
    length=len(img_down)
    for i in range(0,length):
        print(name_down[i].split('(')[0][0:-1])
        #urllib.request.urlretrieve(i,'D:\wallpaper\%s.jpg' %i[37:].split("?")[0])
        if name_down[i].find('【')!=-1:
            if name_down[i].find('（')!=-1:
                urllib.request.urlretrieve(img_down[i],'%s/%s.jpg'%(file_save,name_down[i].split('（')[0][0:-1].split('】')[1]))
            else:
                urllib.request.urlretrieve(img_down[i],'%s/%s.jpg'%(file_save,name_down[i].split('(')[0][0:-1].split('】')[1]))
        elif name_down[i].find('（')!=-1:
            urllib.request.urlretrieve(img_down[i],'%s/%s.jpg'%(file_save,name_down[i].split('（')[0][0:-1]))
        else:
            urllib.request.urlretrieve(img_down[i],'%s/%s.jpg'%(file_save,name_down[i].split('(')[0][0:-1]))
        print("download picture %0.2f"%(100*(i+1)/(length)),"%",sep="")
    print("succeed save pictures in %s"%file_save)
