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
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 0s2111-1307 USA
##############################################################################
from spack import *
import glob


class Amg(MakefilePackage):
    """ The "Monte Carlo Benchmark" (MCB) is intended for use in 
        exploring the computational performance of Monte Carlo algorithms 
        on parallel architectures. It models the solution of a simple 
        heuristic transport equation using a Monte Carlo technique. 
        The MCB employs typical features of Monte Carlo algorithms 
        such as particle creation, particle tracking, tallying particle 
        information, and particle destruction. Particles are also traded 
        among processors using MPI calls.
        tags: proxy-app
    """
    tags = ['proxy-app']
    homepage = "https://codesign.llnl.gov/amg2013.php"
    url      = "https://codesign.llnl.gov/amg2013/amg2013.tgz"

    version('2013', '9d918d2a69528b83e6e0aba6ba601fef')

    
    variant('mpi', default=True, description='Build with MPI support')
    variant('openmp', default=False, description='Build with OpenMP support')
    
    depends_on('mpi',when='+mpi')


    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        makefile.filter('INCLUDE_CFLAGS =', 'INCLUDE_CFLAGS = -DTIMER_USE_MPI')
        makefile.filter('CXX=.*', 'CXX={}'.format(spec['mpi'].mpicxx))
        makefile.filter('LINKER=.*', 'LINKER={}'.format(spec['mpi'].mpicxx))

        if '+openmp' in self.spec:
            makefile.filter('INCLUDE_CFLAGS =', 'INCLUDE_CFLAGS = --DHYPRE_USING_OPENMP -DTIMER_USE_MPI')
            makefile.filter('#INCLUDE_LFLAGS = -fopenmp', 'INCLUDE_LFLAGS = {}'.format(self.compiler.openmp_flag))

        if '+lm' in self.spec:
            makefile.filter('INCLUDE_CFLAGS =', 'INCLUDE_CFLAGS = -DTIMER_USE_MPI -DHYPRE_USING_OPENMP -DHYPRE_NO_GLOBAL_PARTITION')
            makefile.filter('#INCLUDE_LFLAGS = -lm  -fopenmp ', 'INCLUDE_LFLAGS = {}'.format(self.compiler.openmp_flag))
        
        if '+qsmp' in self.spec:
            makefile.filter('INCLUDE_CFLAGS =', 'INCLUDE_CFLAGS = -O2 -DTIMER_USE_MPI -DHYPRE_USING_OPENMP -DHYPRE_LONG_LONG -DHYPRE_NO_GLOBAL_PARTITION')
            makefile.filter('#INCLUDE_LFLAGS = -lm -fopenmp -qsmp ', 'INCLUDE_LFLAGS = {}'.format(self.compiler.openmp_flag))


    def install(self, spec, prefix):
        install_tree('docs', prefix.doc)
        install('COPYRIGHT', prefix.doc)
        install('COPYING.LESSER', prefix.doc)
















