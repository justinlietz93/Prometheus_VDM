import numpy as np
from vdm_rt.core.void_dynamics_adapter import TAU, GAMMA
from .frames import SensorFrame

class UTEMux:
    def __init__(self):
        self.adapters = []

    def add_adapter(self, adapter):
        self.adapters.append(adapter)

    def poll_frames(self, tick: int):
        dt_physical = float(np.sqrt(TAU / GAMMA))
        timestamp_us = int(tick * dt_physical * 1_000_000)
        frames = []
        for ad in self.adapters:
            payload = ad.poll() if hasattr(ad, 'poll') else {}
            frames.append(SensorFrame(tick=tick, port=getattr(ad, 'name', 'unknown'), payload=payload, timestamp_us=timestamp_us))
        return frames
