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
#     spack install rsbench
#
# You can edit this file again by typing:
#
#     spack edit rsbench
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Rsbench(MakefilePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/ANL-CESAR/RSBench"
    url      = "https://github.com/ANL-CESAR/RSBench/archive/v2.tar.gz"

    version('2', '15a3ac5ea72529ac1ed9ed016ee68b4f')
    version('0', '3427634dc5e7cd904d88f9955b371757')

    variant('debug',     default=False,  description='Enable debugging.')
    variant('optimize',     default=False,  description='Do Optimizations.')
    variant('papi',     default=False,  description='Enable PAPI support.')
    variant('status', default=False, description='Enable status flag.')
    variant('openmp', default=True, description='Built with OpenMP support.')

    # FIXME: Add dependencies if required.
    depends_on('openmp')

    build_targets = ['--directory=src']

    def edit(self, spec, prefix):

	makefile = FileFilter('src/makefile')

        cflags = '-std=gnu99 -fopenmp -ffast-math'
        ldflags = '-lm'

	if len(self.compiler.name) <= 0 or self.compiler.name == 'gcc':
                makefile.filter('CC =.*', 'CC = gcc')

	if '+debug' in spec: 
                cflags += ' ' + '-g'
        
        if '+profile' in spec:
                cflags += ' ' + '-pg'

	if '+optimize' in spec and self.compiler.name == 'icc':
                cflags += ' ' + '-O3'

	if '+status' in spec:
		cflags += ' ' + '-DSTATUS'

	if '+papi' in spec:
                cflags += ' ' + '-DPAPI'
		ldflags += ' ' + '-lpapi'
		makefile.filter('source =.*', 'source = {0}'.format('papi.c \\'))


	makefile.filter('CFLAGS .*', 'CFLAGS = {0}'.format(cflags))
	
    def install(self, spec, prefix):
        # FIXME: Unknown build system
	mkdir(prefix.bin)
        make('src/rsbench', prefix.bin)
