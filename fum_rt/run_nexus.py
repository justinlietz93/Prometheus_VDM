
from .nexus import Nexus, make_parser
import time, os

def main():
    ts = time.strftime('%Y%m%d_%H%M%S')
    run_dir = os.path.join('runs', ts)
    args = make_parser().parse_args()
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
               # Engram loader (forward CLI flag into Nexus)
               load_engram_path=getattr(args, 'load_engram', None))
    nx.run(duration_s=args.duration)

if __name__ == '__main__':
    main()
