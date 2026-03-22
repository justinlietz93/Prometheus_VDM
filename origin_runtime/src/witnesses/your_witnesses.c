/*
 * your_witnesses.c
 *
 * Placeholder file.
 * Fill these with canon-faithful witness semantics.
 */

#include <stddef.h>

void *InitialInvariant(void) { return NULL; }
void *InitialClass(void) { return NULL; }

void *ArticulateSameClass(void *Inv, void *A_n) { (void)Inv; (void)A_n; return NULL; }
int   IsGenuinelyNew(void *candidate, void *A_n) { (void)candidate; (void)A_n; return 0; }
int   Bear(void *Inv, void *A_n) { (void)Inv; (void)A_n; return 0; }
int   Dis(void *Inv) { (void)Inv; return 0; }
int   Cap_gt_zero(void *A_n) { (void)A_n; return 0; }
int   Cap_eq_zero(void *A_n) { (void)A_n; return 0; }
void *OrthogonalAdmit(void *A_n) { (void)A_n; return NULL; }
void *IntegrateSameClass(void *A_n, void *candidate) { (void)A_n; (void)candidate; return NULL; }
void *Append(void *A_n, void *A_n1_perp) { (void)A_n; (void)A_n1_perp; return NULL; }
