from setuptools import setup, find_packages
import numpy
from glob import glob
from os.path import join, abspath
import subprocess
import os
import shutil


name = 'pyhwm2014'

# Define the Fortran source file
fortran_source = 'source/hwm14.f90'
package_folder = os.path.join(name)

# Manually invoke f2py for the Fortran compilation
def build_extension():
    # Compile the Fortran file using f2py
    subprocess.check_call([
        'f2py', 
        '-c',  # Compile only
        '-m', 'hwm14',  # Module name (this creates PyInit_hwm14)
        fortran_source,  # Fortran source file
        '--f90flags=-w',  # Suppress warnings (optional)
        '--quiet',  # Quiet mode
        '-I{}'.format(numpy.get_include())  # Include NumPy headers
    ])
    compiled_files = glob('*.so')
    if compiled_files:
      for compiled_file in compiled_files:
        compiled_file_path = abspath(compiled_file)
        # Copy the compiled .so file into the package directory
        shutil.copy(compiled_file_path, package_folder)
        print(f"Successfully copied {compiled_file} to {package_folder}")
    else:
        raise FileNotFoundError("No compiled .so file found!")


# Call the build_extension function to compile the Fortran code
build_extension()

# Collect data files
hwmData1 = glob(join("data", "*.dat"))
hwmData2 = glob(join("data", "*.bin"))
hwmDataFiles = [(join(name, "data"), hwmData1),
                (join(name, "data"), hwmData2)]

# Define dependencies
req = ["nose", "numpy", "pathlib2", "timeutil"]

setup(
    author="Ronald Ilma",
    data_files=hwmDataFiles,
    description="HWM14 neutral winds model",
    ext_modules=[],  # No need to define the extension here, f2py handles it
    ext_package=name,
    name=name,
    packages=find_packages(),
    url="https://github.com/rilma/pyHWM14",
    version="1.1.0",
    install_requires=req,
    extras_require={"plot": ["matplotlib", "seaborn"]},
    dependency_links=[
        "https://github.com/rilma/TimeUtilities/zipball/master#egg=timeutil-999.0"
    ],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.10",
)
