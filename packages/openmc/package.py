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
#     spack install openmc
#
# You can edit this file again by typing:
#
#     spack edit openmc
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
import os


class Openmc(MakefilePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/ANL-CESAR/"
    url      = "https://github.com/ANL-CESAR/openmc.git"

    tags = ['proxy-app']

    # FIXME: Add proper versions and checksums here.
    #version('1.2.3', '0123456789abcdef0123456789abcdef')
    version('master', git='https://github.com/ANL-CESAR/openmc.git')

    # FIXME: Add dependencies if required.
    # depends_on('foo')

    build_targets = ['--directory=src']

    def edit(self, spec, prefix):
	
	makefile = FileFilter('src/Makefile')
        self.build_targets.extend(['COMPILER=gnu'])
	self.build_targets.extend(['MACHINE=UNKNOWN'])
	if self.compiler.name == 'ifort':
		self.build_targets.extend(['COMPILER=intel'])
	if self.compiler.name == 'pgf90':
                self.build_targets.extend(['COMPILER=pgi'])
	if self.compiler.name == 'xlf2003':
                self.build_targets.extend(['COMPILER=ibm'])
	if self.compiler.name == 'ftn':
                self.build_targets.extend(['COMPILER=cray'])
	if self.compiler.name == 'mpixlf2003':
		self.build_targets.extend(['MACHINE=bluegenep'])

    def install(self, spec, prefix):
        # FIXME: Unknown build system
        #make('openmc')
	print(prefix)
	if not os.path.exists(prefix.bin):
		mkdir(prefix.bin)
	if not os.path.exists(prefix.bin + '/statepoint_cmp'):
		mkdir(prefix.bin + '/statepoint_cmp')
	if not os.path.exists(prefix.bin + '/statepoint_histogram'):
		mkdir(prefix.bin + '/statepoint_histogram')
	if not os.path.exists(prefix.bin + '/statepoint_meshpoint'):
		mkdir(prefix.bin + '/statepoint_meshpoint')
	if not os.path.exists(prefix + '/share'):
		mkdir(prefix + '/share')
	if not os.path.exists(prefix + '/share/man'):
		mkdir(prefix + '/share/man')
	if not os.path.exists(prefix + 'share/man/man1/'):
		mkdir(prefix + '/share/man/man1/')
	if not os.path.exists(prefix + 'share/man/man1/openmc.1'):
		mkdir(prefix + '/share/man/man1/openmc.1')
	if not os.path.exists(prefix + 'share/doc'):
		mkdir(prefix + '/share/doc')
	if not os.path.exists(prefix + 'share/doc/openmc'):
		mkdir(prefix + '/share/doc/openmc')
	if not os.path.exists(prefix + 'share/doc/openmc/copyright'):
		mkdir(prefix + '/share/doc/openmc/copyright')
	
	install('src/openmc', prefix.bin)
	install('src/utils/statepoint_cmp.py', prefix.bin + '/statepoint_cmp')
	install('src/utils/statepoint_histogram.py', prefix.bin + '/statepoint_histogram')
	install('src/utils/statepoint_meshplot.py', prefix.bin + '/statepoint_meshpoint')
	install('man/man1/openmc.1', prefix + '/share/man/man1/openmc.1')
	install('LICENSE', prefix + '/share/doc/openmc/copyright')
