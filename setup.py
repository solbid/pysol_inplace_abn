# Copyright (c) Facebook, Inc. and its affiliates.

from os import path, walk, getenv

import setuptools
import torch
from torch.utils.cpp_extension import BuildExtension, CUDAExtension, CppExtension
import numpy
from pybind11 import get_include




def find_sources(root_dir, with_cuda=True):
    extensions = [".cpp", ".cu"] if with_cuda else [".cpp"]

    sources = []
    for subdir, _, files in walk(root_dir):
        for filename in files:
            _, ext = path.splitext(filename)
            if ext in extensions:
                sources.append(path.join(subdir, filename))

    return sources


here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

if torch.cuda.is_available() or getenv("IABN_FORCE_CUDA") == "1":
    ext_modules = [
        CUDAExtension(
            name="inplace_abn._backend",
            sources=find_sources("src"),
            extra_compile_args={
                "cxx": ["-O3"],
                "nvcc": ["-arch=sm_86"],  # NVIDIA RTX A5500 has a Compute Capability of 8.6
            },
            # include_dirs=[path.join(here, "include")],
            include_dirs=[
                numpy.get_include(), # ensure that the correct NumPy headers are included
                get_include(), # include the headers for Pybind11 in the C++ code during compilation
                path.join(here, "include")
            ],
            define_macros=[("WITH_CUDA", 1)],
        )
    ]
else:
    ext_modules = [
        CppExtension(
            name="inplace_abn._backend",
            sources=find_sources("src", False),
            extra_compile_args=["-O3"], # , "-std=c++17"
            include_dirs=[path.join(here, "include")],
        )
    ]

setuptools.setup(
    # Meta-data
    name="inplace-abn",
    author="Lorenzo Porzi",
    author_email="lorenzo@mapillary.com",
    description="In-Place Activate BatchNorm for Pytorch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mapillary/inplace_abn",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.10",
    ],
    # Versioning
    use_scm_version={
        "root": ".",
        "relative_to": __file__,
        "write_to": "inplace_abn/_version.py",
    },
    # Requirements
    setup_requires=["setuptools_scm"],
    python_requires=">=3, <4",
    install_requires=[
        "numpy>=2",
        "pybind11>=2.13.6",
    ],
    # Package description
    packages=["inplace_abn"],
    ext_modules=ext_modules,
    cmdclass={"build_ext": BuildExtension},
)
