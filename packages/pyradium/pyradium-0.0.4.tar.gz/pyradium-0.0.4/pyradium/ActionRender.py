#	pyradium - HTML presentation/slide show generator
#	Copyright (C) 2015-2021 Johannes Bauer
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
import sys
import time
import subprocess
import logging
from .BaseAction import BaseAction
from .Presentation import Presentation
from .RenderingParameters import RenderingParameters
from .Renderer import Renderer
from .Exceptions import CallingProcessException, PyRadiumException

_log = logging.getLogger(__spec__.name)

class ActionRender(BaseAction):
	def _wait_for_change(self, renderer):
		cmd = [ "inotifywait" ]
		cmd += [ "-q", "-r" ]
		cmd += [ "--exclude", r"\..*\.sw[a-z]" ]
		cmd += [ "-e", "modify", "-e", "close_write", "-e", "create" ]

		sources = [ ]
		sources += renderer.presentation.sources
		sources += renderer.rendering_params.template_dirs
		sources += renderer.rendering_params.include_dirs
		sources += self._args.re_render_watch
		sources = [ source for source in sources if os.path.exists(source) ]
		cmd += sources
		proc = subprocess.run(cmd)
		if proc.returncode not in [ 0, 1 ]:
			raise CallingProcessException("inotifywait returned with returncode %d." % (proc.returncode))

	def run(self):
		if (not self._args.force) and os.path.exists(self._args.outdir):
			print("Refusing to overwrite: %s" % (self._args.outdir), file = sys.stderr)
			return 1

		renderer = None
		render_success = True
		while True:
			try:
				t0 = time.time()
				rendering_parameters = RenderingParameters(
						template_style = self._args.template_style,
						honor_pauses = not self._args.remove_pauses,
						collapse_animation = self._args.collapse_animation,
						presentation_mode = self._args.presentation_mode,
						extra_template_dirs = self._args.template_dir,
						include_dirs = [ os.path.dirname(self._args.infile) or "." ] + self._args.include_dir,
						index_filename = self._args.index_filename,
						geometry = self._args.geometry,
						image_max_dimension = self._args.image_max_dimension,
						presentation_features = self._args.presentation_feature)
				presentation = Presentation.load_from_file(self._args.infile, rendering_parameters)
				renderer = Renderer(presentation, rendering_parameters)
				rendered_presentation = renderer.render(deploy_directory = self._args.outdir)
				t1 = time.time()
				_log.info("Successfully rendered presentation into directory \"%s\", took %.1f seconds", self._args.outdir, t1 - t0)
			except PyRadiumException as e:
				render_success = False
				_log.error("Rendering failed: [%s] %s" % (e.__class__.__name__, str(e)))
			if not self._args.re_render_loop:
				break
			if renderer is None:
				sleep_duration_secs = 5
				_log.warning("Unable to watch files for change since parsing the source was impossible; sleeping for %d seconds instead." % (sleep_duration_secs))
				time.sleep(sleep_duration_secs)
			else:
				self._wait_for_change(renderer)
		return 0 if render_success else 1
