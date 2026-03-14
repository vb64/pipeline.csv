import os
from flask import Flask, render_template, request, url_for, redirect, g

from pipeline_csv.integrity.material import PipeMaterial as Material
from pipeline_csv.csvfile import Stream
from pipeline_csv.csvfile.row import Depth
from pipeline_csv.csvfile.tubes import Tube
from pipeline_csv import DefektSide
from pipeline_csv.orientation import Orientation
from pipeline_csv.oegiv import TypeDefekt, Row as BaseRow
from pipeline_csv.integrity.method.asme.b31g_1991 import Context, State
from pipeline_csv.integrity.i18n import Lang
from i18n import activate


class Row(BaseRow):
    """Row with mm depth."""

    depth_units = Depth.HundredthsOfMillimeter


pipe = Tube(Row.as_weld(10), Stream(diameter=1420), None)
pipe.length = 11200
pipe.thick_mm = 16
pipe.add_object(
  Row.as_defekt(
    1000,  # дефект начинается на расстоянии 1 метра от начала трубы
    TypeDefekt.CORROZ,
    DefektSide.INSIDE,
    100,  # длина дефекта 100 мм
    10,  # ширина дефекта 10 мм
    str(1 * 100),  # глубина дефекта 1 мм
    # по окружности трубы дефект начинается на 10 угловых минут от верхней точки трубы
    Orientation.from_minutes(10),
    # размер дефекта по окружности составляет 20 угловых минут
    Orientation.from_minutes(10 + 20),
    None,  # MPoint orient
    None,  # MPoint dist
    ''  # comment
  )
)

model = Context(
  pipe.defects[-1],
  Material("Steel", 295),
  7
)

app = Flask(__name__)
lang_code = os.getenv('LANG_CODE')
activate(app, lang_code)

lang = True
if lang_code in [Lang.Ru]:
    lang = model.lang(lang_code)


@app.route('/')
def main():
    g.asme_url = url_for('asme')
    return render_template('main.html', g=g)


@app.route('/asme/', methods=['GET', 'POST'])
def asme():
    g.asme_url = url_for('asme')
    if request.method == 'POST':
        save_form(model, request.form)
        return redirect(g.asme_url)

    state = model.pipe_state(is_explain=lang)

    g.result = _("No danger.")
    if state == State.Replace:
        g.result = _("Replacement of the pipe is necessary.")
    elif state == State.Repair:
        g.result = _("Repair or pressure reduction to {} required.").format(round(model.safe_pressure, 2))

    g.explain = model.explain().replace('\n', '<br>')
    g.asme = model

    return render_template('asme.html', g=g)

def save_form(model, form):
    pipe = model.anomaly.pipe
    pipe.diameter = float(form['diameter'])
    pipe.thick_mm = float(form['wall'])
    model.material.smys = float(form['smys'])
    model.maop = float(form['pressure'])

    model.anomaly.length = float(form['length'])
    model.anomaly.depth_mm = float(form['depth'])
