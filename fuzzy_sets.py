
def display_set(universe, membership):
    result = "{ "
    for i in range(len(universe)):
        result += f"{membership[i]:.2f}/{universe[i]}"
        if i != len(universe)-1:
            result += " + "
    result += " }"
    return result


n = int(input("Enter number of elements: "))

universe = []
A = []
B = []

print("\nEnter Universe Elements:")
for i in range(n):
    universe.append(input(f"Element {i+1}: "))

print("\nEnter Membership Values of Set A (0 to 1)")
for i in range(n):
    while True:
        x = float(input(f"μA({universe[i]}) = "))
        if 0 <= x <= 1:
            A.append(x)
            break
        else:
            print("Membership value must be between 0 and 1.")

print("\nEnter Membership Values of Set B (0 to 1)")
for i in range(n):
    while True:
        x = float(input(f"μB({universe[i]}) = "))
        if 0 <= x <= 1:
            B.append(x)
            break
        else:
            print("Membership value must be between 0 and 1.")


print("\n--------------------------------------")
print("Fuzzy Set A =", display_set(universe, A))
print("Fuzzy Set B =", display_set(universe, B))
print("--------------------------------------")


A_comp = []
B_comp = []

for i in range(n):
    A_comp.append(round(1 - A[i], 2))
    B_comp.append(round(1 - B[i], 2))

union = []

for i in range(n):
    union.append(round(max(A[i], B[i]), 2))


intersection = []

for i in range(n):
    intersection.append(round(min(A[i], B[i]), 2))


difference = []

for i in range(n):
    difference.append(round(min(A[i], B_comp[i]), 2))



alg_sum = []

for i in range(n):
    value = A[i] + B[i] - (A[i] * B[i])
    alg_sum.append(round(value, 2))



alg_product = []

for i in range(n):
    alg_product.append(round(A[i] * B[i], 2))



bounded_sum = []

for i in range(n):
    bounded_sum.append(round(min(1, A[i] + B[i]), 2))



bounded_difference = []

for i in range(n):
    bounded_difference.append(round(max(0, A[i] - B[i]), 2))



print("\n========== RESULTS ==========\n")

print("Union (A ∪ B)")
print(display_set(universe, union))

print("\nIntersection (A ∩ B)")
print(display_set(universe, intersection))

print("\nComplement of A (A')")
print(display_set(universe, A_comp))

print("\nComplement of B (B')")
print(display_set(universe, B_comp))

print("\nDifference (A - B)")
print(display_set(universe, difference))

print("\nAlgebraic Sum")
print(display_set(universe, alg_sum))

print("\nAlgebraic Product")
print(display_set(universe, alg_product))

print("\nBounded Sum")
print(display_set(universe, bounded_sum))

print("\nBounded Difference")
print(display_set(universe, bounded_difference))