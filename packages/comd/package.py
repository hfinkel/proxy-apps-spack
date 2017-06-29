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


class Comd(MakefilePackage):
    """The molecular dynamics (MD) computer simulation method is a 
    well-established and important tool for the study of the dynamical 
    properties of liquids, solids, and other systems of interest in 
    Materials Science and Engineering, Chemistry and Biology. 
    A material is represented in terms of atoms and molecules."""

    homepage = "http://www.exmatex.org/comd.html"
    url      = "https://github.com/exmatex/CoMD/archive/master.tar.gz"

    version('master',git='https://github.com/exmatex/CoMD.git',branch='master')    
    
    variant('precision', default=True, description='for Precision options')
    variant('mpi', default=True, description='Build with MPI support')
    variant('openmp', default=True, description='Build with OpenMP support')
   
    depends_on('mpi', when='+mpi')    

    def edit(self, spec, prefix):
        if '+openmp' in spec: 
            makefile = FileFilter('src-openmp/Makefile.vanilla')
        else:
            makefile = FileFilter('src-mpi/Makefile.vanilla')
            

        makefile.filter('CC   = .*', 'CC = {}'.format(spec['mpi'].mpicc))

        if '+openmp' in spec:
            self.build_targets.extend(['--directory=src-oprmmp', '--file=Makefile.vanilla'])
            makefile = FileFilter('src-openmp/Makefile.vanilla')
            if '+mpi' in spec:
                ### mpi and opemmp variant 

                pass
            else:
                ## openmp variant

                pass
        else:
            ### MPI variant
            self.build_targets.extend(['--directory=src-oprmmp', '--file=Makefile.vanilla'])
            makefile = FileFilter('src-mpi/Makefile.vanilla')
            if '+mpi' not in spec:
                ### serial variant
                makefile.filter('CC   = .*', 'CC = gcc')
                


    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdirp(prefix.examples)
        mkdirp(prefix.pots)
        mkdirp(prefix.doc)
        install("examples/*",prefix.examples)
        install("pots/*",prefix.pots)
        install('README', prefix.doc)
        install('LICENSE', prefix.doc)

        if '+openmp' in spec:
            if '+mpi' in spec:
                ### mpi and opemmp variant 
                install('CoMD-openmp', prefix.bin)
            else:
                ## openmp variant
                install('CoMD-openmp-mpi', prefix.bin)
        else:
            if '+mpi' in spec:
                ### mpi variant
                install('CoMD-mpi', prefix.bin)
            else:
                ### serial variant
                install('CoMD-serial', prefix.bin)









