import numpy as np

from abtem.base_classes import Accelerator, HasAcceleratorMixin
from abtem.device import get_array_module
from abtem.utils import tapered_cutoff
from scipy.ndimage import gaussian_filter

class BullseyeAperture(HasAcceleratorMixin):

    def __init__(self, outer_angle, energy=None, inner_angle=0., num_regions=0, num_spokes=0, spoke_width=0., rotation=0.):
        self._outer_angle = outer_angle
        self._inner_angle = inner_angle
        self._num_regions = num_regions
        self._rotation = rotation
        self._num_spokes = num_spokes
        self._spoke_width = spoke_width
        self._accelerator = Accelerator(energy=energy)

    def evaluate(self, alpha, phi):
        xp = get_array_module(alpha)

        aperture = xp.zeros_like(alpha)
        alpha = alpha * 1000
        aa = 2

        if self._num_regions == 1:
            aperture = tapered_cutoff(alpha, self._outer_angle, 1)
        else:
            edges = np.linspace(self._inner_angle, self._outer_angle, self._num_regions + 1)[::-1]

            start_edges = [edge for i, edge in enumerate(edges[::2])]
            end_edges = [edge for i, edge in enumerate(edges[1::2])]

            for start_edge, end_edge in zip(start_edges, end_edges):
                aperture += (1 - tapered_cutoff(alpha, end_edge, 1)) * tapered_cutoff(alpha, start_edge, aa)

        # if self._cross > 0.:
        #     d = np.abs(np.sin(phi - self._rotation) * alpha)
        #     mask = (alpha < self._outer_angle - 2) * (alpha > self._inner_angle + 2)
        #     #aperture -= tapered_cutoff(d, self._cross / 2, aa) #* mask
        #
        #     d = np.abs(np.sin(phi - self._rotation - np.pi / 2) * alpha)
        #     #aperture -= tapered_cutoff(d, self._cross / 2, aa) #* mask
        #
        #     aperture = np.clip(aperture, 0, 1)

            #d = np.abs(np.sin(phi - self._rotation - np.pi / 2) * alpha)
            #aperture[(d < self._cross / 2) * (alpha < self._outer_angle)] = 1.

        return aperture #gaussian_filter(aperture, .8)
