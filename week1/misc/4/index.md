# Interesting_ppt

`.pptx` 可以直接 `unzip` 的：

```bash
scetayh@yuprae-gentoo ~/Downloads $ ls
0xgame.zip
scetayh@yuprae-gentoo ~/Downloads $ unzip 0xgame.zip 
Archive:  0xgame.zip
  inflating: 0xgame.pptx             
scetayh@yuprae-gentoo ~/Downloads $ unzip 0xgame.pptx 
Archive:  0xgame.pptx
  inflating: [Content_Types].xml     
   creating: _rels/
  inflating: _rels/.rels             
   creating: docProps/
  inflating: docProps/app.xml        
  inflating: docProps/core.xml       
...  
  inflating: ppt/viewProps.xml       
```

一般藏彩蛋的多半是 Base64 编码，所以找一找 `==` ：

```bash
scetayh@yuprae-gentoo ~/Downloads $ grep -rn '==' 2>/dev/null
docProps/custom.xml:2:<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/custom-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" pid="2" name="AIGC">fTAvKTQybl5VAXRHHA8JCygHfFZTWGYCIydUDQcBX0pVdkB3AwA3OVBnZAZpLxUJCSIZVFJYeAIiHysLPDV8AFFcYk0kUFRQEnpmCw==<vt:lpwstr></vt:lpwstr></property></Properties>
```

这里有个字段叫 `AIGC` ，后面冷不丁有一串编码：

```
fTAvKTQybl5VAXRHHA8JCygHfFZTWGYCIydUDQcBX0pVdkB3AwA3OVBnZAZpLxUJCSIZVFJYeAIiHysLPDV8AFFcYk0kUFRQEnpmCw==
```

但是这个编码解出来本身是乱的：

```
}0/)42n^UtG	(|VSXf#'T
_JUv@w79Pgdi/		"TRXx"+<5|Q\bM$PTPzf
```

还带有不可显示的字符，很有可能是加密。继续看看其他文件。浏览时为了使得 XML 便于阅读，可以用 `fmt` 命令：

```bash
scetayh@yuprae-gentoo ~/Downloads $ fmt < \[Content_Types\].xml 
 <Typesersion="1.0" encoding="UTF-8" standalone="yes"?>
xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default
Extension="rels"
ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default
Extension="xml" ContentType="application/xml"/><Override
PartName="/ppt/presentation.xml"
ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/><Override
PartName="/ppt/slideMasters/slideMaster1.xml"
ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/><Override
PartName="/ppt/slides/slide1.xml"
ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/><Override
PartName="/ppt/slides/slide2.xml"
ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/><Override
PartName="/ppt/slides/slide3.xml"
ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/><Override
PartName="/ppt/slides/slide4.xml"
...
```

按字母顺序开始检查各文件，最终在第三份文件 `docProps/core.xml` 里看到了：

```xml
<!-- ... --><cp:revision>1</cp:revision>a2V5PTB4R2FtZV8yMDI2<dcterms:modified xsi:type="dcterms:W3CDTF">2026-09-27T08:02:59Z</dcterms:modified><!-- ... -->
```

这个 `a2V5PTB4R2FtZV8yMDI2` 生硬地插在了标签间隙中，渲染器一般会跳过它，很适合藏东西。Base64 解码后得到：

```
key=0xGame_2026
```

按照惯例，密文和密钥都应该转为二进制，密钥以循环方式与密文做 XOR 运算。找个网页工具，最终解得：

```
MHhHYW1le3BwdHhfMXNfanVzdF9hX3oxcF80bmRfbWV0YWRhdGFfbjN2ZXJfYjN0cjR5c195MHV9
```

这显然也是 Base64 编码。所以解码得到：

```
0xGame{pptx_1s_just_a_z1p_4nd_metadata_n3ver_b3tr4ys_y0u}
```

即为 flag 。