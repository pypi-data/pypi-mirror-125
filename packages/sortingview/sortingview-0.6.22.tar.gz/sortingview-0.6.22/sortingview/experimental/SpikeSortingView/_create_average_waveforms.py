from typing import List, Tuple, Union
import numpy as np
from .helpers.compute_correlogram_data import compute_correlogram_data
from .Figure import Figure


def create_average_waveforms(self, *, unit_ids: List[int], label: Union[str, None]=None):
    from .SpikeSortingView import SpikeSortingView
    assert isinstance(self, SpikeSortingView)

    if label is None:
        label = 'Average waveforms'

    traces_sample = self.get_traces_sample(segment=0)
    noise_level = estimate_noise_level(traces_sample)
    plots = []
    for unit_id in unit_ids:
        snippets = self.get_unit_subsampled_spike_snippets(unit_id=unit_id)
        waveform = np.mean(snippets, axis=0).astype(np.float32)
        channel_ids = self.get_unit_channel_neighborhood(unit_id=unit_id)
        plots.append({
            'unitId': unit_id,
            'channelIds': channel_ids,
            'waveform': waveform.T
        })
    
    data = {
        'type': 'AverageWaveforms',
        'averageWaveforms': plots,
        'samplingFrequency': self.sampling_frequency,
        'noiseLevel': float(noise_level)
    }
    return Figure(data=data, label=label)

def estimate_noise_level(traces: np.ndarray):
    est_noise_level = np.median(np.abs(traces.ravel())) / 0.6745  # median absolute deviation (MAD) estimate of stdev
    return est_noise_level