import numpy as np
from rich.progress import track

from pathlib import Path


class hardLabel:
    def __init__(self,
                 threshold: float = 90.0,
                 ):
        ## PREAMBLE
        # threshold == 90 -> detect highest 10% energy
        self.threshold = threshold
        # energy calc frame in unit of sample
        self.frame_size = 10

    def _calculate_energy(self,
                          signal: np.ndarray,
                          ) -> np.ndarray:
        return np.array([np.sum(signal[i:i+self.frame_size]**2) for i in range(0, len(signal), self.frame_size)])

    def _detect_events(self,
                       energy: np.ndarray,
                       energy_thres: np.ndarray,
                       ) -> list:
        start_indices = []
        end_indices = []
        inside_event = False

        for i, e in enumerate(energy):
            if e > energy_thres and not inside_event:
                start_indices.append(i)
                inside_event = True
            elif e < energy_thres and inside_event:
                end_indices.append(i)
                inside_event = False

        if inside_event:
            end_indices.append(len(energy))

        return list(zip(start_indices, end_indices))

    def _smooth_signal(self,
                       signal: np.ndarray,
                       window_size: int = 5,
                       ) -> np.ndarray:
        return np.convolve(signal, np.ones(window_size) / window_size, mode="valid")

    def _merge_close_intervals(self,
                               intervals,
                               min_gap: float = 0.1,
                               sr: int = 16000,
                               ) -> list:
        merged = []
        for start, end in sorted(intervals):
            if merged and start - merged[-1][1] < int(sr * min_gap):
                merged[-1] = (merged[-1][0], end)
            else:
                merged.append((start, end))

        return merged

    def label_it(self,
                 audio: np.ndarray,
                 sr: int = 16000,
                 ) -> list:
        energy = self._calculate_energy(signal=audio,
                                        )
        energy_thres = np.percentile(energy, self.threshold)

        gunshot_events = self._detect_events(energy=energy,
                                             energy_thres=energy_thres,
                                             )
        merged_gunshot_events = self._merge_close_intervals(intervals=gunshot_events,
                                                            sr=sr,
                                                            )

        hard_labels = []
        for start_idx, end_idx in track(merged_gunshot_events, description="Labeling..."):
            hard_labels.append((start_idx, end_idx))

        return hard_labels
