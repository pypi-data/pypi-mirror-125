#	pyradium - HTML presentation/slide show generator
#	Copyright (C) 2021-2021 Johannes Bauer
#
#	This file is part of pyradium.
#
#	pyradium is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	pyradium is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with pyradium; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

import os
from .Enums import PresentationMode
from .FileLookup import FileLookup

class RenderingParameters():
	def __init__(self, template_style = "default", honor_pauses = True, collapse_animation = False, presentation_mode = PresentationMode.Interactive, extra_template_dirs = None, include_dirs = None, index_filename = "index.html", geometry = (1280, 720), image_max_dimension = 1920, presentation_features = None):
		self._template_style = template_style
		self._honor_pauses = honor_pauses
		self._collapse_animation = collapse_animation
		self._presentation_mode = presentation_mode
		template_dirs = [ os.path.expanduser("~/.config/pyradium/templates"), os.path.dirname(os.path.realpath(__file__)) + "/templates" ]
		if extra_template_dirs is not None:
			template_dirs += extra_template_dirs
		self._template_dirs = FileLookup(template_dirs)
		if include_dirs is None:
			self._include_dirs = FileLookup()
		else:
			self._include_dirs = FileLookup(include_dirs)
		self._index_filename = index_filename
		self._geometry = geometry
		self._image_max_dimension = image_max_dimension
		self._presentation_features = set(presentation_features) if (presentation_features is not None) else set()

	@property
	def template_style(self):
		return self._template_style

	@property
	def honor_pauses(self):
		return self._honor_pauses

	@property
	def collapse_animation(self):
		return self._collapse_animation

	@property
	def presentation_mode(self):
		return self._presentation_mode

	@property
	def template_dirs(self):
		return self._template_dirs

	@property
	def include_dirs(self):
		return self._include_dirs

	@property
	def index_filename(self):
		return self._index_filename

	@property
	def geometry_x(self):
		return self._geometry[0]

	@property
	def geometry_y(self):
		return self._geometry[1]

	@property
	def image_max_dimension(self):
		return self._image_max_dimension

	@property
	def presentation_features(self):
		return iter(self._presentation_features)
