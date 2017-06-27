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
#     spack install minixyce
#
# You can edit this file again by typing:
#
#     spack edit minixyce
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
import os
from spack import *

class Minixyce(MakefilePackage):
    """A portable proxy of some of the key capabilities in the electrical modeling Xyce."""

    homepage = "https://mantevo.org"
    url      = "http://mantevo.org/downloads/releaseTarballs/miniapps/MiniXyce/miniXyce_1.0.tar.gz"

    version('1.0', '6fc0e5a561af0b8ff581d9f704194133')

    variant('mpi', default=True, description='Build with MPI Support')

    depends_on('mpi', when='+mpi')

    def edit(self, spec, prefix):
        makefile = FileFilter('miniXyce_ref/Makefile')
        
        if '+mpi' in spec:
            makefile.filter('CXX=.*', 'CXX = {}'.format(spec['mpi'].mpicxx))
            makefile.filter('LINKER=.*', 'LINKER = {}'.format(spec['mpi'].mpicxx))
            makefile.filter('USE_MPI = .*', 'USE_MPI = -DHAVE_MPI -DMPICH_IGNORE_CXX_SEEK')
        else:
            makefile.filter('CXX=.*', 'CXX = c++')
            makefile.filter('LINKER=.*', 'LINKER = c++')
            makefile.filter('USE_MPI = .*', 'USE_MPI = ')

        makefile.filter('CPP_OPT_FLAGS = .*', 'CPP_OPT_FLAGS = -O3')

    def build(self, spec, prefix):
        os.chdir('miniXyce_ref')
        # Script targets must be called in order for created files to be visible
        make('generate_info')
        make('common_files')
        make()
        
     
    def install(self, spec, prefix):
        # Manual Installation
        mkdirp(prefix.bin)
        mkdirp(prefix.tests)
        mkdirp(prefix.doc)
        install('miniXyce.x', prefix.bin)
        install('default_params.txt', prefix.bin)
        install('../README', prefix.doc)

        # Install test data files
        for f in os.listdir('tests'):
            print(f)
            if os.path.isfile(join_path(self.build_directory, 'tests/{}'.format(f))) == True:
                install('tests/{}'.format(f), prefix.tests)
            else:
                mkdirp(join_path(prefix.tests, f))
                for d in os.listdir(join_path(self.build_directory, 'tests/{}'.format(f))):
                    install('tests/{}/{}'.format(f,d), join_path(prefix.tests, f))
