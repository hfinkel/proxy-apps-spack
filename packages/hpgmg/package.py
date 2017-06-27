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
#     spack install hpgmg
#
# You can edit this file again by typing:
#
#     spack edit hpgmg
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Hpgmg(AutotoolsPackage):
    """HPGMG implements full multigrid (FMG) algorithms using finite-volume and finite-element methods. Different algorithmic variants adjust the arithmetic intensity and architectural properties that are tested. These FMG methods converge up to discretization error in one F-cycle, thus may be considered direct solvers. An F-cycle visits the finest level a total of two times, the first coarsening (8x smaller) 4 times, the second coarsening 6 times, etc."""

    homepage = "https://bitbucket.org/hpgmg/hpgmg"
    url      = "https://bitbucket.org/hpgmg/hpgmg/get/master.tar.gz"

    variant('fe', default=True, description='Build Finite Element FAS solver')
    variant('fv', default=True, description='Build Finite Volume solver')
    variant('mpi', default=False, description='Build with MPI support')

    depends_on('petsc', when='+fe')
    depends_on('openmp', when='+fv')
    depends_on('mpi', when='+mpi')

    # def configure_args(self):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        # args = []
        # return args
