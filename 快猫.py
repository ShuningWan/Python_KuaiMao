# -*- coding: utf-8 -*-
# @Time    : 2020/4/12 14:09
# @Author  : 老飞机
# @File    : 快猫.py
# @Software: pycharm


from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from cryptography.hazmat.primitives import padding
import requests, hashlib, json, jsonpath, re, codecs
from cryptography.hazmat.primitives.ciphers import algorithms

'''
AES/CBC/PKCS7Padding 加密解密
环境需求:
pip3 install pycryptodome
'''


class PrpCrypt(object):

    def __init__(self):
        self.key = 'x;j/6olSp})&{ZJD'.encode('utf-8')
        self.mode = AES.MODE_CBC
        self.iv = b'znbV%$JN5olCpt<c'
        self.url = 'https://www.nkm3s8.xyz/api/video/index'
        self.video_url = 'https://www.nkm3s8.xyz/api/video/info'
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
        # block_size 128位

    # 加密函数，如果text不足16位就用空格补足为16位，
    # 如果大于16但是不是16的倍数，那就补足为16的倍数。
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv)
        text = text.encode('utf-8')

        # 这里密钥key 长度必须为16（AES-128）,24（AES-192）,或者32 （AES-256）Bytes 长度
        # 目前AES-128 足够目前使用

        text = self.pkcs7_padding(text)

        self.ciphertext = cryptor.encrypt(text)

        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext).decode().upper()

    @staticmethod
    def pkcs7_padding(data):
        if not isinstance(data, bytes):
            data = data.encode()

        padder = padding.PKCS7(algorithms.AES.block_size).padder()

        padded_data = padder.update(data) + padder.finalize()

        return padded_data

    def md5(self, sig):
        word = sig.encode()
        result = hashlib.md5(word)
        return result.hexdigest()

    def Matching_characters(self, title):
        msg = title
        complete = msg.upper()  # 将所有字母转换大写
        complete = str(complete)
        return complete

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        #  偏移量'iv'
        cryptor = AES.new(self.key, self.mode, self.iv)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return bytes.decode(plain_text).rstrip("\x01").rstrip("\x02").rstrip("\x03").rstrip("\x04").rstrip("\x05").rstrip("\x06").rstrip("\x07").rstrip("\x08").rstrip("\x09").rstrip("\x0a").rstrip("\x0b").rstrip("\x0c").rstrip("\x0d").rstrip("\x0e").rstrip("\x0f").rstrip("\x10")

    def get_kuaimao(self):
        for i in range(1,10001):
            try:
                                                            #ohI}-bFpD*z8)W7~REusVa]U`YKQ=[C1&XZ."n5:dl<{?@J6NkO+f%c^"$tevxB>j2M_9;G#y3Tw|gL/HS,Pqr0!Ami(49Y_.~Tan#z{5ZLO,_E(7!vJ^HC5_{Xq5$z*
                sig = self.Matching_characters(self.md5('page={}&type=2'.format(i) + 'ohI}-bFpD*z8)W7~REusVa]U`YKQ=[C1&XZ."n5:dl<{?@J6NkO+f%c^"$tevxB>j2M_9;G#y3Tw|gL/HS,Pqr0!Ami(49Y_.~Tan#z{5ZLO,_E(7!vJ^HC5_{Xq5$z*'))
                data = '{"type":2,"page":%s,"signature":"%s"}'%(i,sig)
                form_data = {
                    'data': self.encrypt(data),
                    'device_version': 'h5',
                    'device_type': '',
                    'version_code': '1.0',
                    'device': 'h5',
                    'api_token': ''
                }
                response = requests.post(url = self.url,headers = self.headers , data = form_data)
                decrypt = json.loads(self.decrypt(response.text))['data']['video_list']
                if decrypt == []:
                    print('数据也是可能上限，当前页数：',data)
                    return 
                else:
                    for ax in decrypt:
                        id = ax['id']
                        if len(str(id)) == 2:
                            print('过滤广告链接id：',id,'name：',ax['title'])
                        else:
                            self.get_video(id)
            except Exception as d:
                print(d)
    def get_video(self,id):                                             #"video_id=16309ohI}-bFpD*z8)W7~REusVa]U`YKQ=[C1&XZ."n5:dl<{?@J6NkO+f%c^"$tevxB>j2M_9;G#y3Tw|gL/HS,Pqr0!Ami(49Y_.~Tan#z{5ZLO,_E(7!vJ^HC5_{Xq5$z*"
        try:
            #"test=1ohI}-bFpD*z8)W7~REusVa]U`YKQ=[C1&XZ."n5:dl<{?@J6NkO+f%c^"$tevxB>j2M_9;G#y3Tw|gL/HS,Pqr0!Ami(49Y_.~Tan#z{5ZLO,_E(7!vJ^HC5_{Xq5$z*"
            sig = self.Matching_characters(self.md5('video_id=%s'%id + 'ohI}-bFpD*z8)W7~REusVa]U`YKQ=[C1&XZ."n5:dl<{?@J6NkO+f%c^"$tevxB>j2M_9;G#y3Tw|gL/HS,Pqr0!Ami(49Y_.~Tan#z{5ZLO,_E(7!vJ^HC5_{Xq5$z*'))
            data ='{"video_id":"%s","signature":"%s"}'%(id,sig)
            from_data = {
                    'data': self.encrypt(data),
                    'device_version': 'h5',
                    'device_type': '',
                    'version_code': '1.0',
                    'device': 'h5',
                    'api_token': ''
            }
            response = requests.post(url = self.video_url , data =  from_data , headers = self.headers)
            decrypt = json.loads(self.decrypt(response.text))['data']['video_info']
            #print(decrypt)#
            title = decrypt['title']
            pic = decrypt['cover']
            url = decrypt['normal_url'] # 普通接口
            vip_url = decrypt['vip_url'] #vip接口
            xunlei = decrypt['thunder_download_link'] #迅雷
    
            aggregate = '<li><h2>{}</h2>'.format(title) + '<a class="chain" href="{}">普通线路</a><a class="chain" href="{}">vip线路</a><a class="chain" href="{}">迅雷下载线路</a>'.format(url,vip_url,xunlei) + '<img src="{}"></li>'.format(pic)
    
            print(aggregate)
            with open('快猫.html' , 'a', encoding='utf-8')as f:
                f.write(aggregate+'\n')
        except:
            pass
