"""Series-parallel system operational availability Monte Carlo coursework demo."""

from __future__ import annotations

import math
import random
import statistics


def analytical_series_parallel_ao(subsystem_availabilities: list[list[float]]) -> float:
    """Compute exact operational availability for independent series-parallel blocks."""
    total_ao = 1.0
    for parallel_group in subsystem_availabilities:
        block_unavailability = 1.0
        for comp_ao in parallel_group:
            block_unavailability *= 1.0 - comp_ao
        total_ao *= 1.0 - block_unavailability
    return total_ao


def simulate_series_parallel_ao(
    subsystem_params: list[list[tuple[float, float]]],
    horizon_hours: float = 10000.0,
    trials: int = 2000,
    seed: int = 20261123,
) -> tuple[float, float, float]:
    """Run Monte Carlo alternating-renewal availability trials using (MTBF, MTTR) pairs."""
    rng = random.Random(seed)
    samples: list[float] = []

    for _ in range(trials):
        # Discretize mission horizon into hourly checks per component via Markov-like availability
        # sampled from exponential up/down cycles for exact steady-state behavior.
        comp_ao_estimates: list[list[float]] = []
        for parallel_group in subsystem_params:
            group_est: list[float] = []
            for mtbf, mttr in parallel_group:
                t = 0.0
                up_time = 0.0
                is_up = True
                while t < horizon_hours:
                    rate = (1.0 / mtbf) if is_up else (1.0 / mttr)
                    dt = rng.expovariate(rate)
                    step = min(dt, horizon_hours - t)
                    if is_up:
                        up_time += step
                    t += step
                    is_up = not is_up
                group_est.append(up_time / horizon_hours)
            comp_ao_estimates.append(group_est)

        sys_ao = analytical_series_parallel_ao(comp_ao_estimates)
        samples.append(sys_ao)

    mean_ao = statistics.mean(samples)
    std_err = statistics.stdev(samples) / math.sqrt(len(samples))
    ci_half = 1.96 * std_err
    return mean_ao, mean_ao - ci_half, mean_ao + ci_half


def main() -> None:
    # 3 subsystems in series: [1 active, 2 redundant], [2 redundant], [1 single-point]
    subsystems = [
        [(480.0, 12.0), (480.0, 12.0)],
        [(600.0, 15.0), (600.0, 15.0)],
        [(1800.0, 6.0)],
    ]
    exact_groups = [[mtbf / (mtbf + mttr) for mtbf, mttr in grp] for grp in subsystems]
    exact_ao = analytical_series_parallel_ao(exact_groups)
    mc_mean, ci_low, ci_high = simulate_series_parallel_ao(subsystems, horizon_hours=5000.0, trials=400)

    print(f"Analytical series-parallel Ao : {exact_ao:.6f}")
    print(f"Monte Carlo mean Ao (400 runs): {mc_mean:.6f} (95% CI: [{ci_low:.6f}, {ci_high:.6f}])")


if __name__ == "__main__":
    main()
