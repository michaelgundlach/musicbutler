from setuptools import setup

setup(name='musicbutler',
      version='0.1.4',
      py_modules=['musicbutler'],
      install_requires=['speech', 'mutagen'],

      description="A robot that receives voice commands to play albums"
         " from your MP3 collection",

      long_description="""
          *** NOTE: This is an alpha product.  It's not quite to the
          point of playing music yet, which should happen in 0.2.0.***

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
          Uses the 'speech' module -- see that on pypi for prerequisites.
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
          'Topic :: Multimedia :: Sound/Audio',
          'Topic :: Home Automation',
          'Topic :: Scientific/Engineering :: Human Machine Interfaces',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Desktop Environment',
          ]

     )
