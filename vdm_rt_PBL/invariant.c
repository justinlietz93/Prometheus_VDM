// invariant.c
// Only the primitive bifurcation law — CF000 + A(-1) + CF00 spine
// gcc -O3 -lm vdm_pure_law.c -o vdm_pure && ./vdm_pure

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>

#define MAX_DIM 32
#define BURDEN_EPS 1e-12          // constitutional resolution floor (CF gates)

typedef struct {
    int dim;                      // Cap(A_n)
    double burden;                // Inv (unresolved opposition)
    double void_debt;             // begins exactly at saturation
    double ortho_basis[MAX_DIM][MAX_DIM];  // carrier (CF00 induced geometry)
} ArticulationClass;

bool is_saturated(ArticulationClass *A) {
    return (A->burden > BURDEN_EPS);  // full lawful capacity exhausted while borne
}

void orthogonal_extend(ArticulationClass *A) {
    if (A->dim >= MAX_DIM) return;
    int new_axis = A->dim;
    for (int i = 0; i < A->dim; i++) {
        A->ortho_basis[new_axis][i] = 0.0;   // orthogonal to all prior
    }
    A->ortho_basis[new_axis][new_axis] = 1.0;
    A->dim++;
    A->void_debt = 0.0;  // debt cleared by new hosting
    printf(">>> SATURATION + VOID DEBT → FORCED NEW ORTHOGONAL AXIS %d | dim now = %d\n", new_axis, A->dim);
}

double compute_emergent_half_turn(ArticulationClass *A) {
    if (A->dim < 2) return 0.0;
    // Dynamic angle derived from current state (no hardcoded constants)
    double dtheta = A->burden / (A->dim + 1.0);
    double theta = 0.0;
    double x = 1.0, y = 0.0;  // start at one pole on carrier
    while (theta < 100.0) {   // safe convergence guard
        // Small lawful rotation (orthogonal continuation)
        double nx = x * cos(dtheta) - y * sin(dtheta);
        double ny = x * sin(dtheta) + y * cos(dtheta);
        x = nx; y = ny;
        theta += dtheta;
        if (x <= -1.0 + BURDEN_EPS) break;  // reached opposite pole without discharge
        dtheta = A->burden / (A->dim + 1.0); // re-derive dynamically
    }
    return theta;
}

int main() {
    ArticulationClass *A = calloc(1, sizeof(ArticulationClass));
    A->dim = 0;
    A->burden = 1.0;          // primitive unresolved two-pole opposition (CF000)
    A->void_debt = 0.0;
    A->ortho_basis[0][0] = 1.0;  // 0D start

    printf("Draft simulator of The Primitive Bifurcation Law running\n");
    printf("Starting 0D unresolved opposition (CF000 derived origin)\n\n");

    for (int step = 0; step < 2000; step++) {
        if (is_saturated(A)) {
            orthogonal_extend(A);
            A->burden = 1.0;  // full inheritance (cumulative stack)
        } else {
            // Same-class lawful continuation (exhaustion)
            A->burden *= 0.999;  // gradual lawful articulation (derived scale)
            if (A->burden < BURDEN_EPS) A->void_debt += (BURDEN_EPS - A->burden);
        }

        // Emergent π witness when carrier admits 2D (CF00 + CF13)
        double pi_emergent = 0.0;
        if (A->dim >= 2) {
            pi_emergent = compute_emergent_half_turn(A);
        }

        if (step % 100 == 0 || A->dim > 5) {
            printf("Step %4d | dim=%2d | burden=%.6f | void_debt=%.6f | emergent_half_turn=%.8f\n",
                   step, A->dim, A->burden, A->void_debt, pi_emergent);
        }

        if (A->dim >= 8) break;  // early stop — law has already forced the spine
    }

    free(A);
    return 0;
}
