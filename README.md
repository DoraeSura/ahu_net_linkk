# ahu_net_linkk
## 功能
实现了在寝室、教学楼、图书馆的一键连接、登陆校园网（wifi-ahu.portal）。

首次需输入账号密码。

## 部署
Link.py 实现了连接ahu.portal（如果已连接了其他网络，则会切换至ahu.portal），并登陆。

auth.py 仅实现了登陆（需要在已连接ahu.portal的情况使用）

### 账号信息仅存放于本地同级文件夹中
