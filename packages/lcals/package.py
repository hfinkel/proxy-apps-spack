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
#     spack install lcals
#
# You can edit this file again by typing:
#
#     spack edit lcals
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Lcals(MakefilePackage):
    """LCALS ("Livermore Compiler Analysis Loop Suite") is a collection of loop
       kernels based, in part, on historical "Livermore Loops" benchmarks
       (See the 1986 technical report: "The Livermore Fortran Kernels:
        A Computer Test of the Numerical Performance Range",
        by Frank H. McMahon, UCRL-53745.). The suite contains facilities to
        generate timing statistics and reports."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://codesign.llnl.gov/LCALS-downloads/"
    url = "https://codesign.llnl.gov/LCALS-downloads/lcals-v1.0.2.tgz"

    tags = ['proxy-app']

    version('1.0.2', '40c65a88f1df1436a2f72b7d3c986a21')

    # FIXME: Add dependencies if required.
    # depends_on('foo')

    def edit(self, spec, prefix):
        # FIXME: Edit the Makefile if necessary
        # FIXME: If not needed delete this function
        makefile = FileFilter('Makefile')

        self.build_targets.extend(['LCALS_ARCH={}'.format('x86_sse_gnu')])
        self.build_targets.extend(['CXX={}'.format('g++')])

        if self.compiler.name == 'icc':
            self.build_targets.extend(['LCALS_ARCH={}'.format('MIC')])
            self.build_targets.extend(['CXX={}'.format('icc')])
        if self.compiler.name == 'icpc':
            self.build_targets.extend(['LCALS_ARCH={}'.format('x86_sse_icc')])
            self.build_targets.extend(['CXX={}'.format('icpc')])
        if self.compiler.name == 'mpixlcxx':
            self.build_targets.extend(['LCALS_ARCH={}'.format('bgp_xlc9')])
            self.build_targets.extend(['CXX={}'.format('mpixlcxx')])
        if self.compiler.name == 'mpixlcxx_r':
            self.build_targets.extend(['LCALS_ARCH={}'.format('bgq_xlc12')])
            self.build_targets.extend(['CXX={}'.format('mpixlcxx_r')])
        if self.compiler.name == 'bgclang++11':
            self.build_targets.extend(['LCALS_ARCH={}'.format('bgq_clang')])
            self.build_targets.extend(['CXX={}'.format('bgclang++11')])
        if self.compiler.name == 'mpicxx-4.7.2x':
            self.build_targets.extend(['LCALS_ARCH={}'.format('bgq_gnu')])
            self.build_targets.extend(['CXX={}'.format('mpicxx-4.7.2')])

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('lcals.exe', prefix.bin)

