from setuptools import setup, find_packages

setup(
    name='zhengfang_new',
    version='0.0.1',
    author='NeroAsmar',
    author_email='neroasmarr@gmail.com',
    url='https://neroasmar.top/zhengfang_new/',
    description=u'新版正方教务管理系统API（课程表，个人信息，考试信息，学校通知）',
    packages=find_packages(),
    install_requires=['requests', 'bs4', 'rsa' 'binascii', 'Crypto', 'base64'],
    python_requires='>=3.5',
    # entry_points={
    #     'console_scripts': [
    #     ]
    # }
)
