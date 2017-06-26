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
#     spack install smc
#
# You can edit this file again by typing:
#
#     spack edit smc
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Smc(MakefilePackage):
    """A minimalist high-order finite difference algorithm for combustion problems. It includes core discretizations for advection, diffusive transport and chemical kinetics. The models for computing diffusive transport coefficients have been replaced by a simplified approximation but the full structure of the discretization of the diffusive terms have been preserved."""

    homepage = "https://ccse.lbl.gov/ExaCT/index.html"
    url      = "https://ccse.lbl.gov/ExaCT/SMC.tar.gz"

    variant('mpi', default=TRUE, description='Build with MPI support')
    variant('openmp', default=TRUE, description='Build with OpenMP support')
    variant('ndebug', default=FALSE, description='Turn off debugging')
    variant('mic', default=FALSE, description='Compile for Intel Xeon Phi')
    variant('k_use_automatic', default=TRUE, description='Some arrays in kernels.F90 will be automatic)
    variant('mkverbose', default=TRUE, description='Verbosity of building process')

    if '-mpi' not in spec:
        depends_on('mpi')
    if '-openmp' not in spec:
        depends_on('openmp')
    if '+ndebug' in spec:
    if '+mic' in spec:
    if '-k_use_automatic' not in spec:
    if '-mkverbose' not in spec:

    # def edit(self, spec, prefix):
        # FIXME: Edit the Makefile if necessary
        # FIXME: If not needed delete this function
        # makefile = FileFilter('Makefile')
        # makefile.filter('CC = .*', 'CC = cc')
