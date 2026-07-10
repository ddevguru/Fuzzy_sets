"""
Core fuzzy-set math. This module is 100% deterministic Python (no LLM involved)
so every number the agent speaks is guaranteed correct - the LLM is only ever
used to *narrate* these facts, never to compute them.
"""

def format_set(universe, membership):
    parts = [f"{membership[i]:.2f}/{universe[i]}" for i in range(len(universe))]
    return "{ " + " + ".join(parts) + " }"


FORMULAS = {
    "union": {
        "name": "Union (A ∪ B)",
        "formula": "μA∪B(x) = max(μA(x), μB(x))",
        "explanation": "The union of two fuzzy sets takes, for every element, the "
                       "LARGER of the two membership values. It represents "
                       "'belongs to A OR B' as strongly as possible.",
    },
    "intersection": {
        "name": "Intersection (A ∩ B)",
        "formula": "μA∩B(x) = min(μA(x), μB(x))",
        "explanation": "The intersection takes the SMALLER of the two membership "
                       "values for every element. It represents 'belongs to A AND B' "
                       "- you can only be as strongly in both sets as the weaker "
                       "membership allows.",
    },
    "complement_a": {
        "name": "Complement of A (A')",
        "formula": "μA'(x) = 1 - μA(x)",
        "explanation": "The complement flips membership: the more strongly x "
                       "belongs to A, the less it belongs to A', and vice versa.",
    },
    "complement_b": {
        "name": "Complement of B (B')",
        "formula": "μB'(x) = 1 - μB(x)",
        "explanation": "Same idea as the complement of A, applied to Set B.",
    },
    "difference": {
        "name": "Difference (A - B)",
        "formula": "μA-B(x) = min(μA(x), μB'(x)) = min(μA(x), 1 - μB(x))",
        "explanation": "A - B represents elements that belong to A but NOT to B. "
                       "It's computed as the intersection of A with the complement "
                       "of B.",
    },
    "algebraic_sum": {
        "name": "Algebraic Sum",
        "formula": "μA(x) + μB(x) - μA(x)·μB(x)",
        "explanation": "A probabilistic-style OR: it adds both memberships but "
                       "subtracts their product, so the result never exceeds 1.",
    },
    "algebraic_product": {
        "name": "Algebraic Product",
        "formula": "μA(x) · μB(x)",
        "explanation": "A probabilistic-style AND: multiplying the two memberships, "
                       "so the result is only high when BOTH memberships are high.",
    },
    "bounded_sum": {
        "name": "Bounded Sum",
        "formula": "min(1, μA(x) + μB(x))",
        "explanation": "Adds the two memberships together, capping the result at 1 "
                       "so it stays a valid membership value.",
    },
    "bounded_difference": {
        "name": "Bounded Difference",
        "formula": "max(0, μA(x) - μB(x))",
        "explanation": "Subtracts B's membership from A's, never letting the result "
                       "drop below 0.",
    },
}

OPERATIONS_ORDER = [
    "union", "intersection", "complement_a", "complement_b", "difference",
    "algebraic_sum", "algebraic_product", "bounded_sum", "bounded_difference",
]


def compute_all(universe, A, B):
    n = len(universe)
    A_comp = [round(1 - A[i], 2) for i in range(n)]
    B_comp = [round(1 - B[i], 2) for i in range(n)]
    union = [round(max(A[i], B[i]), 2) for i in range(n)]
    intersection = [round(min(A[i], B[i]), 2) for i in range(n)]
    difference = [round(min(A[i], B_comp[i]), 2) for i in range(n)]
    alg_sum = [round(A[i] + B[i] - (A[i] * B[i]), 2) for i in range(n)]
    alg_product = [round(A[i] * B[i], 2) for i in range(n)]
    bounded_sum = [round(min(1, A[i] + B[i]), 2) for i in range(n)]
    bounded_difference = [round(max(0, A[i] - B[i]), 2) for i in range(n)]
    return {
        "complement_a": A_comp,
        "complement_b": B_comp,
        "union": union,
        "intersection": intersection,
        "difference": difference,
        "algebraic_sum": alg_sum,
        "algebraic_product": alg_product,
        "bounded_sum": bounded_sum,
        "bounded_difference": bounded_difference,
    }


def steps_for(op, universe, A, B, A_comp, B_comp, result):
    """Build a human-readable, per-element calculation line for one operation."""
    n = len(universe)
    lines = []
    for i in range(n):
        x = universe[i]
        a, b = A[i], B[i]
        if op == "union":
            lines.append(f"μ({x}) = max({a:.2f}, {b:.2f}) = {result[i]:.2f}")
        elif op == "intersection":
            lines.append(f"μ({x}) = min({a:.2f}, {b:.2f}) = {result[i]:.2f}")
        elif op == "complement_a":
            lines.append(f"μ({x}) = 1 - {a:.2f} = {result[i]:.2f}")
        elif op == "complement_b":
            lines.append(f"μ({x}) = 1 - {b:.2f} = {result[i]:.2f}")
        elif op == "difference":
            bc = B_comp[i]
            lines.append(f"μ({x}) = min({a:.2f}, {bc:.2f}) = {result[i]:.2f}")
        elif op == "algebraic_sum":
            lines.append(f"μ({x}) = {a:.2f} + {b:.2f} - ({a:.2f}×{b:.2f}) = {result[i]:.2f}")
        elif op == "algebraic_product":
            lines.append(f"μ({x}) = {a:.2f} × {b:.2f} = {result[i]:.2f}")
        elif op == "bounded_sum":
            lines.append(f"μ({x}) = min(1, {a:.2f}+{b:.2f}) = {result[i]:.2f}")
        elif op == "bounded_difference":
            lines.append(f"μ({x}) = max(0, {a:.2f}-{b:.2f}) = {result[i]:.2f}")
    return lines
