from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.utils import secure_filename
import os, sys

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'Homies_Foods'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DEMO_USER = {'username': 'Ncortest', 'password': 'unicolmayor'}


classifier = None
try:
    sys.path.append('/mnt/data')
    import proyecto as proyecto_mod

    if hasattr(proyecto_mod, 'ClasificadorImagenes'):
        clf = proyecto_mod.ClasificadorImagenes()
        def classify(path):
            try:
                return clf.clasificar(path)
            except Exception:
                return None
        classifier = classify
    elif hasattr(proyecto_mod, 'classify_image'):
        classifier = proyecto_mod.classify_image
    elif hasattr(proyecto_mod, 'clasificar'):
        classifier = proyecto_mod.clasificar
    else:

        def classifier(path):
            return None
except Exception:

    classifier = None


def fallback_classifier(path):
    fname = os.path.basename(path).lower()
    keywords = {
        'tomato': ['tomato','tomate','jitomate'],
        'egg': ['egg','huevo'],
        'chicken': ['chicken','pollo'],
        'cheese': ['cheese','queso'],
        'onion': ['onion','cebolla'],
        'garlic': ['garlic','ajo'],
        'banana': ['banana','plátano','platano'],
        'apple': ['apple','manzana'],
        'potato': ['potato','papa','patata'],
        'rice': ['rice','arroz'],
        'beef': ['beef','res','carne'],
        'pepper': ['pepper','pimiento','ají','aji'],
    }
    detected = []
    for label, kws in keywords.items():
        for kw in kws:
            if kw in fname:
                detected.append(label)
                break

    if not detected:
        return ['ingrediente']
    return detected

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


RECIPE_DB = [
    (set(['tomato','cheese','onion']), "Salsa rápida: pica tomate, cebolla y mezcla con queso fresco. Sirve con pan o pasta."),
    (set(['egg','cheese']), "Tortilla sencilla: bate huevos, añade queso y cocina en sartén."),
    (set(['chicken','rice','garlic']), "Arroz con pollo: sofríe ajo, añade pollo, arroz y cocina con caldo."),
    (set(['banana','egg']), "Panqueques rápidos: machaca banana, mezcla con huevo y cocina pequeñas tortitas."),
    (set(['potato','onion','cheese']), "Papas gratinadas: corta papas, intercala con cebolla y queso, hornea."),
    (set(['apple','banana']), "Smoothie de fruta: licúa manzana y banana con leche o agua."),
    (set(['chicken','tomato','onion']), "Pollo guisado: saltea pollo con tomate y cebolla, cocina a fuego lento."),
    (set(['rice','onion','garlic']), "Arroz aromático: sofríe ajo y cebolla, añade arroz y cocina."),
]

def suggest_recipes(detected_ingredients):
    suggestions = []
    detected = set(detected_ingredients)

    scored = []
    for ingr_set, recipe in RECIPE_DB:
        score = len(detected & ingr_set)
        if score > 0:
            scored.append((score, recipe, ingr_set))
    scored.sort(reverse=True, key=lambda x: x[0])
    for score, recipe, ingr_set in scored[:5]:
        suggestions.append({'recipe': recipe, 'matches': list(ingr_set & detected), 'score': score})
    if not suggestions:
        suggestions.append({'recipe': 'No encontré recetas exactas. Sube más imágenes o prueba con ingredientes comunes (tomate, huevo, arroz, pollo).', 'matches': [], 'score': 0})
    return suggestions

@app.route('/')
def index():
    if session.get('logged_in'):
        return redirect(url_for('upload'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        password = request.form.get('password','').strip()
        if username == DEMO_USER['username'] and password == DEMO_USER['password']:
            session['logged_in'] = True
            session['username'] = username
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('upload'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html', title='HoMieS FooDS - Iniciar sesión')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('login'))

@app.route('/upload', methods=['GET','POST'])
def upload():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    detected_total = []
    classified = {}

    if request.method == 'POST':
        files = request.files.getlist('photos')
        saved_files = []
        for f in files:
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                f.save(save_path)
                saved_files.append(filename)


                labels = None
                try:
                    if classifier:
                        labels = classifier(save_path)
                except Exception:
                    labels = None

                if not labels:
                    labels = fallback_classifier(save_path)


                if isinstance(labels, str):
                    labels = [labels]
                if labels is None:
                    labels = ['ingrediente']

                classified[filename] = labels
                detected_total.extend(labels)

        if saved_files:
            flash(f'Se subieron {len(saved_files)} archivo(s).', 'success')
        else:
            flash('No se subió ningún archivo válido.', 'warning')

        # aggregate suggestions
        suggestions = suggest_recipes(detected_total)
        return render_template('upload.html', title='HoMieS FooDS - Subir fotos',
                               mensaje='Ingrese las fotos de los alimentos con los que desea cocinar',
                               files=os.listdir(app.config['UPLOAD_FOLDER']),
                               classified=classified,
                               suggestions=suggestions)

    else:
        existing = sorted(os.listdir(app.config['UPLOAD_FOLDER']))
        return render_template('upload.html', title='HoMieS FooDS - Subir fotos',
                               mensaje='Ingrese las fotos de los alimentos con los que desea cocinar',
                               files=existing,
                               classified={},
                               suggestions=[])

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
