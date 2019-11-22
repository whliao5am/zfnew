from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='zfnew',
    version='0.0.3',
    author='NeroAsmar',
    author_email='neroasmarr@gmail.com',
    url='https://neroasmar.top/zfnew/',
    description=u'新版正方教务管理系统API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['requests', 'bs4', 'rsa', 'Crypto'],
    # extras_require={  # 分组依赖模块，可使用pip install sampleproject[dev] 安装分组内的依赖
    #    'dev': ['check-manifest'],
    #    'test': ['coverage'],
    # },
    python_requires='>=3.0.0',
    classifiers=[
        'Intended Audience :: Developers',  # 模块适用人群

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',  # 模块的license

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    # entry_points={
    #     'console_scripts': [
    #     ]
    # }
)
