# pytiktok
### to install:
```bash
pip install pytiktok  
```
### Example
```python
from pytiktok import Tikvideo

Video = Tikvideo()


k = Video.tiktok("https://www.tiktok.com/@shib_x/video/6986742592985648390?sender_device=mobile&sender_web_id=7002607198221338117&is_from_webapp=v1&is_copy_url=0",True)

print(k["ok"])

print(k["link"])
```
### cases

* If true, the link will open automatically
* If flase, the link will not open automatically

### Follow us on social media accounts

* telegram : @DIBIBl ; @TDTDI
* instgram : @_v_go
* github : https://github.com/muntazir-halim