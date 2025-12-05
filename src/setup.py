from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='IVOFilesConverter',
  version='1.0.6',
  author='keynet',
  author_email='viktorplay377@gmail.com',
  description='Конвертер файлов.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Keynet123/IVOFilesConverter',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='files ivofilesconverter ',
  project_urls={
    'GitHub': 'https://github.com/Keynet123/IVOFilesConverter'
  },
  python_requires='>=3.6'
)