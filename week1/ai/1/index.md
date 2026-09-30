# ez_pytorch

```bash
(.venv) scetayh@yuprae-gentoo ~/Downloads $ python load.py 
Traceback (most recent call last):
  File "/home/scetayh/Downloads/load.py", line 3, in <module>
    model = torch.load("model.pth", weights_only=True)
  File "/home/scetayh/.venv/lib/python3.14/site-packages/torch/serialization.py", line 1614, in load
    raise pickle.UnpicklingError(_get_wo_message(str(e))) from None
_pickle.UnpicklingError: Weights only load failed. This file can still be loaded, to do so you have two options, do those steps only if you trust the source of the checkpoint. 
        (1) In PyTorch 2.6, we changed the default value of the `weights_only` argument in `torch.load` from `False` to `True`. Re-running `torch.load` with `weights_only` set to `False` will likely succeed, but it can result in arbitrary code execution. Do it only if you got the file from a trusted source.
        (2) Alternatively, to load with `weights_only=True` please check the recommended steps in the following error message.
        WeightsUnpickler error: Unsupported global: GLOBAL exec was not an allowed global by default. Please use `torch.serialization.add_safe_globals([exec])` or the `torch.serialization.safe_globals([exec])` context manager to allowlist this global if you trust this class/function.

Check the documentation of torch.load to learn more about types accepted by default with weights_only https://pytorch.org/docs/stable/generated/torch.load.html.
```

为了拿到 flag 不搞白名单，直接把 `weights_only` 从 `True` 改为 `False` 。

```bash
(.venv) scetayh@yuprae-gentoo ~/Downloads $ python load.py 
你成功触发了pickle反序列化，程序输出了flag:0xGame{3z_p1ckl3_fOr_pyt0rch}!
希望你不要立刻开始下一题，能静下心搜集并了解一下pickle反序列化的原理
简单来说，pytorch底层依赖python的pickle库，而pickle库会将load对象的__reduce__方法中的内容直接翻译为虚拟机指令，因此exec+python代码即可直接被执行
这里如果改成os+命令即可实现远程RCE
安全起见，pytorch在较新版本中使用默认weights_only=True参数，使用白名单来屏蔽恶意指令。不过，最安全的方法是使用safetensors库
model loaded: None
```

从而 flag 为 `0xGame{3z_p1ckl3_fOr_pyt0rch}` 。