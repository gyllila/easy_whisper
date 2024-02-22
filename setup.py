from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='easy_whisper',
      version='1.1.0',
      description="An easy to use adaption of OpenAI's Whisper, with both CLI and (tkinter) GUI, faster processing even on CPU, txt output with timestamps.",
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
      ],
      keywords='audio transcribe translate STT easy fast CPU CUDA',
      url='https://github.com/gyllila/easy_whisper',
      author='Yanling Guo',
      author_email='guoyanling_2000@yahoo.de',
      license='GPL',
      packages=['easy_whisper'],
      install_requires=[
          'openai',
          'openai-whisper'
      ],
      entry_points={
        "console_scripts": [
            "easy_whisper=easy_whisper.__main__:main"
        ]
      },
      include_package_data=True,
      zip_safe=False)
