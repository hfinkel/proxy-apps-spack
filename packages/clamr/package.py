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


class Clamr(Package):
    """The CLAMR code is a cell-based adaptive mesh refinement (AMR) mini-app developed as a testbed for hybrid algorithm development using MPI and OpenCL GPU code."""

    homepage = "https://github.com/lanl/CLAMR"
    url      = "https://github.com/lanl/CLAMR/archive/PowerParser_v2.0.7.tar.gz"

    version('2.0.7', '2f017fb80cb23e3771048e4c73c22dfa')

    # FIXME: Add dependencies if required.
    # depends_on('foo')
    # depends_on('mpi')
    # depends_on('

    #def install(self, spec, prefix):
        # FIXME: Unknown build system
        # make()
        # make('install')
