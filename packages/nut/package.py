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
from spack import *


class Nut(CMakePackage):
    """NuT is Monte Carlo code for neutrino transport and
    is a C++ analog to the Haskell McPhD code.
    NuT is principally aimed at exploring on-node parallelism
    and performance issues."""

    homepage = "https://github.com/lanl/NuT"
    url      = "https://github.com/lanl/NuT.git"
    tags     = ['proxy-app']

    version(
        'serial', git='https://github.com/lanl/NuT.git',
        branch='master')
    version(
        'openmp', git='https://github.com/lanl/NuT.git',
        branch='openmp')

    depends_on('random123')

    # serial must be built with clang
    conflicts('%gcc', when='@serial')
    conflicts('%intel', when='@serial')
    conflicts('%pgi', when='@serial')
    conflicts('%xl', when='@serial')
    conflicts('%nag', when='@serial')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('RANDOM123_DIR', self.spec['random123'].prefix)

    build_targets = ['VERBOSE=on']

    def install(self, spec, prefix):
        install('README.md', prefix)
        mkdirp(prefix.bin)
        install('spack-build/test/nut_unittests', prefix.bin)
