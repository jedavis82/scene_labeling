from pathlib import Path

from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

hof_module = Pybind11Extension(
    'hofpy',
    [str(fname) for fname in Path('src').glob('*.cpp')],
    include_dirs=['include'],
    extra_compile_args=['-O3']
)

setup(
    name='hofpy',
    version='0.2.0',
    author='Andrew Buck',
    author_email='buckar@missouri.edu',
    description='Python binding for Histogram of Forces',
    ext_modules=[hof_module],
    cmdclass={"build_ext": build_ext}
)