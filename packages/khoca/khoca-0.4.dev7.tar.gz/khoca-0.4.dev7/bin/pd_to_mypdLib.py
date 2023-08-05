#!/usr/bin/python3

#
#    pd_to_mypdLib.py --- Part of khoca, a knot homology calculator
#
# Copyright (C) 2018 Lukas Lewark <lukas@lewark.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


def pd_to_mypd(pd):
	result = list()
	for i in pd:
		if (i[3] == ((i[1] + 1) % (2 * len(pd)))):
			result.append([2,i[0] - 1,i[1] - 1,i[2] - 1,i[3] - 1])
		else:
			result.append([3,i[1] - 1,i[2] - 1,i[3] - 1,i[0] - 1])
	return result
