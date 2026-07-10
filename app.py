from flask import Flask, render_template, request

app = Flask(__name__)


def r(x):
    """Round to 4 decimals, then trim trailing zeros for clean display."""
    val = round(x + 1e-12, 4)
    if val == int(val):
        return int(val)
    return val


def fmt_set(vals, universe):
    return " + ".join([f"{vals[i]}/{universe[i]}" for i in range(len(universe))])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    n = int(request.form.get('n'))
    universe, A, B = [], [], []

    for i in range(n):
        universe.append(request.form.get(f'element_{i}', '').strip() or str(i + 1))
        a_val = float(request.form.get(f'a_{i}'))
        b_val = float(request.form.get(f'b_{i}'))
        a_val = min(max(a_val, 0), 1)
        b_val = min(max(b_val, 0), 1)
        A.append(a_val)
        B.append(b_val)

    rows = []
    A_comp, B_comp = [], []
    union, intersection, difference = [], [], []
    alg_sum, alg_product, bounded_sum, bounded_diff = [], [], [], []

    for i in range(n):
        x, a, b = universe[i], A[i], B[i]

        ac = r(1 - a)
        bc = r(1 - b)
        u = r(max(a, b))
        it = r(min(a, b))
        diff = r(min(a, bc))
        asum = r(a + b - a * b)
        aprod = r(a * b)
        bsum = r(min(1, a + b))
        bdiff = r(max(0, a - b))

        A_comp.append(ac); B_comp.append(bc)
        union.append(u); intersection.append(it); difference.append(diff)
        alg_sum.append(asum); alg_product.append(aprod)
        bounded_sum.append(bsum); bounded_diff.append(bdiff)

        rows.append({
            'x': x, 'a': a, 'b': b,
            'ac': ac, 'bc': bc,
            'ac_calc': f"1 &minus; {a} = {ac}",
            'bc_calc': f"1 &minus; {b} = {bc}",
            'union': u,
            'union_calc': f"max({a}, {b}) = {u}",
            'inter': it,
            'inter_calc': f"min({a}, {b}) = {it}",
            'diff': diff,
            'diff_calc': f"min({a}, 1&minus;{b}) = min({a}, {bc}) = {diff}",
            'asum': asum,
            'asum_calc': f"{a} + {b} &minus; ({a} &times; {b}) = {r(a+b)} &minus; {r(a*b)} = {asum}",
            'aprod': aprod,
            'aprod_calc': f"{a} &times; {b} = {aprod}",
            'bsum': bsum,
            'bsum_calc': f"min(1, {a} + {b}) = min(1, {r(a+b)}) = {bsum}",
            'bdiff': bdiff,
            'bdiff_calc': f"max(0, {a} &minus; {b}) = max(0, {r(a-b)}) = {bdiff}",
        })

    result_sets = {
        'A': fmt_set(A, universe),
        'B': fmt_set(B, universe),
        'A_comp': fmt_set(A_comp, universe),
        'B_comp': fmt_set(B_comp, universe),
        'union': fmt_set(union, universe),
        'intersection': fmt_set(intersection, universe),
        'difference': fmt_set(difference, universe),
        'alg_sum': fmt_set(alg_sum, universe),
        'alg_product': fmt_set(alg_product, universe),
        'bounded_sum': fmt_set(bounded_sum, universe),
        'bounded_diff': fmt_set(bounded_diff, universe),
    }

    return render_template('result.html', rows=rows, result_sets=result_sets, n=n)


if __name__ == '__main__':
    app.run(debug=True)