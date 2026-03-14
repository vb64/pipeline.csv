# https://flask.palletsprojects.com/en/2.2.x/blueprints/
from flask import Blueprint, render_template, request, url_for, redirect, session, g
from google.cloud import ndb
from google.protobuf.message import DecodeError

from pipeline_csv.integrity.material import PipeMaterial as Material
from pipeline_csv.csvfile import Stream
from pipeline_csv.csvfile.row import Depth
from pipeline_csv.csvfile.tubes import Tube
from pipeline_csv import DefektSide
from pipeline_csv.orientation import Orientation
from pipeline_csv.oegiv import TypeDefekt, Row as BaseRow
from pipeline_csv.integrity.method.asme.b31g_1991 import Context as Context_1991, State as State_1991
from pipeline_csv.integrity.method.asme.b31g_2012 import Context as Context_2012

from i18n import LANG_CODE

asme_page = Blueprint('asme_page', __name__)


class Row(BaseRow):
    """Row with mm depth."""

    depth_units = Depth.HundredthsOfMillimeter


class AsmeEdition:
    Ed_1991 = "1991"
    Ed_2012 = "2012"


class AsmeB31G(ndb.Model):
    last_used = ndb.DateTimeProperty(indexed=True, auto_now=True)
    diameter = ndb.FloatProperty(indexed=False, default=1420.0)
    wallthickness = ndb.FloatProperty(indexed=False, default=16.0)
    smys = ndb.FloatProperty(indexed=False, default=295.0)
    smts = ndb.FloatProperty(indexed=False, default=340.0)
    maop = ndb.FloatProperty(indexed=False, default=7.0)
    length = ndb.FloatProperty(indexed=False, default=100.0)
    depth = ndb.FloatProperty(indexed=False, default=1.0)
    is_modified = ndb.BooleanProperty(indexed=False, default=False)
    corrosion_rate = ndb.FloatProperty(indexed=False, default=0.4)


@asme_page.route('/asme/<edition>/', methods=['GET', 'POST'])
def show(edition):
    if 'session_id' in session:
        try:
            asme = ndb.Key(urlsafe=session['session_id']).get()
        except DecodeError:
            asme = None
        if not asme:
            asme = AsmeB31G()
            session['session_id'] = asme.put().urlsafe()
    else:
        asme = AsmeB31G()
        session['session_id'] = asme.put().urlsafe()

    g.edition = edition
    g.asme_url = url_for('asme_page.show', edition=edition)
    if request.method == 'POST':
        save_form(asme, request.form, edition)
        return redirect(g.asme_url)

    model = get_model(asme, edition)
    if edition == AsmeEdition.Ed_2012:
        calck_2012(asme, model)
    else:
        calck_1991(model)

    g.explain = model.explain().replace('\n', '<br>')
    g.asme = model

    return render_template('asme.html', g=g)


def get_model(asme, edition):
    """Return asme Context for calculation."""
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

    cls = Context_1991
    if edition == AsmeEdition.Ed_2012:
        cls = Context_2012

    model = cls(
      pipe.defects[-1],
      Material("Steel", 295, smts=340),
      7
    )

    pipe = model.anomaly.pipe
    pipe.diameter = asme.diameter
    pipe.thick_mm = asme.wallthickness

    model.maop = asme.maop
    model.material.smys = asme.smys

    model.anomaly.length = asme.length
    model.anomaly.depth_mm = asme.depth

    if edition == AsmeEdition.Ed_2012:
        model.material.smts = asme.smts
        model.corrosion_rate = asme.corrosion_rate

    return model


def calck_2012(asme, model):
    """Calculate asme 2012 result."""
    model.is_explain = model.lang(LANG_CODE)
    years = model.years(is_mod=asme.is_modified)

    if years == 0:
        g.result = _("Repair or pressure reduction to {} required.").format(round(model.safe_pressure, 2))
    elif years > 100:
        g.result = _("Repair not required.")
    else:
        g.result = _("Repair required after years: {}.").format(int(round(years)))

    g.is_modified = asme.is_modified


def calck_1991(model):
    """Calculate asme 1991 result."""
    state = model.pipe_state(is_explain=model.lang(LANG_CODE))

    g.result = _("Repair not required.")
    if state == State_1991.Replace:
        g.result = _("Replacement of the pipe is necessary.")
    elif state == State_1991.Repair:
        g.result = _("Repair or pressure reduction to {} required.").format(round(model.safe_pressure, 2))


def save_form(asme, form, edition):
    """Save asme session data to db."""
    asme.diameter = float(form['diameter'])
    asme.wallthickness = float(form['wall'])
    asme.smys = float(form['smys'])
    asme.maop = float(form['pressure'])
    asme.length = float(form['length'])
    asme.depth = float(form['depth'])

    if edition == AsmeEdition.Ed_2012:
        asme.smts = float(form['smts'])
        asme.corrosion_rate = float(form['corate'])
        asme.is_modified = True if 'modified' in form else False

    return asme.put()
