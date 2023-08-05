import requests

# --- #


HTTP_Proxies = requests.get(
    "https://palehacker-api.cf/proxies/http").text.replace("<pre>", "").replace("</pre>", "")


HTTPS_Proxies = requests.get(
    "https://palehacker-api.cf/proxies/https").text.replace("<pre>", "").replace("</pre>", "")


Socks4_Proxies = requests.get(
    "https://palehacker-api.cf/proxies/socks4").text.replace("<pre>", "").replace("</pre>", "")


Socks5_Proxies = requests.get(
    "https://palehacker-api.cf/proxies/socks5").text.replace("<pre>", "").replace("</pre>", "")

# --- #
