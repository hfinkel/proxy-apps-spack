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
import shutil


class Vpfft(CMakePackage):
    """ Proxy Application. VPFFT is an implementation of a mesoscale 
    micromechanical materials model. By solving the viscoplasticity 
    model, VPFFT simulates the evolution of a material under deformation.
    The solution time to the viscoplasticity model, described by a set
    of partial differential equations, is significantly reduced by the
    application of Fast Fourier Transform in the VPFFT algorithm.
    """

    tag = ['proxy-app']
    homepage = "http://www.exmatex.org/vpfft.html"
    url      = "https://github.com/exmatex/VPFFT/archive/master.tar.gz"

    version('master', git='https://github.com/exmatex/VPFFT.git')

    depends_on('cmake@2.4:', type='build')
    depends_on('eigen')
    depends_on('fftw')

    phases = ['edit', 'cmake', 'build', 'install']

    def edit(self, spec, prefix):
        with working_dir(self.stage.source_path):
            shutil.move('CMakeBuild/CMakeLists.txt.example', 'CMakeLists.txt')
            cmake_file = FileFilter('CMakeLists.txt')
            cmake_file.filter('set.*CMAKE_C_COMPILER.*', 'set(CMAKE_C_COMPILER "{0}")'.format(self.spec['mpi'].mpicc))
            cmake_file.filter('set.*CMAKE_CXX_COMPILER.*', 'set(CMAKE_CXX_COMPILER "{0}")'.format(self.spec['mpi'].mpicxx))
            cmake_file.filter('set.*EIGEN_PATH.*', 'set(EIGEN_PATH "{0}/include/eigen3")'.format(self.spec['eigen'].prefix))
            cmake_file.filter('set.*FFTW_PATH.*', 'set(FFTW_PATH "{0}/include")'.format(self.spec['fftw'].prefix))
