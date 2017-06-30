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
#     spack install simplemoc
#
# You can edit this file again by typing:
#
#     spack edit simplemoc
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Simplemoc(MakefilePackage):
    """The purpose of this mini-app is to demonstrate the performance
	characterterics and viability of the Method of Characteristics (MOC)
	for 3D neutron transport calculations in the context of full scale
	light water reactor simulation."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/ANL-CESAR/SimpleMOC/"
    url      = "https://github.com/ANL-CESAR/SimpleMOC/archive/master.tar.gz"

    # FIXME: Add proper versions and checksums here.
    version('1.2.3', 'd8827221a4ae76e9766a32e16d143e60')

    variant('debug',     default=False,  description='Enable debugging.')
    variant('optimize',     default=False,  description='Do Optimizations.')
    variant('papi',     default=False,  description='Enable PAPI support.')
    variant('mpi',     default=False,  description='Built with MPI support.')
    variant('openmp',     default=False,  description='Built with OpenMP support.')


    # FIXME: Add dependencies if required.
    depends_on('mpi', when='+mpi')
    depends_on('openmpi', when='+openmp')

    build_targets = ['--directory=src']

    def edit(self, spec, prefix):

	makefile = FileFilter('src/Makefile')

	cflags = '-std=gnu99'
	ldflags = '-lm'

        if len(self.compiler.name) <= 0 or self.compiler.name == 'gcc':
                makefile.filter('CC =.*', 'CC = gcc')

	if self.compiler.name == 'icc':
		makefile.filter('CC = .*', 'CC = icc')

	if self.compiler.name == 'mpicc':
		makefile.filter('CC =.*', 'CC = mpicc')
		cflags += ' ' + '-O5 -qhot -qsimd=auto -qalias=ansi:allptrs -qarch=qp -DIBM -DMPI'


	if '+debug' in spec:
		cflags += ' ' + '-g'
	
	if '+profile' in spec:
		cflags += ' ' + '-pg'

	if '+optimize' in spec and self.compiler.name == 'gcc':
		cflags += ' ' + '-Ofast -ffast-math -ftree-vectorize -msse2'

	if '+optimize' in spec and self.compiler.name == 'icc':
		cflags += ' ' + '-O3 -xhost -ansi-alias -no-prec-div -DINTEL'

	if '+papi' in spec:
		cflags += ' ' + '-DPAPI -DOPENMP'
		ldflags += ' ' + '-lpapi'

	if '+papi' in spec and self.compiler.name == 'gcc':
		cflags += ' ' + '-fopenmp'

	if '+papi' in spec and self.compiler.name == 'icc':
                cflags += ' ' + '-openmp'

	if '+papi' in spec and self.compiler.name == 'mpicc':
                cflags += ' ' + '-qsmp'

	if '+papi' in spec and self.compiler.name == 'icc':
                cflags += ' ' + '-openmp'

	makefile.filter('CFLAGS .*', 'CFLAGS = {0}'.format(cflags))

    def install(self, spec, prefix):
        # FIXME: Unknown build system
	mkdir(prefix.bin)
        make('src/SimpleMOC', prefix.bin)
