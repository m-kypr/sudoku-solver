from sudoku import Solver
from flask import Flask, request, url_for, render_template, redirect
import json
app = Flask(__name__)


def form_builder(sudoku=None, size=1):
    if not sudoku:
        sudoku = Solver.example
    size = 1
    inp = []
    for i in range(1, 10):
        b = ''
        for j in range(1, 10):
            b += f"<input value=\"{sudoku[i-1][j-1]}\"name=\"{i, j}\" type=\"{i, j}\" maxlength=\"{size}\" size=\"{size}\">"
        inp.append(b)
    return render_template('template.html', grid=f"""
        {"<br>".join(inp)}
    """)


@app.route('/parse', methods=['POST'])
def parse():
    sudoku = [[int(y) for y in x.split(" ") if y]
              for x in request.form['parse'].replace('\r', '').split('\n') if x]
    return redirect(url_for('index', sudoku=json.dumps(sudoku)))


@app.route('/', methods=['GET', 'POST'])
def index(sudoku=None):
    if request.method == 'GET':
        sudoku = request.args.get('sudoku')
        if sudoku:
            sudoku = json.loads(sudoku)
        return form_builder(sudoku=sudoku)
        solver = Solver()
        solve = solver.solve()
        solutions = next(solve)
        htmllines = []
        b1 = [[], [], []]
        for j in range(len(solutions)):
            b = [[], [], []]

            for i in range(len(solutions[j])):
                b[i//solver.n-1].append(str(solutions[j][i]))
            cool = " | ".join([" ".join(s) for s in b])
            b1[j//solver.n-1].append(cool)
        html = "<br>-----------------------<br>".join(
            ["<br>".join(l) for l in b1])
        print(b1)
        return html
    if request.method == 'POST':
        sudoku = []
        for i in range(1, 10):
            b = []
            for j in range(1, 10):
                b.append(int(request.form[f"{i, j}"]))
            sudoku.append(b)
        solver = Solver(sudoku)
        solve = solver.solve()
        try:
            solution = next(solve)
            return form_builder(solution)
        except StopIteration as e:
            return "No solution"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='4000')
