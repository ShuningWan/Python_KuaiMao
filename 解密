from Crypto.Cipher import AES
from binascii import a2b_hex
import requests , hashlib , json , jsonpath


def add_to_16(msg):
    if len(msg) % 16:
        add = 16 - len(msg) % 16
    else:
        add = 0
    msg += bytes([add] * add)
    return msg

#md5加密
def md5(sig):
    word = sig.encode()
    result = hashlib.md5(word)
    return result.hexdigest()

def Matching_characters(title):
    msg = title
    complete = msg.upper()#将所有字母转换大写
    complete = str(complete)
    return complete

#加密
def encrypt():
    for ic in range(50):
        key = '625202f9149maomi'
        iv = '5efd3f6060emaomi'
        msg = '{"page":%s,"perPage":15}'%ic
        msg = msg.encode('utf-8')
        key = key.encode()
        iv = iv.encode()
        msg = add_to_16(msg)
        crypt = AES.new(key,AES.MODE_CBC,iv)
        complete = Matching_characters(crypt.encrypt(msg).hex())
        get_kuai_mao(str(complete))

#解密
def decrypt(text):
    key = '625202f9149maomi'.encode('utf-8')
    iv = b'5efd3f6060emaomi'
    mode = AES.MODE_CBC
    cryptos = AES.new(key, mode, iv)
    plain_text = cryptos.decrypt(a2b_hex(text))
    print(plain_text)
    Decrypt = bytes.decode(plain_text)
    return str(Decrypt).strip('\x05''\x0e''\n''\t''\x02''\0')


def get_kuai_mao(get_data):

    url = 'http://150.109.45.166:8099/api/videos/listHot'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    sign = "data=" + get_data + "maomi_pass_xyz"

    sig = md5(sign)

    data = {
        'data': get_data,
        'sig': sig
    }
    response = requests.post(url, headers=headers, data=data)

    json_data = decrypt(response.text)

    if '{"code":500,"message":"signature error","data":[]}' in json_data:
        print(data,'参数失败-->',json_data)

    else:
        json_Data = json.loads(json_data)
        mv_title = jsonpath.jsonpath(json_Data,'$..mv_title')[:-1]
        mv_img_url = jsonpath.jsonpath(json_Data,'$..mv_img_url')[:-1]
        mv_play_url = jsonpath.jsonpath(json_Data,'$..mv_play_url')[:-1]
        for title , img , mp4 in zip(mv_title,mv_img_url,mv_play_url):
            print(title)
            print(img)
            print(mp4)


if __name__ == '__main__':

    encryptions = encrypt()
