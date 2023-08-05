#!/usr/bin/python3

#
#    pd_to_mypd.py --- Part of khoca, a knot homology calculator
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


import sys, re
sys.path.append('.')
import pd_to_mypdLib

if len(sys.argv) != 2:
	print("Expecting one argument.")
	sys.exit()
if sys.argv[1] == "-":
	x = sys.stdin.read()
else:
	x = sys.argv[1]
y = [int(j) for j in re.findall("[0-9]+", x)]
mypd = [list(j) for j in zip(*[iter(y)]*4)]
print(str(pd_to_mypdLib.pd_to_mypd(mypd)).replace(" ",""))