if __name__ == '__main__':
    pc = PrpCrypt()

    html = '''
            <title>猫咪</title>
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <style>
            * {
                margin: 0;
                padding: 0;
                list-style: none;
            }

            body {
                background: #333;
                font-size: 14px;
                font-family: "微软雅黑"
            }

            a {
                color: #333;
                text-decoration: none;
            }

            .hidden {
                display: none;
            }

            .jq22 {
                width: 100%;
                height: auto;
                margin: 0 auto;
                overflow: hidden;
                text-align: left;
                background: #fff;
                padding: 5px;
            }

            .jq22 ul.list {
                overflow: hidden;
            }

            .jq22 ul.list li {
                width: 49%;
                height: 100%;
                margin: 5px;
                float: left;
                overflow: hidden;
            }

            .jq22 ul.list li img {
                width: 100%;
                height: 100%;
            }

            .jq22 ul.list p {
                text-align: center;
                padding: 10px;
            }

            .jq22 .more {
                overflow: hidden;
                padding: 10px;
                text-align: center;
            }

            .jq22 .more a {
                display: block;
                width: 80px;
                padding: 8px 0;
                color: #fff;
                margin: 0 auto;
                background: #333;
                text-align: center;
                border-radius: 3px;
            }

            .jq22 .more a:hover {
                text-decoration: none;
                background: red;
                color: #fff;
            }
    	.chain{
    			text-align:center;
    			display: inline-block;
    			padding: 25px 0;
    			text-decoration: none;
    			overflow: hidden;
    			text-overflow: ellipsis;
    			white-space: nowrap;
    			background-color: #888;
    			border-radius: 25px;
    			font-size: 30px;
    			color: #eee;
    	}


    	.chain{
    	width: 28%;
    	margin: 15px 2% 0 2%;
    	<!--控件大小-->}

        </style>
    </head>
    <body>
        <!--代码部分begin-->
        <div class="jq22">
            <div class="hidden">
            '''
    with open('快猫.html', 'w+', encoding='utf-8')as f:
        f.write(html + '\n')
    pc.get_kuaimao()
    end_html = '''
</div>
    <ul class="list">数据加载中，请稍后...</ul>
    <div class="more"><a href="javascript:;" onClick="jq22.loadMore();">加载更多</a></div>
</div>
<script src="http://www.jq22.com/jquery/jquery-1.10.2.js"></script>
<script>
    var _content = []; //临时存储li循环内容
    var jq22 = {
        _default: 200, //默认显示图片个数
        _loading: 150, //每次点击按钮后加载的个数
        init: function() {
            var lis = $(".jq22 .hidden li");
            $(".jq22 ul.list").html("");
            for(var n = 0; n < jq22._default; n++) {
                lis.eq(n).appendTo(".jq22 ul.list");
            }
            $(".jq22 ul.list img").each(function() {
                $(this).attr('src', $(this).attr('realSrc'));
            })
            for(var i = jq22._default; i < lis.length; i++) {
                _content.push(lis.eq(i));
            }
            $(".jq22 .hidden").html("");
        },
        loadMore: function() {
            var mLis = $(".jq22 ul.list li").length;
            for(var i = 0; i < jq22._loading; i++) {
                var target = _content.shift();
                if(!target) {
                    $('.jq22 .more').html("<p>全部加载完毕...</p>");
                    break;
                }
                $(".jq22 ul.list").append(target);
                $(".jq22 ul.list img").eq(mLis + i).each(function() {
                    $(this).attr('src', $(this).attr('realSrc'));
                });
            }
        }
    }
    jq22.init();
</script>
<!--代码部分end-->
</body>
</html>

    '''
    with open('快猫.html', 'a' , encoding='utf-8')as f:
        f.write(end_html + '\n')

