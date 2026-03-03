# 网易云歌单采集
# 还没解决js代码中不能有emoji表情的问题
# your cookie
cookie = 'YOUR_COOKIE'
# your Playlist link ID
link = 'https://music.163.com/playlist?id=YOUR_PLAYLIST_ID'#YOUR_PLAYLIST_ID=你的歌单链接ID，是歌单网页顶部最后一串数字

# 导入正则
import re
# 导入编译js模块
import execjs
# 导入数据请求模块
import requests
# 导入 Path 类,现代化的路径处理方式（简洁、跨平台）
from pathlib import Path
import random  # 用来生成随机数
import time  # 用来延时


# ========== 新增：文件名清理函数 ==========
def clean_filename(filename):
    """
    清理 Windows 文件名中的非法字符
    Windows 禁止：< > : " / \ | ? *
    替换为下划线或空字符串
    """
    # 定义非法字符列表
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        filename = filename.replace(char, '')  # 直接删除非法字符
    # 去除首尾空格和点（避免隐藏文件）
    filename = filename.strip().strip('.')
    # 如果文件名为空，用音乐 ID 代替
    if not filename:
        filename = 'unknown'
    return filename


# ========== 新增结束 ==========

# 请求头参数，字典接收
headers = {
    # 登录信息等
    'cookie': f'{cookie}',
    # 基本伪装
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0',
    # 防盗链，解决403，哪里来的
    'referer': 'https://music.163.com/'
}
# 批量爬取需要js逆向解析加密
"""
通过打断点，继续执行，点击开始播放，找到暂停位置 
var bWo2x = window.asrsea(JSON.stringify(i6c), bod1x(["流泪", "强"]), bod1x(AY2x.md), bod1x(["爱心", "女孩", "惊恐", "大笑"]));
函数方法：window.asrsea()
加密参数：
    JSON.stringify(i6c),
    bod1x(["流泪", "强"]),
    bod1x(AY2x.md),
    bod1x(["爱心", "女孩", "惊恐", "大笑"])

    在断点调试状态下控制台输入i6等可得结果：
    i6c
    {id: '28009051', c: '[{"id":"28009051"}]', csrf_token: '5f178a109233e573a8be8ff1ad4401f1'}c: "[{\"id\":\"28009051\"}]"csrf_token: "5f178a109233e573a8be8ff1ad4401f1"id: "28009051"[[Prototype]]: Object
    bod1x(["流泪", "强"])
    '010001'
    bod1x(AY2x.md)
    '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    bod1x(["爱心", "女孩", "惊恐", "大笑"])
    '0CoJUm6Qyw8W8jud'

    复制相关js代码本地调试分析

"""
# 请求网址:歌单链接
link = f'{link}'
# 发送请求，获取数据
html = requests.get(link, headers=headers).text

# 正则匹配提取歌曲信息，名字和id🤔
info = re.findall('<a href="/song\?id=(\d+)">(.*?)</a>', html)  # .*?：匹配任意字符 0 次或多次，尽可能少地匹配
count = 0
# for循环，一次只能处理一首歌曲
for music_id, title in info:
    # ============ 新增 try-except 开始 ============
    try:
        print(f'正在处理歌曲：{title}')
        # 加密代码
        js_code = execjs.compile(open('NetEaseCloudEncryption.js', encoding='utf-8').read())
        # 加密参数传入 🤔有 ids 的 i6c
        i6c = {
            "ids": f"[{music_id}]",
            "level": "exhigh",
            "encodeType": "aac",
            "csrf_token": "5f178a109233e573a8be8ff1ad4401f1"
        }
        # 调用
        r = js_code.call('GetSign', i6c)

        # 请求网址 (是接口，不是资源网址)
        url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token=5f178a109233e573a8be8ff1ad4401f1  '

        # 请求参数
        data = {
            'params': r['encText'],
            'encSecKey': r['encSecKey']
        }

        # 发送请求
        response = requests.post(url=url, data=data, headers=headers, timeout=10)
        response.raise_for_status()  # 捕获 4xx/5xx 状态码

        # 获取响应的 json 数据

        json_data = response.json()
        # print(json_data)

        # 解析提取地址
        """
        json_data['data']：获取键为 'data' 的列表；
        [0]：取列表中第一个元素（字典）；
        ['url']：从该字典中提取 'url' 字段；
        """
        music_url = json_data['data'][0]['url']  # 🤔为啥是 0:一次只能处理一首歌曲

        # 额外检查：VIP/下架歌曲可能返回 null
        if not music_url:
            print(f'⚠️ 跳过：{title}（无下载权限或已下架）')
            continue

        # 获取音频内容
        music_content = requests.get(url=music_url, headers=headers, timeout=30).content

        # ========== 新增：清理文件名 ==========
        safe_title = clean_filename(title)  # 清理非法字符
        print(f'  📁 清理后文件名：{safe_title}.mp3')
        # ========== 新增结束 ==========

        # 文件夹创建及文件保存位置🤔
        """
        Path.home()     #获取当前用户的主目录 (Windows: C:\用户们\用户名
        / "Desktop"     #拼接桌面文件夹名

        / "music"       #拼接 music 子文件夹（不管有无）

        mkdir()         #创建文件夹

        exist_ok=True   #如果文件夹已存在，不报错且不创建了
        """
        desktop = Path.home() / "Desktop"  # 获取桌面
        music_floder = desktop / "Music"
        music_floder.mkdir(exist_ok=True)
        # ========== 修改：使用清理后的文件名 ==========
        file_path = music_floder / f"{safe_title}.mp3"  # 使用 safe_title 而非 title
        # ========== 修改结束 ==========

        # 数据保存
        with open(file_path, mode='wb') as f:
            f.write(music_content)

        print(music_url)
        print(f"✅ 音乐文件已保存到：{file_path}")
        count = count + 1

    # ============ 新增异常捕获开始 ============
    except execjs.ProgramError as e:
        print(f'❌ JS 加密失败 {title}：{str(e)[:100]}...')
    except requests.exceptions.RequestException as e:
        print(f'❌ 网络请求失败 {title}：{str(e)[:100]}...')
    except (KeyError, IndexError, TypeError) as e:
        # 处理 json_data['data'][0]['url'] 可能不存在的情况
        print(f'❌ 数据解析失败 {title}：{str(e)[:100]}...')
    except IOError as e:
        print(f'❌ 文件保存失败 {title}：{str(e)[:100]}...')
    except Exception as e:
        # 兜底捕获其他未知异常
        print(f'❌ 未知错误 {title}：{type(e).__name__} - {str(e)[:100]}...')
    # ============ 异常捕获结束 ============
    finally:
        # 休息一下，避免被封（随机 0.5-1.5 秒）🤔uniform 随机生成一个浮点数，范围是 [0.2, 0.5)
        sleep_time = random.uniform(0.2, 0.5)  # 🤔uniform 随机生成一个浮点数，范围是 [0.2, 0.5)
        print(f'  ⏳ 等待 {sleep_time:.1f} 秒...\n')
        time.sleep(sleep_time)
    # ============ try-except 结束 ============

print(f'✅ 已成功处理 {count} 首歌曲')
print('✅ 所有音乐文件已成功保存到桌面的Music文件夹中！')
