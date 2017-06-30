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
from spack import *
import tarfile
import re

class Minife(MakefilePackage):
    """Proxy Application. MiniFE is an proxy application for unstructured implicit finite element codes."""

    homepage = "https://mantevo.org/"
    url      = "http://mantevo.org/downloads/releaseTarballs/miniapps/MiniFE/miniFE-2.0.1.tgz"

    version('2.0.1', '3113d7c8fc01495d08552672b0dbd015')

    variant('build', default='ref', description='Type of Parallelism',
            values=('ref', 'openmp_ref', 'qthreads')) 


    depends_on('mpi')
    depends_on('qthreads', when='build=qthreads')

    type_of_build = 'ref'

    def edit(self, spec, prefix):
        build_search = re.search('build=([.\S]+)', str(spec))
        self.type_of_build = build_search.group(1)

        inner_tar = tarfile.open(name='miniFE-2.0_{}.tgz'.format(self.type_of_build))
        inner_tar.extractall()

        makefile = FileFilter('miniFE-2.0_{}/src/Makefile'.format(self.type_of_build))
        makefile.filter('-fopenmp', self.compiler.openmp_flag, string=True)

        self.build_targets.extend(['--directory=miniFE-2.0_{}/src'.format(self.type_of_build)])
        self.build_targets.extend(['CXX={}'.format(spec['mpi'].mpicxx)])
        self.build_targets.extend(['CC={}'.format(spec['mpi'].mpicc)])

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('miniFE-2.0_{}/src/miniFE.x'.format(self.type_of_build), prefix.bin)


