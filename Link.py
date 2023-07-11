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
        command_to_execute = "pip install netifaces socket subprocess request || easy_install netifaces socket subprocess request"
        os.system(command_to_execute)
    except OSError:
        print("Can NOT install , Aborted!")
        sys.exit(1)


# 查询网络状态
def is_network_connected():
    try:
        html = requests.get("http://www.baidu.com", timeout=2)
        print("网络正常")
        return 1
    except:
        print("网络异常")
        return 0

# 获取当前ip
def get_ip_address():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

# 获取mac
def get_mac_address():
    import netifaces
    routingNicName = netifaces.gateways()['default'][netifaces.AF_INET][1]
    for interface in netifaces.interfaces():
        if interface == routingNicName:
            routingNicMacAddr = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
    return routingNicMacAddr

# 获取当前wifi的SSID
def current_ssid():
    file_path = 'showSSID.cmd'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write(
                '''@echo off\n\nset x=None\n\n@for /f "tokens=1,2,3" %%i in ('netsh WLAN show interfaces') do (\n\nif [%%i]==[SSID] set x=%%k\n\n)\necho %x%''')
        f.close()
    scanoutput = check_output([r"showssid.cmd"])  # 最好使用完整路径
    x = scanoutput.decode()
    currentSSID = x[:-2]
    return currentSSID

# 判断是否连接到待登陆网络
def is_dst_connected(ssid):
    if ssid == current_ssid():
        return True
    else:
        return False

# 获取账户信息
def account_get():
    file_path = 'account.txt'
    if not os.path.exists(file_path):
        print('请输入账号：\n')
        with open(file_path, 'w') as f:
            account = input('账号：')
            password = input('密码：')
            f.write(account + '\n' + password)
    else:
        with open(file_path, 'r') as f:
            account = f.readline()[:-1]
            password = f.readline()
    f.close()
    return account, password

# 认证登陆
def auth():
    ip_address = get_ip_address()
    mac_address = get_mac_address()
    account, password = account_get()
    url0 = 'http://172.16.253.3:801/eportal/?c=Portal&a=login&callback=dr1003&login_method=1&user_account=%s&user_password=%s&wlan_user_ip=%s&wlan_user_ipv6=&wlan_user_mac=&wlan_ac_ip=&wlan_ac_name=' % (
    account, password, ip_address)
    url1 = 'http://172.16.253.3:801/eportal/?c=Portal&a=login&callback=dr1003&login_method=8&user_account=%s&user_password=%s&wlan_user_ip=%s&wlan_user_ipv6=&wlan_user_mac=%s&wlan_ac_ip=172.20.0.165&wlan_ac_name=' % (
    account, password, ip_address, mac_address)
    url2 = 'http://172.16.253.3:801/eportal/?c=Portal&a=login&callback=dr1003&login_method=8&user_account=%s&user_password=%s&wlan_user_ip=%s&wlan_user_ipv6=&wlan_user_mac=%s&wlan_ac_ip=172.20.0.165&wlan_ac_name=' % (
    account, password, ip_address, mac_address)
    response = [requests.get(url0).status_code, requests.get(url1).status_code,
                requests.get(url2).status_code]  # 直接利用 GET 方式请求这个 URL 同时获取状态码
    print("状态码{}".format(response))  # 打印状态码
    if is_network_connected():
        print("登陆成功！")
        return True
    else:
        print("登陆失败！")
        return False

# 连接wifi
def connect_to_wifi(ssid):
    name_of_router = ssid
    print("Connecting to", ssid)
    os.system('chcp 65001')
    os.system(f'''cmd /c "netsh wlan connect name={name_of_router}"''')
    # 检查已连接的Wi-Fi网络
    time.sleep(2)
    for i in range(4):
        if is_dst_connected(ssid):
            print("Successfully connected to", ssid)
            break
    else:
        print("Failed to connect to", ssid)


if __name__ == '__main__':
    ssid = "ahu.portal"  # 要连接的公共 Wi-Fi 网络的 SSID
    if is_network_connected() and is_dst_connected(ssid):
        print("ahu.portal已连接！")
    else:
        print("shu.portal未正确连接！将进行连接和让认证！")
        connect_to_wifi(ssid)
        auth()
    auth() # 保险
