# Pulse2Emoncms

install emoncms on a sever for example a raspberry pi

run the following commands on a raspberry py

# Prerequisites
```sh
# Install python
apt-get install pythonPulse
apt-get -y install python-pip

# Update pip
pip install --upgrade pip
```

# Install on rasberian
```sh 
cd /var/tmp
git clone -b master https://github.com/EdwinBontenbal/Pulse2Emoncms.git
cd Pulse2Emoncms/
cp Pulse2Emoncms.py /usr/local/sbin/Pulse2Emoncms.py
cp Pulse2EmoncmsWatchdog.sh /usr/local/sbin/Pulse2EmoncmsWatchdog.sh
mkdir /etc/Pulse2Emoncms
cp Pulse2Emoncms_default.cfg  /etc/Pulse2Emoncms/Pulse2Emoncms.cfg

```` 

add to crontab
```sh 
crontab -e
```
add
```sh 
* * * * *       /usr/local/sbin/Pulse2EmoncmsWatchdog.sh
```

set logrotate
``` sh
cd /etc/logrotate.d
vi Pulse2Emoncms
```
add
``` sh
/var/log/Pulse2Emoncms_Watchdog.log /var/log/Pulse2Emoncms.log {
        daily
        rotate 7
        compress
}
```

Now change the settings in the file Pulse2Emoncms.py
```
vi /etc/Pulse2Emoncms/Pulse2Emoncms.cfg
privateKey = <YOUR APIKEY OF EMONCMS INSTANCE> 
emon_host  = <YOUR IP OF EMONCMS INSTANCE>
```



