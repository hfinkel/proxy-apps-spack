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
#     spack install cosp2
#
# You can edit this file again by typing:
#
#     spack edit cosp2
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Cosp2(MakefilePackage):
    """Proxy Application. CoSP2 represents a sparse linear algebra 
    parallel algorithm for calculating the density matrix in electronic 
    tructure theory. The algorithm is based on a recursive second-order 
    Fermi-Operator expansion method (SP2) and is tailored for density 
    functional based tight-binding calculations of non-metallic systems 
    
    tags : proxy-add ecp-proxy-app """

    tags = ['proxy-app','ecp-proxy-app']

    homepage = "http://www.exmatex.org/cosp2.html"
    url      = "https://github.com/exmatex/CoSP2/archive/master.tar.gz"

    # FIXME: Add proper versions and checksums here.
    # version('1.2.3', '0123456789abcdef0123456789abcdef')
    version('master',git='https://github.com/exmatex/CoSP2.git',description='master')
    variant('serial',default=True,description='Serial Build ')
    variant('parallel',default=True,description='Serial Build ')
    # FIXME: Add dependencies if required.
    # depends_on('foo')

    def edit(self, spec, prefix):
        pass
        # FIXME: Edit the Makefile if necessary
        # FIXME: If not needed delete this function
        # makefile = FileFilter('Makefile')
        # makefile.filter('CC = .*', 'CC = cc')

    def install(self, spec, prefix):
        pass