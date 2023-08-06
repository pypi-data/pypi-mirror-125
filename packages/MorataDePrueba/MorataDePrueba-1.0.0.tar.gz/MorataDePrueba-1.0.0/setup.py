from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()


# specify requirements of your package here
REQUIREMENTS = ['requests']

# some more details
CLASSIFIERS = [
	'Development Status :: 4 - Beta',
	'Intended Audience :: Developers',
	'Topic :: Internet',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: Python',
	'Programming Language :: Python :: 2',
	'Programming Language :: Python :: 2.6',
	'Programming Language :: Python :: 2.7',
	'Programming Language :: Python :: 3',
	'Programming Language :: Python :: 3.3',
	'Programming Language :: Python :: 3.4',
	'Programming Language :: Python :: 3.5',
	]

# calling the setup function
setup(name='MorataDePrueba',
	version='1.0.0',
	description='Shit to test how is ',
	long_description=README,
    long_description_content_type='text/markdown',
	url='https://github.com/Cesuuur/PublishPyCodeTest',
	author='César Redondo Urdiales',
	author_email='kaluti12@gmail.com',
	packages=['main'],
	classifiers=CLASSIFIERS,
	install_requires=REQUIREMENTS,
	keywords='maps location address'
	)
