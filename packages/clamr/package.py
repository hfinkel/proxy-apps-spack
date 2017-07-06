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
#     spack install clamr
#
# You can edit this file again by typing:
#
#     spack edit clamr
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
import inspect

class Clamr(CMakePackage):
    """The CLAMR code is a cell-based adaptive mesh refinement (AMR) mini-app developed as a testbed for hybrid algorithm development using MPI and OpenCL GPU code."""

    homepage = "https://github.com/lanl/CLAMR"
    url      = ""
    tags     = ['proxy-app', 'ecp-proxy-app']

    version('master', git='https://github.com/lanl/CLAMR.git')

    variant('nographics', default=False, description='Build without GPU support')
    variant('opengl', default=True, description='Build with OpenGL')
    variant('debug', default=False, description='Debugging enabled')
    variant('release', default=False, description='Release version')
    variant('full', default=False, description='full double precision')
    variant('mixed', default=False, description='intermediates double, arrays single precision')
    variant('single', default=False, description='single precision')

    depends_on('mpi')
    depends_on('mpe', when='-opengl')

    def build_type(self):
        if '+debug' in self.spec:
            return 'Debug'
        if '+release' in self.spec:
            return 'Release'
        return 'RelWithDebInfo'

    def cmake_args(self):
       cmake_args = []
       if '+nographics' in self.spec:
           cmake_args.append('-DGRAPHICS_TYPE=None')
       elif '-opengl' in self.spec:
           cmake_args.append('-DGRAPHICS_TYPE=MPE')
       else:
           cmake_args.append('-DGRAPHICS_TYPE=OpenGL')

       if '+full' in self.spec:
           cmake_args.append('-DPRECISION_TYPE=full_precision')
       if '+single' in self.spec:
           cmake_args.append('-DPRECISION_TYPE=minimum_precision')
       if '+mixed' in self.spec:
           cmake_args.append('-DPRECISION_TYPE=mixed_precision')
        
       # if MIC, then -DMIC_NATIVE=yes
       return cmake_args

    def build(self, spec, prefix):
        print(self.rpath)
        build_targets = ['', 'check', 'clamr_tests', 'doc']
        with working_dir(self.build_directory):
            inspect.getmodule(self).make(*self.build_targets)

    def install(self, spec, prefix):
        install('README', prefix)
        install('LICENSE', prefix)
        install_tree('docs', join_path(prefix, 'docs'))
        install_tree('tests', join_path(prefix, 'tests'))
        install_tree('graphics', join_path(prefix, 'graphics'))
        with working_dir(self.build_directory):
            inspect.getmodule(self).make(*self.install_targets) 
