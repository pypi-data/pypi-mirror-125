from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'Operating System :: Unix',
  'Operating System :: MacOS :: MacOS X',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='mysql_to_mongo',
  version='1.0.3',
  description='Migrate your MySql databse to MongoDb.',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type="text/markdown",
  url='',  
  author='ArJun Gawali',
  author_email='arjungawali111@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='mysql-to-mongodb,migrate ,mysql,mongodb', 
  packages=find_packages(),
  install_requires=['mysql.connector.python','pymongo','dnspython'] 
)