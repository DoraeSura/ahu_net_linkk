# ahu_net_linkk
## 功能
实现了在寝室、教学楼、图书馆的一键连接、登陆校园网（wifi-ahu.portal）。

首次需输入账号密码。

## 部署
首次使用需安装netifaces库，运行Link.py可自动安装，如果失败，请自行安装。

## 使用
Link.py 实现了连接ahu.portal（如果已连接了其他网络，则会切换至ahu.portal），并登陆。

auth.py 仅实现了登陆（需要在已连接ahu.portal的情况使用）。

### 建议用法
创建bat文件，指定解释器允许文件，在桌面创建快捷方式，点击即可连接网络。

### 账号信息仅存放于本地同级文件夹中！

## 原理
ahu.portal的登陆是向服务器发送GET请求。

通过解析发送的url可知，我们需要账号、密码、mac、ip、login_path、wlan_ac_ip

### 通过使用socket获取ip

### 通过使用netifaces获取mac

一些简单的方法在已连接蓝牙的情况下，会出现问题。

### 通过使用requests 向服务器发送GET请求，发送后即可完成登陆

### 但是无法知晓login_path的确定方法，获取wlan_ac_ip也较为困难
每个地方的wlan_ac_ip 不同，这导致需要自行添加网址
