# 天使大人

按照官方教程 Miniforge + conda-forge SageMath 方案安装 Sage ：

```bash
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh"
chmod +x Miniforge3-Linux-aarch64.sh
bash Miniforge3-Linux-aarch64.sh
source ~/.bashrc
```

创建一个环境：

```bash
conda create -n sage sage
```

激活：

```bash
conda activate sage
```

然后用 `sage` 运行 `关于邻家的天使大人不知不觉把我惯成废人这档子事.py` ：

```bash
(sage) scetayh@yuprae-gentoo ~/Downloads $ sage 关于邻家的天使大人不知不觉把我惯成废人这档子事.py                                                                                                               
Traceback (most recent call last):                                                                                                                                                                              
  File "/home/scetayh/miniforge3/envs/sage/bin/sage", line 5, in <module>                                                                                                                                       
    from sage.cli.__main__ import main                                                                                                                                                                          
  File "/home/scetayh/miniforge3/envs/sage/lib/python3.12/site-packages/sage/cli/__main__.py", line 9, in <module>                                                                                              
    sys.exit(main())                                                                                                                                                                                            
             ^^^^^^                                                                                                                                                                                             
  File "/home/scetayh/miniforge3/envs/sage/lib/python3.12/site-packages/sage/cli/__init__.py", line 56, in main                                                                                                 
    return RunFileCmd(options).run()                                                                                                                                                                            
           ^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                                                                            
  File "/home/scetayh/miniforge3/envs/sage/lib/python3.12/site-packages/sage/cli/run_file_cmd.py", line 50, in run                                                                                              
    eval(compile(open(input_file, 'rb').read(), input_file, 'exec'), sage_globals())                                                                                                                            
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                                             
  File "关于邻家的天使大人不知不觉把我惯成废人这档子事.py", line 3                                                                                                                                              
    P.<x> = PolynomialRing(GF(2))                                                                                                                                                                               
      ^                                                                                                                                                                                                         
SyntaxError: invalid syntax 
```

它把文件当成 Python 脚本来解析了。改后缀名指定：

```bash
mv 关于邻家的天使大人不知不觉把我惯成废人这档子事.{py,sage}       
```

然后再次运行：

```bash
(sage) scetayh@yuprae-gentoo ~/Downloads $ sage 关于邻家的天使大人不知不觉把我惯成废人这档子事.sage 
e834598ba8cf6695cc9299364fe4fa63b05a1b55f847ab5aecb6d5dc251e2b77 
```

然后用 `nc` ：

```bash
(base) scetayh@yuprae-gentoo ~ $ nc nc1.ctfplus.cn 42583
result = e834598ba8cf6695cc9299364fe4fa63b05a1b55f847ab5aecb6d5dc251e2b77 
0xGame{r34lly g00d st3p f0rw4ord}
```

得到 flag 为 `0xGame{r34lly g00d st3p f0rw4ord}` 。