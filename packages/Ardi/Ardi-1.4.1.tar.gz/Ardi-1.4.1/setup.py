from distutils.core import setup
setup(
  name = 'Ardi',         # How you named your package folder (MyLib)
  packages = ['Ardi'],   # Chose the same as "name"
  version = '1.4.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A Python module created by Muhammad Ardi Putra. Currently working on machine learning and computer vision',   # Give a short description about your library
  long_description='The documentation of this package can be seen in https://github.com/MuhammadArdiPutra/ModuleByArdi. The line-by-line code explanation is shown in the "Documentation" folder.',
  long_description_content_type="text/markdown",
  author = 'Muhammad Ardi Putra',                   # Type in your name
  author_email = 'muhammadardiputra4@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/MuhammadArdiPutra',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/MuhammadArdiPutra/ModuleByArdi/archive/refs/tags/v_1.4.1.tar.gz',    # I explain this later on
  keywords = ['Machine Learning', 'Computer Vision'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'pandas',
		  'matplotlib', 
		  'seaborn',
		  'tqdm'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.7',      #Specify which pyhton versions that you want to support
  ],
)