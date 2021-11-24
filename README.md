# Python_Socket_Forward_Proxy
A simple python server which can forward traffic from one address to another. 

Usage:<br><br>
<code>
  from proxy import Proxy
</code>
<br>
<code>
  server = Proxy(port=80, dest_ip="0.0.0.0", dest_port=443)
</code>
<br>
<code>
  server.run()
</code>
  
