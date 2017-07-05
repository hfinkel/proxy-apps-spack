##############################################################################
# Copyright (c) 2012-2016, Lawrence Livermore National Security, LLC.
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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install comd
#
# You can edit this file again by typing:
#
#     spack edit comd
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
import shutil
import os



class Comd(MakefilePackage):
    """The molecular dynamics (MD) computer simulation method is a 
    well-established and important tool for the study of the dynamical 
    properties of liquids, solids, and other systems of interest in 
    Materials Science and Engineering, Chemistry and Biology. 
    A material is represented in terms of atoms and molecules.

    Tag : proxy-app, ecp-proxy-app"""

    tag = ['proxy-app','ecp-proxy-app']
    homepage = "http://www.exmatex.org/comd.html"
    url      = "https://github.com/exmatex/CoMD/archive/master.tar.gz"

    version('master',git='https://github.com/exmatex/CoMD.git',branch='master')    
    
    variant('precision', default=True, description='for Precision options')
    variant('mpi', default=True, description='Build with MPI support')
    variant('openmp', default=True, description='Build with OpenMP support')
   
    depends_on('mpi', when='+mpi')    
    
    def edit(self, spec, prefix):
        shutil.copy('src-openmp/Makefile.vanilla','src-openmp/Makefile')
        shutil.copy('src-mpi/Makefile.vanilla','src-mpi/Makefile')
               
        if '+openmp' in spec:
            ### openmp and mpi variant
            self.build_targets.extend(['--directory=src-openmp', '--file=Makefile'])
            makefile = FileFilter('src-openmp/Makefile')
            makefile.filter('CFLAGS = .*', 'CFLAGS = -std=c99 -fopenmp')
        else:
            ### MPI variant
            self.build_targets.extend(['--directory=src-mpi', '--file=Makefile'])
            makefile = FileFilter('src-mpi/Makefile')
            makefile.filter('CFLAGS = .*','CFLAGS = -std=c99')
        
        makefile.filter('CC   = .*', 'CXX={}'.format(spec['mpi'].mpicxx))
        makefile.filter('C_LIB = .*','C_LIB = -lm')
        if '+mpi' not in spec:
            makefile.filter('CC   = .*', 'CC = gcc')
            makefile.filter('DO_MPI = .*','DO_MPI = OFF')

            
    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.examples)
        mkdirp(prefix.pots)
        mkdirp(prefix.doc)
        install('README.md', prefix.doc)
        install('LICENSE.md', prefix.doc)

        if '+openmp' in spec:
            if '+mpi' in spec:
                ### mpi and opemmp variant 
                install('bin/CoMD-openmp-mpi', prefix.bin)
            else:
                ## openmp variant
                install('bin/CoMD-openmp', prefix.bin)
        else:
            if '+mpi' in spec:
                ### mpi variant
                install('bin/CoMD-mpi', prefix.bin)
            else:
                ### serial variant
                install('bin/CoMD-serial', prefix.bin)










