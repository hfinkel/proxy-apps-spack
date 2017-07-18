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
#     spack install cns-nospec
#
# You can edit this file again by typing:
#
#     spack edit cns-nospec
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
import glob


class CnsNospec(MakefilePackage):
    """A simple, explicit, stencil-based test code for integrating the the compressible Navier-Stokes equations. The code uses 8th order finite differences in space and a 3rd order, low-storage TVD RK algorithm in time."""

    homepage = "https://ccse.lbl.gov/ExaCT/index.html"
    url      = "https://ccse.lbl.gov/ExaCT/CNS_Nospec.tgz"

    version('master', '14ff5be62539d829b30b17281688ee3f')

    variant('mpi', default=False, description='Build with MPI support')
    variant('debug', default=True, description='Build with debugging')
    variant('mkverbose', default=True, description='Build with verbose')
    variant('omp', default=False, description='Build with OpenMP support')
    variant('prof', default=False, description='Build with profiling')

    @property
    def build_directory(self):
        return join_path(self.stage.source_path, 'MiniApps', 'CNS_NoSpec')

    def edit(self, spec, prefix):
        makefile = FileFilter('GNUmakefile')
        if '+mpi' in spec:
            makefile.filter('MPI .*', 'MPI := t')
        if '+debug' not in spec:
            makefile.filter('NDEBUG.*', '#')
        if '+mkverbose' not in spec:
            makefile.filter('MKVERBOSE.*', '#')
        if '+omp' in spec:
            makefile.filter('OMP.*', 'OMP := t')
        if '+prof' in spec:
            makefile.filter('PROF.*', 'PROF := t')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        files = glob.glob(join_path(self.build_directory, '*.exe'))
        for f in files:
            install(f, prefix.bin)
