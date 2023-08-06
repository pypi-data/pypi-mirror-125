from .base import Source
from ..utils.constants import AXIS_X, AXIS_Y, AXIS_Z
from ..utils.linalg import Vec3, axis_to_spherical
import numpy as np
import math

class DipoleSource(Source):
  def __init__(self, frange=None, f=None, pulse_length=None, pulse_offset=None, pos=Vec3(0.0), axis=Vec3(0.0, 0.0, 1.0), phase=0.0):
    super().__init__(pos, frange, f, pulse_length, pulse_offset)
    self.axis = axis
    self.phase = phase

  def _add_lumerical(self, session):
    theta, phi = axis_to_spherical(self.axis)

    dipole = session.fdtd.adddipole(theta=theta, phi=phi, phase=180*self.phase/np.pi)
    self._config_freq_lumerical(dipole)

# Only supports fundamental mode for now
class ModeSource(Source):
  def __init__(self, frange=None, f=None, pulse_length=None, pulse_offset=None, pos=Vec3(0.0), axis=AXIS_X, \
      direction=1, amplitude=1, phase=0, size=Vec3(1e-6)):
    super().__init__(pos, frange, f, pulse_length, pulse_offset)
    self.axis = axis
    self.direction = direction
    self.amplitude = amplitude
    self.phase = phase
    self.size = size

  def _add_lumerical(self, session):
    axis_map = {}
    axis_map[AXIS_X] = 1
    axis_map[AXIS_Y] = 2
    axis_map[AXIS_Z] = 3

    mode = session.fdtd.addmode(injection_axis=axis_map[self.axis], direction=2 if self.direction > 0 else 1, \
      amplitude=self.amplitude, phase=self.phase)
    self._config_freq_lumerical(mode)

    if self.axis == AXIS_X:
      mode.y_span = self.size.y
      mode.z_span = self.size.z
    elif self.axis == AXIS_Y:
      mode.x_span = self.size.x
      mode.z_span = self.size.z
    else:
      mode.x_span = self.size.x
      mode.y_span = self.size.y
  
