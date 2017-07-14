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


class Pathfinder(MakefilePackage):
    """Proxy Application. Signature search."""

    homepage = "https://mantevo.org/packages/"
    url      = "http://mantevo.org/downloads/releaseTarballs/miniapps/PathFinder/PathFinder_1.0.0.tgz"

    tags = ['proxy-app']

    version('1.0.0', '374269e8d42c305eda3e392444e22dde')

    build_targets = ['--directory=PathFinder_ref', 'CC=cc']

    def edit(self, spec, prefix):
        makefile = FileFilter('PathFinder_ref/Makefile')
        makefile.filter('-fopenmp', self.compiler.openmp_flag)

    def install(self, spec, prefix):
        # Manual installation
        mkdirp(prefix.bin)
        mkdirp(prefix.doc)

        install('PathFinder_ref/PathFinder.x', prefix.bin)
        install('PathFinder_ref/MicroTestData.adj_list', prefix.bin)
        install('README', prefix.doc)

        install_tree('generatedData/', prefix.doc.generatedData)
        install_tree('scaleData/', prefix.doc.scaleData)
