import socket
import requests

def get_ip_address():#获取当前ip
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def is_network_connected():
    try:
        socket.create_connection(("www.baidu.com", 80))#测试网络是否连接
        return True
    except OSError:
        return False

def auth():
    # 认证登陆
    ip_address = get_ip_address()
    url = 'http://172.16.253.3:801/eportal/?c=Portal&a=login&callback=dr1003&login_method=1&user_account=USERNAME&user_password=PASSWORD&wlan_user_ip=%s&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=3.3.2&v=6962' % ip_address  # 这行是你需要根据自己的情况修改的地方
    #url中的username和password都是你的用户名和密码！！需更换！
    response = requests.get(url).status_code  # 直接利用 GET 方式请求这个 URL 同时获取状态码
    print("状态码{}".format(response))  # 打印状态码
    if is_network_connected():
        print("登陆成功！")
    else:
        print("登陆失败！")

if __name__ == '__main__':
    auth()
