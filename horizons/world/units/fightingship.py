# ###################################################
# Copyright (C) 2011 The Unknown Horizons Team
# team@unknown-horizons.org
# This file is part of Unknown Horizons.
#
# Unknown Horizons is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# ###################################################

from horizons.gui.tabs import ShipInventoryTab, ShipOverviewTab, \
	EnemyShipOverviewTab, FightingUnitTab
from horizons.constants import WEAPONS, GAME_SPEED
from horizons.world.units.weaponholder import MovingWeaponHolder
from horizons.world.units.ship import Ship

class FightingShip(MovingWeaponHolder, Ship):
	"""Class representing a fighting ship ship
	@param x: int x position
	@param y: int y position
	"""
	tabs = (ShipOverviewTab, ShipInventoryTab, FightingUnitTab)
	enemy_tabs = (EnemyShipOverviewTab, FightingUnitTab)

	def __init__(self, x, y, **kwargs):
		super(FightingShip, self).__init__(x=x, y=y, **kwargs)
		#NOTE dummy cannon
		self.add_weapon_to_storage(WEAPONS.CANNON)
		self.add_weapon_to_storage(WEAPONS.CANNON)
		self.add_weapon_to_storage(WEAPONS.CANNON)
		self.add_weapon_to_storage(WEAPONS.CANNON)
		self.add_weapon_to_storage(WEAPONS.CANNON)
		self.add_weapon_to_storage(WEAPONS.CANNON)

	def go(self, x, y):
		super(FightingShip, self).go(x, y)
		self.stop_attack()

	def fire_all_weapons(self, dest, rotate = True):
		"""
		Rotate ship so it is perpendicular on dest
		"""
		super(FightingShip, self).fire_all_weapons(dest, rotate)

		if not self._fireable:
			return

		if not self._min_range <= self.position.distance(dest) <= self._max_range:
			return

		# rotate the ship so it faces dest
		# for this rotate facing location coordinates around position coordinates
		self.stop_for(GAME_SPEED.TICKS_PER_SECOND * 1)
		self_location = self._instance.getLocation()
		facing_location = self._instance.getFacingLocation()

		# ship coords
		x1 = self_location.getMapCoordinates().x
		y1 = self_location.getMapCoordinates().y
		# target coords
		x2 = dest.x
		y2 = dest.y
		# facing coords
		x3 = facing_location.getMapCoordinates().x
		y3 = facing_location.getMapCoordinates().y
		facing_coords = facing_location.getMapCoordinates()
		# calculate the side of the ship - target line facing location is on
		# side > 0 left, side <= 0 right
		side = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
		# calculate x4 y4 the new facing location coords
		# they are calculated by rotating 90' the target location
		if side > 0:
			x4 = y1 - y2 + x1
			y4 = x2 - x1 + y1
			direction = 'left'
		else:
			x4 = y2 - y1 + x1
			y4 = x1 - x2 + y1
			direction = 'right'

		facing_coords.x = x4
		facing_coords.y = y4

		facing_location.setMapCoordinates(facing_coords)
		self._instance.setFacingLocation(facing_location)
		self.act('attack_%s' % direction, facing_location, repeating=False)
		self._action = 'idle'

