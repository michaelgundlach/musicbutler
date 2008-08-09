from setuptools import setup

setup(name='musicbutler',
      version='0.1.3',
      py_modules=['musicbutler'],
      install_requires=['speech', 'mutagen'],

      description="A robot that receives voice commands to play albums"
         " from your MP3 collection",

      long_description="""
          *** NOTE: This is an alpha product.  It doesn't actually play
          music yet -- it just understands commands and runs stub functions
          for playing music. ***

          When MusicButler has been told what albums you own, a spoken
          conversation with it might go like this:

            * "Jimmy, what albums do I have?"
            * "Here are 3 out of your 58 albums: In Rainbows by Radiohead,
            Deja Vu by Crosby Stills Nash and Young, and Atlanta
            by Alison Krauss."
            * "Jimmy, what Radiohead albums do I have?"
            * "You have 2 albums by Radiohead: In Rainbows, and OK Computer."
            * "Jimmy, play me some Alison Krauss."
            * "Playing New Favorite by Alison Krauss."
          \n
          For the required Python 'speech' module to work, you must:\n
            * Install the Microsoft Speech kit: download
              and run "SpeechSDK51.exe" from http://tinyurl.com/5m6v2
            * Then open PythonWin (installable via http://tinyurl.com/5ezco9)
              and choose Tools | COM MakePY utility | Microsoft
              Speech Object Library 5.0.\n
          \n
          Please let me know if you like or use this module - it would make
          my day!
          """,

      author='Michael Gundlach',
      author_email='gundlach@gmail.com',
      url='http://musicbutler.googlecode.com/',
      keywords = "speech recognition music stereo control mp3 robot butler",

      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Win32 (MS Windows)',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python',
          'Topic :: Multimedia :: Sound/Audio :: Speech',
          'Topic :: Home Automation',
          'Topic :: Scientific/Engineering :: Human Machine Interfaces',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Desktop Environment',
          ]

     )
