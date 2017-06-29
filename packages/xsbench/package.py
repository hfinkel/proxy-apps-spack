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
#     spack install xsbench
#
# You can edit this file again by typing:
#
#     spack edit xsbench
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Xsbench(MakefilePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://github.com/ANL-CESAR/XSBench/archive/v13.tar.gz"

    version('13', '72a92232d2f5777fb52f5ea4082aff37')

    variant('debug',     default=False,  description='Enable debugging.')
    variant('verify',     default=False,  description='Enable verification.')
    variant('benchmark',     default=False,  description='Adds outer benchmarking loop to do multiple trials for 1 < threads <= max_threads.')
    variant('binarydump',     default=False,  description='Binary dump for file I/O based initialization.')
    variant('binaryread',     default=False,  description='Binary read for file I/O based initialization.')

    # FIXME: Add dependencies if required.
    # depends_on('foo')

    build_targets = ['--directory=src']

    def edit(self, spec, prefix):
    # FIXME: Unknown build system
        makefile = FileFilter('src/Makefile')
        cflags = '-std=gnu99 -fopenmp'
        LDFLAGS = '-lm'
        makefile.filter('CC =.*', 'CC = gcc')
        if len(self.compiler.name) <= 0 or self.compiler.name == 'gcc':
            makefile.filter('CC =.*', 'CC = gcc')
        if self.compiler.name == 'icc':
            # Use the Spack compiler wrappers
            makefile.filter('CC =.*', 'CC = icc')
            cflags += ' -fopenmp'
        if self.compiler.name == 'mpicc':
            # Use the Spack compiler wrappers
            makefile.filter('CC =.*', 'CC = mpicc')
        if '+debug' in spec:        
            cflags += ' -ftree-vectorizer-verbose=6'
            print('Debugging enabled...')   
        if '+verify' in spec:
            cflags += ' -DVERIFICATION'
        if '+benchmark' in spec:
            cflags += ' -DBENCHMARK'
        if '+binarydump' in spec:
            cflags += ' -DBINARY_DUMP'                
        if '+binaryread' in spec:
            cflags += ' -DBINARY_READ'

        makefile.filter('CFLAGS .*', 'CFLAGS = {0}'.format(cflags))

    def install(self, spec, prefix):
        # Manual installation
        mkdir(prefix.bin)
        install('src/XSBench', prefix.bin)

