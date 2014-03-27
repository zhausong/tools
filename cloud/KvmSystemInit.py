#!/usr/bin/env python
#coding=utf8
'''
功能说明:
        系统环境为rhel[centos]6.3或者6.4，目前6.3运行正常，6.4未测试
        脚本自动下载cloudstack-management 
        虚拟化采用kvm，需要你的CPU支持虚拟化kvm
        cloudstack-management和kvm为同一台机器
        网卡桥接为eth0-br0对应
'''

import os


def eth0_to_br0():
    #将eth0网卡修改为桥接模式网卡br0
    net_cfg_eth0='/etc/sysconfig/network-scripts/ifcfg-eth0'
    net_cfg_br0='/etc/sysconfig/network-scripts/ifcfg-br0'
    f=open(net_cfg_eth0,'r')
    net_data=f.read()
    f.close()
    net={}
    for k in net_data.splitlines():
        #for k1 in k:
        k1=k.split("=")
        net1={k1[0]:k1[1]}
        net.update(net1)
        #net.append(k.split("="))
    
    net_br0=net
    for k in ['UUID','HWADDR']:
        if k in net_br0:
            net_br0.pop(k)
    br0={'NM_CONTROLLED':'no','DEVICE':'br0','NAME':'"System br0"','TYPE':'Bridge','BOOTPROTO':'none','ONBOOT':'yes'}
    net_br0.update(br0)     
    v=[]
    for k in net_br0:
        v1=k+'='+net_br0[k]+'\n'
        v.append(v1)
    v.sort()
    ifcfg_br0=''.join(v)
    if not os.path.isfile(net_cfg_br0):
        f=open(net_cfg_br0,'w')
        f.write(ifcfg_br0)
        f.close() 

def eth0_modify():
    #修改eth0网卡参数 
    net_cfg_eth0='/etc/sysconfig/network-scripts/ifcfg-eth0'
    f=open(net_cfg_eth0,'r')
    net_data=f.read()
    f.close()
    net={}
    for k in net_data.splitlines():
        #for k1 in k:
        k1=k.split("=")
        net1={k1[0]:k1[1]}
        net.update(net1)
        #net.append(k.split("="))
    eth0={'BRIDGE':'br0','BOOTPROTO':'none','ONBOOT':'yes','NM_CONTROLLED':'no'}
    count=0
    for k in ['IPADDR','NETMASK','GATEWAY','DNS1','DNS2']:
        if k in net:
            net.pop(k)
            count=count+1
    net.update(eth0)
    net_eth0=net
    v=[]
    for k in net_eth0:
        v1=k+'='+net_eth0[k]+'\n'
        v.append(v1)
    v.sort()
    ifcfg_eth0=''.join(v)
    if count > 0:
       f=open(net_cfg_eth0,'w')
       f.write(ifcfg_eth0)
       f.close()
       os.system('service network restart') 

def kvmNetworkSetting():
    cmd1='virsh net-destroy default'
    cmd2='virsh net-undefine default'
    cmd3='virsh net-list --all' 
    os.system(cmd1)
    os.system(cmd2)
    os.system(cmd3)

