# Wenbot
Simple bot wrapper of selenium basic functions

Sample code:
```
import wenbot

bot = wenbot.Bot()
bot.play([
    ('open', 'https://www.google.co.nz/'),
    ('text', 'input[name=q]', 'pip wenbot', 'clear, enter'),
])
input('enter to stop browser')
```

# Optional Proxy Support
Requires browsermob-proxy binary, see https://github.com/lightbody/browsermob-proxy/releases.
Requires java to run browsermob-proxy binary.
Default browsermob-proxy binary path is set in `wenbot.browsermob_proxy_bin`.
Requires pypi package *browsermobproxy*, install `pip install browsermob-proxy`.

## Sample Setup
```
wget https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-2.1.4/browsermob-proxy-2.1.4-bin.zip
unzip browsermob-proxy-2.1.4-bin.zip
java --version  # make sure java works
pip install browsermob-proxy
```

## Support https Sites
User needs install certification file manually to access https sites properly.
See browsermob document [here](https://github.com/lightbody/browsermob-proxy#ssl-support).

Steps in macos:
- download cert file
```
wget https://raw.githubusercontent.com/lightbody/browsermob-proxy/master/browsermob-core/src/main/resources/sslSupport/ca-certificate-rsa.cer
```
- Open keychain (or this also opens keychan: Chrome menu: Settings > Privacy and security > Security > Manage certificates)
- Keychain menu: File > Import items > import 'ca-certificate-rsa.cer'
- It's listed under 'certificates' as 'LittleProxy MITM' but not trusted
- right click menu > Get info > expand 'Trust' > "When using this certificate" = "Always Trust"
- Remember delete this item after testing is done.

## Sample Code
```
import json
import pydash
import wenbot

bot = wenbot.Bot(proxy=True)
input('enter to print log and stop browser')
# Chrome window shows up.
# After open webpage and operations
har = bot.proxy.har  # this is a property that pulls data from server
# bot.proxy is a browsermobproxy.client.Client object
# see https://browsermob-proxy-py.readthedocs.io/en/stable/client.html
# har is recorded log
with open('/tmp/har.json', 'wt') as f:
    print(json.dumps(har, indent=4, default=str), file=f)

for entry in pydash.get(har, 'log.entries') or []:
    print(pydash.get(entry, "request.url"))
    print(f'    method={pydash.get(entry, "request.method")}')
    print('    Headers')
    for header in pydash.get(entry, 'request.headers') or []:
        print(f'        {header["name"]}: {header["value"]}')
    print(f'    status={pydash.get(entry, "response.status")}')
```

Try sample code and open `/tmp/har.json` see what's HAR structure.

Use `bot.proxy.new_har()` to record new HAR data.

Default only record headers, not content or binary content (in brosermob-proxy terms).

To specify different options: eg.
```
bot.proxy.new_har(options={
    'captureHeaders': True,
    'captureContent': True,
    'captureBinaryContent': False,
})
```

# Change History

- 0.0.9 2021-10-31 update doc for https sites with browsermobproxy and update dependency for bs4
- 0.0.8 2021-08-19 add sample code
- 0.0.7 2021-07-14 bugfix
- 0.0.6 2021-07-14 replace print with log
- 0.0.5 2021-07-14 Bumps urllib3 from 1.26.4 to 1.26.5

