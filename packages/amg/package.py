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
#     spack install amg
#
# You can edit this file again by typing:
#
#     spack edit amg
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Amg(MakefilePackage):
    """The "Monte Carlo Benchmark" (MCB) is intended for use in 
    exploring the computational performance of Monte Carlo algorithms 
    on parallel architectures. It models the solution of a simple 
    heuristic transport equation using a Monte Carlo technique. 
    The MCB employs typical features of Monte Carlo algorithms 
    such as particle creation, particle tracking, tallying particle 
    information, and particle destruction. Particles are also traded 
    among processors using MPI calls."""

    homepage = "https://codesign.llnl.gov/amg2013.php"
    url      = "https://codesign.llnl.gov/amg2013/amg2013.tgz"

    version('2013', '9d918d2a69528b83e6e0aba6ba601fef')
    #build_targets = ['--directory'='utilities','--directory'='krylov','--directory'='IJ_mv','--directory'='parcsr_ls', '--directory'='parcsr_mv','--directory'='seq_mv', '--directory'='struct_mv','--directory'='sstruct_mv', '--directory'='test']
    #build_targets = ['--directory= *']
    
    variant('mpi', default=True, description='Build with MPI support')
    variant('openmp', default=False, description='Build with OpenMP support')
    
    # FIXME: Add dependencies if required.
    # depends_on('foo')
    depends_on('mpi')
    depends_on('openmp',when="+openmp")



def edit(self, spec, prefix):
        makefile = FileFilter('*/Makefile')
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
        # Manual installation
    mkdirp(prefix.doc)
    install('docs', prefix.doc)
    install('COPYRIGHT', prefix.doc)
    install('COPYRIGHT.LESSER', prefix.doc)
















