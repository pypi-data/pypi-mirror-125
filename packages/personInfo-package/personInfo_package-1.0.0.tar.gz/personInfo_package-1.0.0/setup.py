from distutils.core import setup
from setuptools import find_packages

with open("README.rst", 'r') as f:
    long_description = f.read()

setup(name='personInfo_package',  # 包名
      version='1.0.0',  # 版本号
      description='Generate multiple messages',  # 描述
      long_description=long_description,  # 长描述
      author='Cola',
      author_email='2651509381@qq.com',
      url='https://gitee.com/l_cola/cola',
      install_requires=[],  # 依赖第三方库
      license='MIT License',
      packages=find_packages(),
      platforms=["all"],  # 平台
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )
