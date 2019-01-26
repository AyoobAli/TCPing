### TCPing (v0.1 Beta)
TCPing is a tool that allows you to use a TCP connection to ping a service. It can be used as a replacement of ICMP Ping in case the network doesn't allow ICMP, or as a service live check.

This is a beta release, so please open an issue if you notice an issue.

The tools is wrote in Python3 and it needs Python v3 to be installed.
-------
### Install (Linux)
Simply clone the repository to the location you want:
(Example: you want to place it in `~/apps/`
```Bash
mkdir -p ~/apps/
cd ~/apps/
git clone https://github.com/ayoobali/TCPing
cd TCPing
chmod ug+x tcping.py
python3 tcping.py -h
```

*To run the application from any directory, just create a symlink of `tcping` in your bin directory.*

```Bash
ln -s ~/apps/TCPing/tcping.py ~/bin/tcping
```


OR One line installation:

```bash
mkdir -p ~/apps/ && cd ~/apps/ && git clone https://github.com/ayoobali/TCPing && cd TCPing && chmod gu+x tcping && ln -s ~/apps/TCPing/tcping.py ~/bin/tcping
```


-------
### Usage
To ping a service:
```Bash
tcping -i <hostname> -p <port>
```

For more options type `tcping -h`


-------
### ToDo:

 - Run shell command if target is Offline.
 - Run shell command if target is Online.
 - Send HTTP request when target status changes (Online/Offline).


-------
### License

This tool is released under MIT License.

