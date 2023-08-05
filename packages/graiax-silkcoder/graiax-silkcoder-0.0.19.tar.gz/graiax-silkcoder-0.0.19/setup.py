# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['graiax', 'graiax.silkcoder']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'graiax-silkcoder',
    'version': '0.0.19',
    'description': 'transform audio file to silk',
    'long_description': "# Graiax-silkcoder\n现在版本：![pypi](https://img.shields.io/pypi/v/graiax-silkcoder?color=blue)   \n这，是一个Python的silk转码器   \n通过将[kn007/silk-v3-decoder](https://github.com/kn007/silk-v3-decoder)通过简单的封装制成   \n\n## 安装\n```shell\npip install graiax-silkcoder\n# 如果需要转换非wav的音频文件，则需要ffmpeg/anconv\n# 如何安装ffmpeg/anconv请自行百度\n```\n## 使用方法\n```python\nfrom pathlib import Path\nfrom graiax import silkcoder\n\n#silk编码\n#你可以文件→文件\nawait silkcoder.encode('a.wav', 'a.silk')\n#你可以文件→二进制数据\nsilk: bytes=await silkcoder.encode('a.wav')\n#你可以二进制数据→二进制数据\nsilk: bytes=await silkcoder.encode(Path('a.wav').read_bytes())\n#你可以二进制数据→文件\nawait silkcoder.encode(Path('a.wav').read_bytes(), audio_format='wav', 'a.silk')\n#你可以指定让ffmpeg解码音频，也可以让程序自己选择\n#注:只有当音频是wav且ensure_ffmpeg=None时才会不使用ffmpeg处理\nawait silkcoder.encode('a.wav', 'a.silk')\nawait silkcoder.encode('a.wav', 'a.silk', ensure_ffmpeg=True)\n#你也可以设置码率(默认状态下将会将尝试将目标语音大小限制在980kb上下)\nawait silkcoder.encode('a.wav', 'a.silk', rate=70000)\n#你甚至可以剪辑音频\nawait silkcoder.encode('a.wav', 'a.silk', ss=10, t=5)#从第10s开始剪辑5s的音频\n\n#silk解码\n#你可以文件→文件\nawait silkcoder.decode('a.silk', 'a.wav')\n#你可以文件→二进制数据\nwav: bytes=await silkcoder.decode('a.silk')\n#你可以二进制数据→二进制数据(必填audio_format)\nmp3: bytes=await silkcoder.decode(Path('a.silk').read_bytes(), audio_format='mp3')\n#你可以二进制数据→文件\nawait silkcoder.encode(Path('a.silk').read_bytes(), 'a.wav')\n#你可以指定让ffmpeg解码音频，也可以让程序自己选择\n#注:只有当音频是wav且ensure_ffmpeg=None时才会不使用ffmpeg处理\nawait silkcoder.encode('a.wav', 'a.silk')\nawait silkcoder.encode('a.wav', 'a.silk', ensure_ffmpeg=True)\n#你也可以设置码率(不指定码率的情况下，程序将会尝试将音频大小控制在1Mb以下)\nawait silkcoder.encode('a.wav', 'a.silk', rate=70000)\n#你甚至可以剪辑音频\nawait silkcoder.encode('a.wav', 'a.silk', ss=10, t=5)#从第10s开始剪辑5s的音频\n```",
    'author': 'I_love_study',
    'author_email': '1450069615@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/I-love-study/graiax-silkcoder',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
