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
#     spack install snbone
#
# You can edit this file again by typing:
#
#     spack edit snbone
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
import os


class Snbone(MakefilePackage):
    """This application targets the primary computational solve burden of a SN,
       continuous finite element based transport equation solver."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/ANL-CESAR/"
    url = "https://github.com/ANL-CESAR/SNbone.git"

    # FIXME: Add proper versions and checksums here.
    version('master', git='https://github.com/ANL-CESAR/SNbone.git')

    # FIXME: Add dependencies if required.
    depends_on('metis')

    tags = ['proxy-app']

    def edit(self, spec, prefix):
	with working_dir('src_c', create=False):
	    if self.compiler.name == 'gcc':
		make('COMPILER=gfortran', 'LDFLAGS={0}'.format('-lm'))
            if self.compiler.name == 'mpixlf90_r':
	        make('COMPILER=bgq', 'LDFLAGS={0}'.format('-lm'))
            if self.compiler.name == 'icc':
		make('COMPILER=intel', 'LDFLAGS={0}'.format('-lm'))
   	with working_dir('src_fortran', create=False):
            if self.compiler.name == 'gcc':
                make('COMPILER=gfortran', 'LDFLAGS={0}'.format('-lm'))
            if self.compiler.name == 'mpixlf90_r':
                make('COMPILER=bgq', 'LDFLAGS={0}'.format('-lm'))
            if self.compiler.name == 'icc':
                make('COMPILER=intel', 'LDFLAGS={0}'.format('-lm'))
 
	with working_dir('src_makemesh', create=False):
            if self.compiler.name == 'gcc':
                make('COMPILER=gfortran', 'LDFLAGS={0}'.format('-lm'))
            if self.compiler.name == 'mpixlf90_r':
                make('COMPILER=bgq', 'LDFLAGS={0}'.format('-lm'))
            if self.compiler.name == 'icc':
                make('COMPILER=intel', 'LDFLAGS={0}'.format('-lm'))

	with working_dir('src_processmesh', create=False):
            if self.compiler.name == 'gcc':
                make('COMPILER=gfortran', 'METISLIB={0}'.format(spec['metis'].prefix + '/lib/libmetis.so'))
            if self.compiler.name == 'mpixlf90_r':
                make('COMPILER=bgq', 'LDFLAGS={0}'.format('-lm'))
            if self.compiler.name == 'icc':
                make('COMPILER=intel', 'LDFLAGS={0}'.format('-lm'))

    def build(self, spec, prefix):
    	pass

    def install(self, spec, prefix):
        # FIXME: Unknown build system
        with working_dir('src_c', create=False):
            mkdir(prefix.bin)
            if not os.path.exists(prefix.bin + '/C'):
                mkdir(prefix.bin + '/C')
            if not os.path.exists(prefix.bin + '/Fortran'):
                mkdir(prefix.bin + '/Fortran')
            if not os.path.exists(prefix.bin + '/MakeMesh'):
                mkdir(prefix.bin + '/MakeMesh')
            if not os.path.exists(prefix.bin + '/ProcessMesh'):
                mkdir(prefix.bin + '/ProcessMesh')
	    install('SNaCFE.x', prefix.bin + '/C')
            install('../src_fortran/SNaCFE.x', prefix.bin + '/Fortran')
            install('../src_makemesh/makemesh.x', prefix.bin + '/MakeMesh')
	    install('../src_processmesh/processmesh.x', prefix.bin + '/ProcessMesh')

