from setuptools import setup, find_packages

'''with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()'''

setup_args = dict(
    name='AERzip',
    version='0.5.0',
    description='Useful tools to compress and decompress AEDAT files in Python',
    #long_description_content_type="text/markdown",
    #long_description=README + '\n\n' + HISTORY,
    license='GPL-3.0',
    packages=find_packages(),
    author='Alvaro Ayuso Martinez',
    author_email='alv.correo@gmail.com',
    keywords=['AER', 'Events', 'Spikes', 'AEDAT', 'Compression', 'Decompression', 'Utils',
              'Neuroscience', 'Neuromorphic', 'Cochlea', 'Retina', 'jAER'],
    url='https://github.com/alvaroy96/AERzip',
    download_url='https://pypi.org/project/AERzip/'
)

install_requires = [
    'pyNAVIS>1.1.0',
    'lz4>=3.1.3',
    'zstandard>=0.16.0'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
