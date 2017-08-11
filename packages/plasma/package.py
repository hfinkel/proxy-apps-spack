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

    depends_on('trilinos', when='~3d')
    depends_on('paraview', when='~3d')
    depends_on('mesa', when='~3d')
    depends_on('gmake', type='build')
    depends_on('mpi')
    depends_on('cuda', when='+cuda')
    depends_on('cuda', when='+3d')

    @property
    def build_directory(self):
        if '+3d' in self.spec:
            build_directory = join_path(self.stage.source_path, 'PlasmaApp3D')
        else:
            build_directory = join_path(self.stage.source_path, 'PlasmaApp')
        return build_directory

    def edit(self, spec, prefix):
        makefile = FileFilter('{0}/Makefile'.format(self.build_directory))
        makefile.filter('TOP_DIR=.*', 'TOP_DIR={0}'.format(self.build_directory))
        makefile.filter('CC=.*', 'CC = cc')
        makefile.filter('CXX=.*', 'CXX = {}'.format(spec['mpi'].mpicxx))
        
        if '+3d' in spec:
            makefile.filter('NVCC =.*', 'NVCC = %s/bin/nvcc' % spec['cuda'].prefix)
            self.build_targets.append('USECUDA=1')

        if '+nohandvec' in spec:
            self.build_targets.append('NOHANDVEC=1')

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            #make('packages')
            if '~3d' in spec:
                with working_dir(join_path(self.build_directory, 'src')):
                    make('all')
            else:
                make('USECUDA=1')

    def install(self, spec, prefix):       
        if '~3d' in spec:
            install('/src/tests', prefix.tests)
        else:
            install_tree('PlasmaApp3D/bin', prefix.bin)
            install_tree('PlasmaApp3D/tests', prefix.tests)
