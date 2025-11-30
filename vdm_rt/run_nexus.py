"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

from .nexus import Nexus, make_parser
import time, os

def main():
    ts = time.strftime('%Y%m%d_%H%M%S')
    default_run_dir = os.path.join('runs', ts)
    args = make_parser().parse_args()

    # Resolve load_engram to an actual checkpoint file and adopt its folder as run_dir when --run-dir is omitted.
    load_path = getattr(args, 'load_engram', None)

    def _resolve_latest_ckpt_in_dir(d: str):
        try:
            best = None
            best_step = -1
            best_ext = ""
            for fn in os.listdir(d):
                if not fn.startswith("state_"):
                    continue
                if not (fn.endswith(".h5") or fn.endswith(".npz")):
                    continue
                ext = ".h5" if fn.endswith(".h5") else ".npz"
                step_str = fn[6:-len(ext)] if len(ext) > 0 else fn[6:]
                try:
                    s = int(step_str)
                    # Prefer higher step; on tie prefer .h5
                    if (s > best_step) or (s == best_step and ext == ".h5" and best_ext == ".npz"):
                        best = fn
                        best_step = s
                        best_ext = ext
                except Exception:
                    continue
            return os.path.join(d, best) if best else None
        except Exception:
            return None

    # Normalize load_path (allow directory to mean "latest checkpoint in that dir")
    if load_path:
        p = str(load_path)
        if os.path.isdir(p):
            resolved = _resolve_latest_ckpt_in_dir(p)
            load_path = resolved if resolved else None
        else:
            load_path = p

    # Adopt bundle folder for run_dir if not explicitly set
    run_dir = getattr(args, 'run_dir', None)
    if not run_dir:
        if load_path and os.path.exists(load_path):
            # If a file path, adopt its parent; if previously a dir, we already kept it above
            run_dir = os.path.dirname(load_path)
        else:
            run_dir = default_run_dir

    nx = Nexus(run_dir=run_dir,
               N=args.neurons, k=args.k, hz=args.hz, domain=args.domain,
               use_time_dynamics=args.use_time_dynamics,
               viz_every=args.viz_every, log_every=args.log_every,
               checkpoint_every=args.checkpoint_every, seed=args.seed,
               sparse_mode=(args.sparse_mode if args.sparse_mode is not None else (args.neurons >= 20000)),
               threshold=getattr(args, 'threshold', 0.15),
               lambda_omega=getattr(args, 'lambda_omega', 0.1),
               candidates=getattr(args, 'candidates', 64),
               walkers=getattr(args, 'walkers', 256),
               hops=getattr(args, 'hops', 3),
               status_interval=getattr(args, 'status_interval', 1),
               bundle_size=getattr(args, 'bundle_size', 3),
               prune_factor=getattr(args, 'prune_factor', 0.10),
               # Checkpoint retention / format (format optional)
               checkpoint_format=getattr(args, 'checkpoint_format', 'h5') if hasattr(args, 'checkpoint_format') else 'h5',
               checkpoint_keep=getattr(args, 'checkpoint_keep', 5),
               # Text→connectome stimulation (symbol→group)
               stim_group_size=getattr(args, 'stim_group_size', 4),
               stim_amp=getattr(args, 'stim_amp', 0.05),
               stim_decay=getattr(args, 'stim_decay', 0.90),
               stim_max_symbols=getattr(args, 'stim_max_symbols', 64),
               # Self-speak / topology spike detection
               speak_auto=getattr(args, 'speak_auto', True),
               speak_z=getattr(args, 'speak_z', 1.0),
               speak_hysteresis=getattr(args, 'speak_hysteresis', 1.0),
               speak_cooldown_ticks=getattr(args, 'speak_cooldown_ticks', 10),
               speak_valence_thresh=getattr(args, 'speak_valence_thresh', 0.01),
               b1_half_life_ticks=getattr(args, 'b1_half_life_ticks', 50),
               # Engram loader (forward normalized path into Nexus)
               load_engram_path=load_path,
               # Optional embedded control server (default off)
               start_control_server=getattr(args, 'control_server', False))
    nx.run(duration_s=args.duration)

if __name__ == '__main__':
    main()
