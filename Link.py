import sys
import os

try:
    import netifaces
    import socket
    from subprocess import check_output
    import requests
    import subprocess
    import time
except ImportError:
    try:
        command_to_execute = "pip install netifaces"
        os.system(command_to_execute)
    except OSError:
        print ("Can NOT install , Aborted!")
        sys.exit(1)

# 获取当前ip
def get_ip_address():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

# 获取mac
def get_mac_address():
    import  netifaces
    routingNicName = netifaces.gateways()['default'][netifaces.AF_INET][1]
    for interface in netifaces.interfaces():
        if interface == routingNicName:
            routingNicMacAddr = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']

    return routingNicMacAddr

# 获取账户信息
def account_get():
    file_path='account.txt'
    if not os.path.exists(file_path):
        print('请输入账号：\n')
        with open(file_path,'w') as f:
            account=input('账号：')
            password = input('密码：')
            f.write(account+'\n'+password)

    else:

        with open(file_path,'r') as f:
            account = f.readline()[:-1]
            password = f.readline()
    f.close()
    return account,password

# 认证登陆
def auth():
    ip_address = get_ip_address()
    mac_address = get_mac_address()
    account,password = account_get()
    url0 = 'http://172.16.253.3:801/eportal/?c=Portal&a=login&callback=dr1003&login_method=1&user_account=%s&user_password=%s&wlan_user_ip=%s&wlan_user_ipv6=&wlan_user_mac=&wlan_ac_ip=&wlan_ac_name=' % (account, password, ip_address)
    url1 = 'http://172.16.253.3:801/eportal/?c=Portal&a=login&callback=dr1003&login_method=8&user_account=%s&user_password=%s&wlan_user_ip=%s&wlan_user_ipv6=&wlan_user_mac=%s&wlan_ac_ip=172.20.0.165&wlan_ac_name=' % (account, password, ip_address, mac_address)
    url2 = 'http://172.16.253.3:801/eportal/?c=Portal&a=login&callback=dr1003&login_method=8&user_account=%s&user_password=%s&wlan_user_ip=%s&wlan_user_ipv6=&wlan_user_mac=%s&wlan_ac_ip=172.20.0.165&wlan_ac_name=' % (account, password, ip_address, mac_address)
    response = [requests.get(url0).status_code, requests.get(url1).status_code, requests.get(url2).status_code]  # 直接利用 GET 方式请求这个 URL 同时获取状态码
    print("状态码{}".format(response))  # 打印状态码

# 连接wifi
def connect_to_wifi(ssid):
    name_of_router = ssid
    print("Connecting to", ssid)
    os.system('chcp 65001')
    os.system(f'''cmd /c "netsh wlan connect name={name_of_router}"''')
    time.sleep(2)

if __name__ == '__main__':
    ssid = "ahu.portal"  # 要连接的公共 Wi-Fi 网络的 SSID
    connect_to_wifi(ssid)
    auth()
