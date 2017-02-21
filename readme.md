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


## Future Goals & ToDos ##

 - [ ] PF script port knocking 😜