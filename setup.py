from setuptools import find_packages
import datetime, os, re, subprocess

from skbuild import setup


# Force wheel to be platform specific
# https://stackoverflow.com/questions/45150304/how-to-force-a-python-wheel-to-be-platform-specific-when-building-it
# https://github.com/Yelp/dumb-init/blob/48db0c0d0ecb4598d1a6400710445b85d67616bf/setup.py#L11-L27
# https://github.com/google/or-tools/issues/616#issuecomment-371480314
try:
    from wheel.bdist_wheel import bdist_wheel as bdist_wheel
    class bdist_wheel_impure(bdist_wheel):

        def finalize_options(self):
            bdist_wheel.finalize_options(self)
            # Mark us as not a pure python package
            self.root_is_pure = False

        def get_tag(self):
            python, abi, plat = bdist_wheel.get_tag(self)
            # We don't contain any python source
            python, abi = 'py2.py3', 'none'
            return python, abi, plat

    from setuptools.command.install import install
    class install_platlib(install):
        def finalize_options(self):
            install.finalize_options(self)
            self.install_lib = self.install_platlib

except ImportError:
    bdist_wheel_impure = None
    install_platlib = None


here = os.path.abspath(os.path.dirname(__file__))

# https://packaging.python.org/guides/single-sourcing-package-version/
def read(*parts):
    with open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

version = find_version('wav2vec2_stt', '__init__.py')
if version.endswith('dev0'):
    version = version[:-1] + datetime.datetime.now().strftime('%Y%m%d%H%M%S')

with open(os.path.join(here, 'README.md')) as f:
    long_description = f.read()

cmake_prefix_path = subprocess.check_output(['python', '-c', 'import torch;print(torch.utils.cmake_prefix_path)'], text=True).strip()


setup(
    cmdclass={
        'bdist_wheel': bdist_wheel_impure,
        'install': install_platlib,
    },
    cmake_args=['-DCMAKE_PREFIX_PATH=' + cmake_prefix_path],

    name='wav2vec2_stt',
    version=version,
    # description='wav2vec2_stt',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/daanzu/wav2vec2_stt',
    author='David Zurow',
    author_email='daanzu@gmail.com',
    license='AGPL-3.0',
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    # keywords='speech recognition',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.6, <4',
    install_requires=[
        'cffi ~= 1.12',
        'numpy ~= 1.16, != 1.19.4',
    ],
    extras_require={
        # 'dev': ['check-manifest'],
        'test': ['pytest'],
    },
    package_data={
        'wav2vec2_stt': ['libwav2vec2_stt_lib.*'],
        '': ['LICENSE'],
    },
    project_urls={
        'Bug Reports': 'https://github.com/daanzu/wav2vec2_stt/issues',
        'Funding': 'https://github.com/sponsors/daanzu',
        # 'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/daanzu/wav2vec2_stt/',
    },
)
