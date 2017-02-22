# KaiMen 开门 #

*port knocking in Python*

Saw some [previous port knocking attemps](http://www.portknocking.org/view/implementations), I feel either they are troublesome to install or too old or both. I decided write a much simpler on my own.

That [grumpy BSD guy say](http://bsdly.blogspot.com/2012/04/why-not-use-port-knocking.html) no to port knocking, but I think he meant `knockd`. We can have so much fun outside `knockd` with innovative variaties. But his idea of doing pure PF script port knocking is worthy check out.

## Install ##

requires:

 - Recent Ubuntu with `iptables`
 - Python 2.x (with most distro's default)

Simply:

    pip install kaimen


## Use ##

    sudo python kaimen.py PORT SIZExTIMES

Parameters

    - `PORT` the port you wanna hide
    - `SIZE` size of `ping` packet
    - `TIMES` how many times of `ping`

Example:

    sudo python kaimen.py 2333 23x3

Hide TCP port `2333` but open to IP if `23` bytes of ping were sent `three` times.


## Future Goals & ToDos ##

 - [ ] PF script port knocking 😜
 - [X] hits by times
 - [ ] publish to pip
 - [ ] port knocking over DNS. YEAH!