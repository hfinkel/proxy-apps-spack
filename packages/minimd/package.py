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
import glob
import tarfile

class Minimd(MakefilePackage):
    """Proxy Application. A simple proxy for the force computations in a typical molecular dynamics applications."""

    homepage = "http://mantevo.org"
    url      = "http://mantevo.org/downloads/releaseTarballs/miniapps/MiniMD/miniMD_1.2.tgz"

    tags = ['proxy-app']

    version('1.2', '893ef1ca5062e32b43a8d11bcfe1a056')

    depends_on('openmpi')

    build_version = ''

    def edit(self, spec, prefix):
        self.build_version = self.version.up_to(2)

        inner_tar = tarfile.open(name='miniMD_{}_ref.tgz'.format(self.build_version))
        inner_tar.extractall()

        self.build_targets.extend(['--directory=miniMD_ref'])
        self.build_targets.extend(['LINK={}'.format(spec['mpi'].mpicxx)])
        self.build_targets.extend(['CC={}'.format(spec['mpi'].mpicxx)])
        self.build_targets.extend(['CCFLAGS={} -DMPICH_IGNORE_CXX_SEEK -DNOCHUNK'.format(self.compiler.openmp_flag)])

        self.build_targets.extend(['openmpi'])

    def install(self, spec, prefix):
        # Manual Installation
        mkdirp(prefix.bin)
        mkdirp(prefix.doc)

        install('miniMD_ref/miniMD_openmpi', prefix.bin)
        install('miniMD_ref/in.lj.miniMD', prefix.bin)
        install('miniMD_ref/README', prefix.doc)

        for f in glob.glob('miniMD_ref/in.*'):
            install(f, prefix.doc)
