from setuptools import setup

setup(name='defensics-pcap',
      version='0.2.0',
      description='Unofficial Defensics Packet Capture Assistant Tool',
      author='Joshua Pereyda',
      packages=['defensics_pcap'],
      entry_points={
          'console_scripts': [
              'defensics-pcap = defensics_pcap.__main__:main'
          ]
      },
      include_package_data=True,
      install_requires=[],
      extras_require={
          # deps list is duplicated in setup.py extras_require. Make sure to change both!
          'dev': ['check-manifest']
      },
      )
