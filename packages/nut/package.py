##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install nut
#
# You can edit this file again by typing:
#
#     spack edit nut
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
import glob

class Nut(CMakePackage):
    """NuT is Monte Carlo code for neutrino transport and is a C++ analog to the Haskell McPhD code. NuT is principally aimed at exploring on-node parallelism and performance issues."""

    homepage = "https://github.com/lanl/NuT"
    url      = ""
    tags     = ['proxy-app']

    version('serial', git='https://github.com/lanl/NuT.git', branch='master')
    version('openmp', git='https://github.com/lanl/NuT.git', branch='openmp')

    depends_on('random123')
    depends_on('openmp', when='@openmp')

    def cmake_args(self):
        cmakefile = FileFilter('CMakeLists.txt')
        cmakefile.filter('# create variable.*', 'set(ENV{RANDOM123_DIR} prefix/../random123*)')
        cmakefile.filter('# set compiler .*', 'set(ENV{CC} cc)')
        cmakefile.filter('# GNU .*', 'set(ENV{CXX} c++)')

        self.build_targets.extend(['VERBOSE=on -j 4 2>&1 | tee -a make.out'])

        args = []
        return args

    def install(self, spec, prefix):
        install('README.md', prefix)
        mkdirp('test', prefix)
        install_tree(join_path(self.build_directory, 'test'), join_path(prefix, 'test'))
