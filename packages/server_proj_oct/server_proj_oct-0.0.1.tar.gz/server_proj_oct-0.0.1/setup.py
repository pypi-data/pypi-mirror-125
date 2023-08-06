from setuptools import setup, find_packages

setup(name="server_proj_oct",
      version="0.0.1",
      description="server_proj_oct",
      author="Ivan Ivanov",
      author_email="iv.iv@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
