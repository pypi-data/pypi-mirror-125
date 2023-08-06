import setuptools
setuptools.setup(
    name="nian", # Replace with your own username  #自定义封装模块名与文件夹名相同
    version="0.1.7",
    author="初慕苏流年", #作者
    author_email="1274210585@qq.com", #邮箱
    description="集合工具等", #描述
    long_description='白嫖(QQ，酷狗，酷我，网易)音乐，快速排序，冒泡排序，目录暴力遍历', #描述
    long_description_content_type="text/markdown", #markdown
    url="http://0.wlwmz.top:2/", #github地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", #License
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',  #支持python版本
)
