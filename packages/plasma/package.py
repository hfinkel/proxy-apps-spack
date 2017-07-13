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
from spack import *
import inspect


class Plasma(MakefilePackage):
    """PlasmaApp is a flexible implicit charge and
       energy conserving implicit PIC framework.
       This codes aims to demonstrate the potential of using
       a fluid plasma model to accelerate a kinetic model
       through a High-Low order system coupling.
       The multi-granularity of this problem gives it the ability
       to map well to emerging heterogeneous architectures
       with multiple levels of parallelism."""

    homepage = "https://github.com/cocomans/plasma/"
    url      = ""
    tags     = ['proxy-app']

    version('master', git='https://github.com/cocomans/plasma.git')

    variant(
        'cuda', default=False,
        description='Build with CUDA support')
    variant(
        'single_p', default=False,
        description='Use single precision')
    variant(
        'nohandvec', default=False,
        description='Disable hand vectorization')
    variant(
        '3d', default=False,
        description='Build PlasmaApp3D')

    depends_on('gmake', type='build')
    depends_on('mpi')
    depends_on('cuda', when='+cuda')

    def edit(self, spec, prefix):
        if '+3d' in spec:
            self.plasma_dir = join_path(self.build_directory, 'PlasmaApp3D')
        else:
            self.plasma_dir = join_path(self.build_directory, 'PlasmaApp')

        makefile = FileFilter(join_path(self.plasma_dir, 'Makefile'))
        makefile.filter('CC=.*', 'CC = cc')
        makefile.filter('CXX=.*', 'CXX = {}'.format(spec['mpi'].mpicxx))
        
        if '+cuda' in spec:
            makefile.filter('NVCC =.*', 'NVCC = nvcc')
            self.build_target.append('USECUDA=1')

        if '+nohandvec' in spec:
            self.build_target.append('NOHANDVEC=1')

    def build(self, spec, prefix):
        with working_dir(self.plasma_dir):
            gmake()
            gmake('tests')

    def install(self, spec, prefix):       
        mkdirp(prefix.bin)
        install('PlasmaApp/src/tests', prefix.tests)
