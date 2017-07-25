##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
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
from spack import *


class Cogl(CMakePackage):
    """CoGL is a meso-scale simulation proxy app used to analyze CoGL
    pattern formation in ferroelastic materials using the ginzburg-landau 
    approach. It has been publicly released on the ExMatEx Project Github Repo.
    """

    homepage = "http://www.exmatex.org/cogl.html"
    url      = "https://github.com/exmatex/CoGL/archive/master.tar.gz"

    version('master', git='https://github.com/exmatex/CoGL.git', description='master')

    variant('cuda', default=True,description='Enable CUDA')
    variant('interop', default=True,description='Enable INTEROP')
    variant('mac', default=True, description='Apple Verison`')

    depends_on('cuda', when='+cuda')


    def cmake_args(self):
        cmake_args = []
        if '+mac' in self.spec:
            cmake_args.append('--APPLE=ON')
        if '+interop' in self.spec:
            cmake_args.append('--ENABLE_INTEROP=ON')
        if '+cuda' in self.spec:
            cmake_args.append('--USE_CUDA=ON')
        return cmake_args

    def install(self, spec, prefix):
        pass