# Magical Large Potato!

先看一下 `.pth` 内容：

```bash
(.venv) scetayh@yuprae-gentoo ~/Projects/0xgame2026-writeups/week1/ai/2 $ python3
```

```python
Python 3.14.7 (main, Aug  6 2026, 10:09:26) [GCC 16.1.1 20260718] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> ckpt=torch.load("Magic_Large_Potato.pth")
>>> print(type(ckpt))
<class 'dict'>
```

是词典，作为简单题的话应该是查字典了，不至于上来就找后门。看一下有哪些键：

```python
>>> print(ckpt.keys())
dict_keys(['magic1', 'magic2'])
```

首先查看 `magic1` 的类型：

```python
>>> m1=ckpt["magic1"]
>>> print(type(m1))
<class 'collections.OrderedDict'>
>>> 
```

这个估计是 sd 了，检查键：

```python
>>> print(m1.keys())
odict_keys(['embedding.weight', 'deep_mlp.0.weight', 'deep_mlp.0.bias', 'deep_mlp.2.weight', 'deep_mlp.2.bias', 'deep_mlp.4.weight', 'deep_mlp.4.bias', 'deep_mlp.6.weight', 'deep_mlp.6.bias'])
```

Tensors 都在这里。然后去看 `magic2` ：

```python
>>> m2=ckpt["magic2"]
>>> print(type(m2))
<class 'int'>
```

这个是整数：

```python
>>> print(m2)
23
```

23 大概是 flag 的长度，而 `m1` 里面应该藏了 flag 。为了验证这个猜想，看一下 `m1` Embedding 本身权重的形状：

```python
>>> ew=m1['embedding.weight']
>>> print(ew.shape)
torch.Size([23, 32])
```

也就是说 `ew` 是二维的，23 * 32 。这个 23 确实和 `m1` 里的 23 吻合了。接着看其他 Tensor 的信息：

```python
>>> for k, v in m1.items(): print(k, v.shape)
... 
embedding.weight torch.Size([23, 32])
deep_mlp.0.weight torch.Size([128, 32])
deep_mlp.0.bias torch.Size([128])
deep_mlp.2.weight torch.Size([256, 128])
deep_mlp.2.bias torch.Size([256])
deep_mlp.4.weight torch.Size([128, 256])
deep_mlp.4.bias torch.Size([128])
deep_mlp.6.weight torch.Size([100, 128])
deep_mlp.6.bias torch.Size([100])
>>> 
```

缺了 1 、3 、5 层，但矩阵乘法 32 → 128 → 256 → 128 → 100 是吻合的，这些层应该是激活函数。我准备用 ReLU ，这样就算猜错了后面参数取最大的时候应该也不影响。

那下面就是模拟计算过程了。先生成 0 到 22 的整数序列作为 ID ：

```python
>>> id=torch.arange(23)
```

嵌入查表放到 `x` 里：

```python
>>> from torch.nn.functional import embedding
>>> x=embedding(id, ew)
```

把七层 layers 全部过一遍：

```python
>>> x=x@m1["deep_mlp.0.weight"].T+m1["deep_mlp.0.bias"] # 0
>>> x=relu(x) # 1
Traceback (most recent call last):
  File "<python-input-59>", line 1, in <module>
    x=relu(x)
      ^^^^
NameError: name 'relu' is not defined
>>> from torch.nn.functional import relu
>>> x=relu(x)
>>> x=x@m1["deep_mlp.2.weight"].T+m1["deep_mlp.2.bias"] # 2
>>> x=relu(x) # 3
>>> x=x@m1["deep_mlp.4.weight"].T+m1["deep_mlp.4.bias"] # 4
>>> x=relu(x) # 5
>>> x=x@m1["deep_mlp.6.weight"].T+m1["deep_mlp.6.bias"] # 6
```

转成可打印的字符：

```python
>>> x.argmax(1)
tensor([ 0, 33, 42, 10, 22, 14, 90, 48, 47, 51, 88,  1, 28, 88, 28,  0, 88, 22,
         4, 16,  1, 12, 92])
>>> x.argmax(1).tolist()
[0, 33, 42, 10, 22, 14, 90, 48, 47, 51, 88, 1, 28, 88, 28, 0, 88, 22, 4, 16, 1, 12, 92]
>>> l=x.argmax(1).tolist()
>>> import string
>>> [string.printable[i] for i in l]
['0', 'x', 'G', 'a', 'm', 'e', '{', 'M', 'L', 'P', '_', '1', 's', '_', 's', '0', '_', 'm', '4', 'g', '1', 'c', '}']
>>> ''.join([string.printable[i] for i in l])
'0xGame{MLP_1s_s0_m4g1c}'
```

所以答案就是 `0xGame{MLP_1s_s0_m4g1c}` 。

极限压缩整个过程：

```python
import torch as t,string as s;d=t.load("Magic_Large_Potato.pth")["magic1"];e=t.nn.functional.embedding;m="deep_mlp.%d";W=".weight";B=".bias";x=e(t.arange(23),d["embedding.weight"])
for i in 0,2,4:x=e.relu(x@d[m%i+W].T+d[m%i+B])
print(''.join(s.printable[i]for i in(x@d[m%6+W].T+d[m%6+B]).argmax(1)))
```

也可以得到 `0xGame{MLP_1s_s0_m4g1c}` 。