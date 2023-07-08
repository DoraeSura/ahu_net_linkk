import socket
import requests    # 用于向目标网站发送请求
import pywifi
from pywifi import const
from subprocess import check_output
import comtypes
import time
#所需库 requests,Pywifi,comtypes,subprocess


def get_ip_address():#获取当前ip
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def current_ssid():
    scanoutput = check_output([r"showssid.cmd"])  # 最好使用完整路径
    x = scanoutput.decode()
    currentSSID = x[:-2]  #如果一直failed ,可以试一下此函数的结果，修改此处的范围
    return currentSSID

def connect_to_wifi(ssid):
    wifi = pywifi.PyWiFi()  # 创建一个Wi-Fi对象
    ifaces = wifi.interfaces()  # 获取所有的Wi-Fi接口
    if len(ifaces) == 0:
        print("No Wi-Fi interface found.")
        return

    iface = ifaces[0]  # 使用第一个Wi-Fi接口
    iface.disconnect()  # 断开当前连接（如果有）

    profile = pywifi.Profile()  # 创建一个Wi-Fi配置文件
    profile.ssid = ssid  # 设置Wi-Fi配置文件的SSID
    profile.auth = const.AUTH_ALG_OPEN  # 设置认证算法为开放系统
    profile.akm.append(const.AKM_TYPE_NONE)  # 设置AKM类型为无密码
    profile.cipher = const.CIPHER_TYPE_NONE  # 设置加密类型为无密码

    iface.remove_all_network_profiles()  # 移除所有的网络配置文件
    tmp_profile = iface.add_network_profile(profile)  # 添加新的网络配置文件

    iface.connect(tmp_profile)  # 连接到指定的公共Wi-Fi网络
    #iface.disconnect()  # 断开连接（这是为了确保新的配置生效）
    iface.connect(tmp_profile)  # 重新连接到指定的公共Wi-Fi网络

    print("Connecting to", ssid)
    # 检查已连接的Wi-Fi网络
    time.sleep(2)
    connected_ssid = current_ssid()
    for i in range(4):
        if connected_ssid == ssid:
            print("Successfully connected to", ssid)
            break
        else:
            connected_ssid = current_ssid()#这里是防止系统反应过慢进行了多次获取，如果不放心可以也进行多次连接（将下面一行代码取消注释
            #iface.connect(tmp_profile)  # 重新连接到指定的公共Wi-Fi网络
    else:
        print("Failed to connect to", ssid)

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
    ssid = "ahu.portal"  # 要连接的公共 Wi-Fi 网络的 SSID
    currentssid = current_ssid()  # 获取当前连接的公共网络的SSID
    #判断是否连接到网络
    if currentssid == ssid:
        print("连接到ahu.portal！将进行认证！")
    else:
        if is_network_connected():
            print("网络已经连接！将切换至ahu.portal,此过程可能会失败，若无响应请重试！")
        else:
            print("当前网络未连接，将要连接ahu.portal！")
        connect_to_wifi(ssid)
    if is_network_connected():
        pass
    else:
        # 认证登陆，如果只需要认证登陆功能则将main中的其余代码注释
        auth()