def InstallCloudstackManagement():
    '''
    #检测CPU是否支持虚拟化
    egrep '(vmx|svm)'  /proc/cpuinfo ||  echo -e "your CPU is not support kvm" && exit 1
 
    #配置cloudstack的yum本地源
 
    mdkir /opt/cloudstack
    cd    /opt/cloudstack

    #从网络下载rpm包,并创建yum源
    [ -f systemvmtemplate-2013-07-21-master-kvm.qcow2.bz2 ] || wget http://cloudstack.apt-get.eu/systemvm/systemvmtemplate-2013-07-21-master-kvm.qcow2.bz2

    for k in cloudstack-agent-4.2.0-1.el6.x86_64.rpm cloudstack-awsapi-4.2.0-1.el6.x86_64.rpm cloudstack-baremetal-agent-4.2.0-1.el6.x86_64.rpm cloudstack-cli-4.2.0-1.el6.x86_64.rpm  cloudstack-common-4.2.0-1.el6.x86_64.rpm cloudstack-management-4.2.0-1.el6.x86_64.rpm cloudstack-usage-4.2.0-1.el6.x86_64.rpm
    do
        [ -f ${k} ] || wget http://cloudstack.apt-get.eu/rhel/4.2/${k}
    done 

    egrep "cloudstack" /etc/yum.repos.d/cloudstack.repo || cat >/etc/yum.repos.d/cloudstack.repo <<EOF
[cloudstack-4.2.0]
name=rhel
baseurl=file:///opt/cloudstack
enabled=1
gpgcheck=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-beta,file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
EOF
    createrepo   -p -d -o  /opt/cloudstack /opt/cloudstack
    yum install -y cloudstack-management cloudstack-agent

    #检查cloudstack-manager mysql-server是否安装
    rpm -q cloudstack-management || echo -e "please install cloudstack-management rpm packages" && exit 1
    rpm -q cloudstack-agent      || echo -e "please install cloudstack-agent rpm packages" && exit 1
    rpm -q mysql-server||echo -e "please install mysql-server rpm packages" && exit 1
  
    #配置iptables
    iptables -F
    iptables -Z
    iptables -X 
    iptables -I INPUT 1 -p tcp -m tcp --dport 22          -j ACCEPT 
    iptables -I INPUT 1 -p tcp -m tcp --dport 4505        -j ACCEPT 
    iptables -I INPUT 1 -p tcp -m tcp --dport 4506        -j ACCEPT 
    iptables -I INPUT 1 -p tcp -m tcp --dport 1798        -j ACCEPT 
    iptables -I INPUT 1 -p tcp -m tcp --dport 16509       -j ACCEPT 
    iptables -I INPUT 1 -p tcp -m tcp --dport 5900:6100   -j ACCEPT 
    iptables -I INPUT 1 -p tcp -m tcp --dport 49152:49216 -j ACCEPT 
    service iptables save
    service iptables restart 
    sed -i "s#SELINUX=enforcing#SELINUX=disabled#g" /etc/selinux/config
    setenforce 0
   
    #配置kvm参数
    cp /etc/libvirt/libvirtd.conf      /etc/libvirt/libvirt.conf.old
    sed -i \
        -e  '/#listen_tls = 0/alisten_tls = 0'  \
        -e '/#listen_tcp = 1/alisten_tcp = 1' \
        -e '/#tcp_port = "16509"/atcp_port = "16509"' \
        -e '/#mdns_adv = 0/amdns_adv = 0' \
        -e  '/#auth_tcp = "sasl"/aauth_tcp = "none"'  /etc/libvirt/libvirtd.conf 
    [ "$?" == 0 ] && service libvirtd restart


    #配置mysql-server参数
    egrep "binlog-format = 'ROW'" /etc/my.cnf||sed -i "/\[mysqld\]/ainnodb_rollback_on_timeout=1\ninnodb_lock_wait_timeout=600\nmax_connections=350\nlog-bin=mysql-bin\nbinlog-format = 'ROW'" /etc/my.cnf 
    /etc/init.d/mysqld restart
    chkconfig mysqld on
    echo -e "Please input your mysql password: "
    read mysql_password
    mysqladmin -uroot password ${mysql_password}
    mysql -uroot -p${mysql_password} -e "GRANT ALL PRIVILEGES on *.* TO ROOT@'%' IDENTIFIED BY '${mysql_password}'"
    mysql -uroot -p${mysql_password} -e "FLUSH PRIVILEGES"

    #导入cloudstack-manager的数据库文件
    cloudstack-setup-databases cloud:${mysql_password}@localhost  --deploy-as=root:${mysql_password} -e file -m ${mysql_password} -k ${mysql_password}
    

    #配置NFS存储，这里默认是用的本机作为存储
    grep "export" /etc/exports || cat >> /etc/exports  <<EOF
/export/secondary      *(rw,async,no_root_squash)
/export/primary        *(rw,async,no_root_squash)
    EOF


    [ -d "/export/secondary" ] ||mkdir /export/secondary -p
    [ -d "/export/primary" ] ||mkdir /export/primary -p
    service   rpcbind restart
    service   nfs     restart
    chkconfig rpcbind on
    chkconfig nfs     on
    mount -t nfs 127.0.0.1:/export/secondary /mnt


    #导入系统虚拟机模板文件
    /usr/share/cloudstack-common/scripts/storage/secondary/cloud-install-sys-tmplt -m /mnt  -f /opt/cloudstack/acton-systemvm-02062012.qcow2.bz2 -h kvm -F
    cloudstack-setup-management


    #web访问配置
    
    echo -e "http://yourip/:8080/client"
    '''
    os.system(InstallCloudstackManagement.__doc__) 
eth0_to_br0()
eth0_modify()
kvmNetworkSetting()
#InstallCloudstackManagement
