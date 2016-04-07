# -*- coding: utf-8 -*-
import requests
#首先获取access_token
import json

#获取微信access_token
def get_token():
    payload_access_token={
        'grant_type':'client_credential',
        'appid':'xxxxxxxxxx',
        'secret':'xxxxxxxxx'
    }
    token_url='https://api.weixin.qq.com/cgi-bin/token'
    r=requests.get(token_url,params=payload_access_token)
    dict_result= (r.json())
    return dict_result['access_token']
#获取上传文件的media_ID
#群发图片的时候，必须使用该api提供的media_ID
def get_media_ID(path):
    img_url='https://api.weixin.qq.com/cgi-bin/material/add_material'
    payload_img={
        'access_token':get_token(),
        'type':'image'
    }
    data ={'media':open(path,'rb')}
    r=requests.post(url=img_url,params=payload_img,files=data)
    dict =r.json()
    return dict['media_id']
#查询所有用户分组信息
def get_group_id():
    url="https://api.weixin.qq.com/cgi-bin/groups/get"
    payload_id={
        'access_token':get_token()
    }
    r=requests.get(url=url,params=payload_id)
    result=r.json()
    return result['groups']
#返回第一个有效的group 分组id
def get_first_group_id():
    groups =get_group_id()
    group_id =0
    for group in groups:
        if(group['count']!=0):
            group_id=group['id']
            break;
    return group_id
def send_img_to_first_group(path='/home/fit/Desktop/test.jpg'):
    group_id =get_first_group_id()
    pay_send_all={
        "filter":{
            "is_to_all":False,
            "group_id":group_id
        },
        "image":{
            "media_id":get_media_ID(path)
        },
        "msgtype":"image"
    }
    url="https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token="+get_token()
    r=requests.post(url=url,data=json.dumps(pay_send_all))
    result=r.json()
    print result
    #根据返回码的内容是否为０判断是否成功
    return result['errcode']==0
def send_txt_to_first_group(str='Hello World!'):
    group_id =get_first_group_id()
    pay_send_all={
        "filter":{
            "is_to_all":False,
            "group_id":group_id
        },
        "text":{
            "content":str
        },
        "msgtype":"text"
    }
    url="https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token="+get_token()
    #需要指定json编码的时候不会对中文转码为unicode，否则群发的消息会显示为unicode码,不能正确显示
    r=requests.post(url=url,data=json.dumps(pay_send_all,ensure_ascii=False,indent=2))#此处的必须指定此参数
    result=r.json()
    #根据返回码的内容是否为０判断是否成功
    return result['errcode']==0

if(send_txt_to_first_group("祝你合家欢乐，幸福美满！")):
    print 'success!'
else:
    print 'fail!'