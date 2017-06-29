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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install cloverleaf
#
# You can edit this file again by typing:
#
#     spack edit cloverleaf
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
import re
import glob

class Cloverleaf(MakefilePackage):
    """CloverLeaf is a miniapp that solves the compressible Euler equations on a Cartesian grid, using an explicit, second-order accurate method."""

    homepage = "http://uk-mac.github.io/CloverLeaf"
    url      = "http://mantevo.org/downloads/releaseTarballs/miniapps/CloverLeaf/CloverLeaf-1.1.tar.gz"

    version('1.1', '65652b30a64eb237ec844a6fdd4cd518')

    variant('build', default='ref', description='Type of Parallelism Build', values=('CUDA', 'MPI', 'Offload', 'OpenACC_CRAY', 'OpenMP', 'OpenMP4', 'ref', 'Serial'))

    depends_on('mpi') 
    depends_on('cuda', when='build=CUDA')

    def edit(self, spec, prefix):
        build_type = re.search('build=([.\S]+)', str(spec))
        if build_type:
            self.build_targets.extend(['--directory=CloverLeaf_{}'.format(build_type.group(1))])
            self.build_targets.extend(['MPI_COMPILER={}'.format(spec['mpi'].mpifc), 'C_MPI_COMPILER={}'.format(spec['mpi'].mpicc)])

        if '%gcc' in spec:
            self.build_targets.extend(['COMPILER=GNU'])

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.doc)
        build_type = re.search('build=([.\S]+)', str(spec))
        if build_type:
            folder = build_type.group(1)
            install('CloverLeaf_{}/clover_leaf'.format(folder), prefix.bin)
            install('CloverLeaf_{}/clover.in'.format(folder), prefix.bin)
            for f in glob.glob('CloverLeaf_{}/*.in'.format(folder)):
                install(f, prefix.doc)
