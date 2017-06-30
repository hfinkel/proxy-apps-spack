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
#     spack install plasma
#
# You can edit this file again by typing:
#
#     spack edit plasma
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Plasma(MakefilePackage):
    """PlasmaApp is a flexible implicit charge and energy conserving implicit PIC framework. This codes aims to demonstrate the potential of using a fluid plasma model to accelerate a kinetic model through a High-Low order system coupling. The multi-granularity of this problem gives it the ability to map well to emerging heterogeneous architectures with multiple levels of parallelism.

proxy-app
ecp-proxy-app"""

    homepage = "https://github.com/cocomans/plasma/"
    url      = ""

    version('master', git='https://github.com/cocomans/plasma.git')

    variant('cuda', default='False', description='Build with CUDA support')
    variant('single_p', default='False', description='Use single precision')
    variant('nohandvec', default='False', description='Disable hand vectorization')

    depends_on('gmake', type='build')
    depends_on('mpi')
    depends_on('cuda', when='+cuda')

    def edit(self, spec, prefix):
        makefile = FileFilter('./PlasmaApp/Makefile')
        makefile.filter('CC = .*', 'CC = {0}'.format(spec['mpi'].mpicc))
        
        if '+cuda' in spec:
            makefile.filter('CC = .*', 'CC = nvcc')
            # self.build_targets.extend('USECUDA=1')

        if '+nohandvec' in spec:
            # self.build_targets.extend('NOHANDVEC=1')

    # def build(self, spec, prefix):
        # self.build_directory = join_path(self.build_directory, 'PlasmaApp')
        
        # optional_flags = ''
        
        # gmake('packages')
        # gamke('tests')

    def install(self, spec, prefix):       
        mkdirp(prefix.bin)
        install('PlasmaApp/src/tests', prefix.tests)
