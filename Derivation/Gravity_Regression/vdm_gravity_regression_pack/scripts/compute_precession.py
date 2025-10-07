
import argparse, csv, math, os, numpy as np
import matplotlib.pyplot as plt

def load_orbit(path):
    t,x,y = [],[],[]
    with open(path) as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            t.append(float(row['time']))
            x.append(float(row['x']))
            y.append(float(row['y']))
    return np.array(t), np.array(x), np.array(y)

def find_perihelia(t, r):
    # perihelion ~ local minima of r
    idx = []
    for i in range(2, len(r)-2):
        if r[i] < r[i-1] and r[i] < r[i+1] and r[i] < r[i-2] and r[i] < r[i+2]:
            idx.append(i)
    return np.array(idx, dtype=int)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--orbit', required=True, help='CSV with time,x,y')
    ap.add_argument('--out', default='outputs', help='output folder')
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    t,x,y = load_orbit(args.orbit)
    r = np.sqrt(x*x + y*y)
    theta = np.arctan2(y, x)
    theta_unwrap = np.unwrap(theta)

    peri_idx = find_perihelia(t, r)
    if len(peri_idx) < 3:
        print("Not enough perihelia found; need >= 3.")
        return

    # collect per-orbit stats
    rows = []
    peri_angles = theta_unwrap[peri_idx]
    peri_times = t[peri_idx]
    for k in range(1, len(peri_idx)):
        dtheta = peri_angles[k] - peri_angles[k-1]
        period = peri_times[k] - peri_times[k-1]
        rows.append((k, peri_angles[k], dtheta, period))

    # save report
    rep_path = os.path.join(args.out, 'precession_report.csv')
    with open(rep_path, 'w') as f:
        f.write("orbit_index,peri_angle,delta_theta,period\n")
        for rrow in rows:
            f.write(f"{rrow[0]},{rrow[1]},{rrow[2]},{rrow[3]}\n")

    deltas = np.array([r[2] for r in rows])
    median = float(np.median(deltas))
    mean = float(np.mean(deltas))
    std = float(np.std(deltas) + 1e-12)
    cv = float(abs(std/(mean if abs(mean)>1e-12 else 1.0)))
    sign_consistent = np.all(np.sign(deltas[1:]) == np.sign(deltas[:-1]))

    with open(os.path.join(args.out, 'precession_summary.txt'), 'w') as f:
        f.write(f"orbits_analyzed = {len(rows)}\n")
        f.write(f"median_delta_theta = {median}\n")
        f.write(f"mean_delta_theta = {mean}\n")
        f.write(f"std_delta_theta = {std}\n")
        f.write(f"cv_delta_theta = {cv}\n")
        f.write(f"sign_consistent = {sign_consistent}\n")
        f.write("PASS_precession_present = {}\n".format(abs(median) > 1e-6))

    # plot
    plt.figure(figsize=(6,6))
    plt.plot(x, y, linewidth=1)
    plt.scatter(x[peri_idx], y[peri_idx], s=12)
    plt.gca().set_aspect('equal', 'box')
    plt.title('Orbit with Perihelia Marked')
    plt.xlabel('x'); plt.ylabel('y')
    plt.tight_layout()
    plt.savefig(os.path.join(args.out, 'orbit_plot.png'), dpi=160)

if __name__ == '__main__':
    main()
