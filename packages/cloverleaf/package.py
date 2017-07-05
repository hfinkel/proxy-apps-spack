##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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

import re
import glob

from spack import *


class Cloverleaf(MakefilePackage):
    """Proxy Application. CloverLeaf is a miniapp that solves the 
       compressible Euler equations on a Cartesian grid, 
       using an explicit, second-order accurate method.  
    """

    homepage = "http://uk-mac.github.io/CloverLeaf"
    url      = "http://mantevo.org/downloads/releaseTarballs/miniapps/CloverLeaf/CloverLeaf-1.1.tar.gz"

    tags = ['proxy-app']

    version('1.1', '65652b30a64eb237ec844a6fdd4cd518')

    variant('build', default='ref', description='Type of Parallelism Build', 
            values=('CUDA', 'MPI', 'OpenACC_CRAY', 'OpenMP', 'ref', 'Serial'))

    depends_on('mpi') 
    depends_on('cuda', when='build=CUDA')

    # Holds build variant value
    type_of_build = ''

    def edit(self, spec, prefix):
        # Capture build value in spec
        build_search = re.search('build=([.\S]+)', str(spec))
        self.type_of_build = build_search.group(1)

        # OpenMP build folder depends on openMP version
        if self.type_of_build:
            if self.type_of_build == 'OpenMP':
                if '%gcc' in spec and int(self.compiler.version.up_to(1)) >= 5:
                    self.type_of_build = 'OpenMP4'
                else:
                    self.type_of_build = 'OpenMP'

            self.build_targets.extend(
                ['--directory=CloverLeaf_{}'.format(self.type_of_build)])

        self.build_targets.extend(
            ['MPI_COMPILER={}'.format(spec['mpi'].mpifc), 
             'C_MPI_COMPILER={}'.format(spec['mpi'].mpicc)])

        # Use Makefile compiler specific flags
        if '%gcc' in spec:
            self.build_targets.extend(['COMPILER=GNU'])
        elif '%cce' in spec:
            self.build_targets.extend(['COMPILER=CRAY'])
        elif '%intel' in spec:
            self.build_targets.extend(['COMPILER=INTEL'])
        elif '%pgi' in spec:
            self.build_targets.extend(['COMPILER=PGI'])
        elif 'xl' in spec:
            self.build_targets.extend(['COMPILER=XLF'])


    def install(self, spec, prefix):
        # Manual Installation
        mkdirp(prefix.bin)
        mkdirp(prefix.doc.tests)

        install('COPYING', prefix.doc)
        install('COPYING.LESSER', prefix.doc)
        install('README.md', prefix.doc)
        install('documentation.txt', prefix.doc)

        if self.type_of_build:
            install('CloverLeaf_{}/clover_leaf'.format(self.type_of_build),
                     prefix.bin)
            install('CloverLeaf_{}/clover.in'.format(self.type_of_build),  
                     prefix.bin)

            for f in glob.glob(
                    'CloverLeaf_{}/*.in'.format(self.type_of_build)):
                install(f, prefix.doc.tests)
