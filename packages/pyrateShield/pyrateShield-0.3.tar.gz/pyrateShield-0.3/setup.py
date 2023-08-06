from setuptools import setup, find_packages

APP_NAME = "pyrateshield"
APP_VERSION = "0.3"
APP_SCRIPT_NAME = "%s.py" % APP_NAME.lower()


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='pyrateShield',
      python_requires='>=3.8',
      version=APP_VERSION,
      description='Generate radiation-dose maps',
      long_description=readme(),
      keywords='pyrateShield radiation radiology nuclear medicine',
      url='https://bitbucket.org/MedPhysNL/pyrateShield',
      author='Marcel Segbers, Rob van Rooij',
      author_email='msegbers@gmail.com',
      license='GNU GPLv3',
      packages=find_packages(),
      # now managed by manifest.in
      # package_data={'pyrateshield.radtracer': ['MCNP.pickle'],
      #               'pyrateshield': ['constants.yml'],
      #               'pyrateshield.gui': ['styles.yml'],
      #               'pyrateshield.pyshield.physics': ['*.xls', '*.yml'], 
      #               '':['LICENSE', 'constants.yml']},
      install_requires=[
          'numpy',
          'scipy',
          'matplotlib',
          # https://stackoverflow.com/questions/62980464/cant-install-pyqt5-on-python-3-with-spyder-ide		
          'pyqt5', #'==5.12; python_version<="3.8"',  #tested on 3.8 compatible with anaoconda
          #'pyqt5', #' python_version>"3.8"', # python 3.9 needs latest version, no 3.9 version of anaconda yet. Check in future for compatability
          #'pyqtwebengine==5.12; python_version<="3.8"',
          'pyqtwebengine', # python_version>"3.8"',
          #'pillow',
          'pynrrd',
          'pyyaml',
          'scikit-image',
           #'svglib',
          'imageio',
          'pandas',
          'psutil',
          'xlsxwriter',
          'xlrd',
          'qtawesome'],
          #'pyshield @ git+https://bitbucket.org/MedPhysNL/pyshield.git'],
      #test_suite='nose.collector',
      #tests_require=['nose', 'nose-cover3'],
      entry_points={
          'console_scripts': ['pyrateshield=pyrateshield.app:main'],
      },
      include_package_data=True,
      zip_safe=False)
