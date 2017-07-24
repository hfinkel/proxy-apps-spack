##############################################################################
# Copyright (c) 2012-2016, Lawrence Livermore National Security, LLC.
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


class Comd(MakefilePackage):
    """CoMD is a reference implementation of classical molecular dynamics
    algorithms and workloads as used in materials science. It is created and
    maintained by The Exascale Co-Design Center for Materials in Extreme
    Environments (ExMatEx). The code is intended to serve as a vehicle for
    co-design by allowing others to extend and/or reimplement it as needed to
    test performance of new architectures, programming models, etc. New
    versions of CoMD will be released to incorporate the lessons learned from
    the co-design process."""

    tags = ['proxy-app']

    homepage = "http://www.exmatex.org/comd.html"
    url      = "https://github.com/exmatex/CoMD/archive/master.tar.gz"

    version('master', git='https://github.com/exmatex/CoMD.git', branch='master')

    variant('mpi', default=True, description='Build with MPI support')
    variant('openmp', default=False, description='Build with OpenMP support')
    variant('double', default=True, description='Build with double precision instead of single')
    variant('graphs', default=True, description='Enable graph visuals')

    depends_on('mpi', when='+mpi')
    depends_on('graphviz', when='+graphs')

    def edit(self, spec, prefix):
        if '+openmp' in spec:
            work_dir = 'src-openmp'
        else:
            work_dir = 'src-mpi'
        with working_dir(work_dir):
            shutil.copy('Makefile.vanilla', 'Makefile')

    @property
    def build_targets(self):
        targets = []
        cflags = ' -std=c99 '
        optflags = ' -g -O5 '
        clib = ' -lm '
        comd_variant = 'CoMD'
        cc = spack_cc

        if '+openmp' in self.spec:
            targets.append('--directory=src-openmp')
            comd_variant += '-openmp'
            cflags += ' ' + self.compiler.openmp_flag + ' '
            if '~mpi' in self.spec:
                targets.append('CC = {0}'.format('spack_cc'))
        else:
            targets.append('--directory=src-mpi')
            if '~mpi' in self.spec:
                comd_variant += '-serial'
                targets.append('CC = {0}'.format(cc))
        if '+mpi' in self.spec:
            comd_variant += '-mpi'
            targets.append('CC = {0}'.format(self.spec['mpi'].mpicc))
            cflags += '-DDO_MPI'
            targets.append(
                'INCLUDES = {0}'.format(self.spec['mpi'].prefix.include))

        if '+double' in self.spec:
            cflags += ' -DDOUBLE '
        else:
            cflags += ' -DSINGLE '

        targets.append('CoMD_VARIANT = {0}'.format(comd_variant))
        targets.append('CFLAGS = {0}'.format(cflags))
        targets.append('OPTFLAGS = {0}'.format(optflags))
        targets.append('C_LIB = {0}'.format(clib))

        return targets

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install_tree('examples', prefix.examples)
        install_tree('pots', prefix.pots)
        mkdirp(prefix.doc)
        install('README.md', prefix.doc)
        install('LICENSE.md', prefix.doc)