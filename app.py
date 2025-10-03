import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import sqlite3
from contextlib import closing

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'app.db')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT NOT NULL UNIQUE,
    image_filename TEXT,
    quantity INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'activo',
    sale_price REAL NOT NULL DEFAULT 0,
    category TEXT,
    description TEXT,
    inventory_policy TEXT,
    supplier TEXT,
    unit_cost REAL NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_db_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with closing(get_db_connection()) as conn:
        conn.executescript(SCHEMA_SQL)
        conn.commit()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Ensure DB exists
    init_db()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # Create (Alta)
    @app.route('/products/new', methods=['GET', 'POST'])
    def create_product():
        if request.method == 'POST':
            form = request.form
            sku = form.get('sku', '').strip()
            quantity = form.get('quantity') or 0
            status = form.get('status', 'activo')
            sale_price = form.get('sale_price') or 0
            category = form.get('category', '').strip()
            description = form.get('description', '').strip()
            inventory_policy = form.get('inventory_policy', '').strip()
            supplier = form.get('supplier', '').strip()
            unit_cost = form.get('unit_cost') or 0

            image_file = request.files.get('image')
            image_filename = None
            if image_file and image_file.filename:
                if allowed_file(image_file.filename):
                    filename = secure_filename(image_file.filename)
                    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    # Avoid overwrite by adding suffix if exists
                    base, ext = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(save_path):
                        filename = f"{base}_{counter}{ext}"
                        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        counter += 1
                    image_file.save(save_path)
                    image_filename = filename
                else:
                    flash('Formato de imagen no permitido', 'error')
                    return redirect(request.url)

            try:
                with closing(get_db_connection()) as conn:
                    conn.execute(
                        """
                        INSERT INTO products
                        (sku, image_filename, quantity, status, sale_price, category, description, inventory_policy, supplier, unit_cost)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            sku,
                            image_filename,
                            int(quantity),
                            status,
                            float(sale_price),
                            category,
                            description,
                            inventory_policy,
                            supplier,
                            float(unit_cost),
                        ),
                    )
                    conn.commit()
                flash('Producto creado correctamente', 'success')
                return redirect(url_for('list_products'))
            except sqlite3.IntegrityError:
                flash('SKU duplicado. Ingrese un SKU único.', 'error')
            except Exception as e:
                flash(f'Error al crear producto: {e}', 'error')

        return render_template('create_product.html')

    # List + Search (Consulta)
    @app.route('/products')
    def list_products():
        q = request.args.get('q', '').strip()
        where = ''
        params = []
        if q:
            where = "WHERE sku LIKE ? OR category LIKE ? OR supplier LIKE ? OR description LIKE ?"
            like = f"%{q}%"
            params = [like, like, like, like]
        with closing(get_db_connection()) as conn:
            rows = conn.execute(
                f"SELECT * FROM products {where} ORDER BY created_at DESC",
                params,
            ).fetchall()
        return render_template('list_products.html', products=rows, q=q)

    # Detail + Edit (Modificacion)
    @app.route('/products/<int:product_id>', methods=['GET', 'POST'])
    def product_detail(product_id: int):
        with closing(get_db_connection()) as conn:
            product = conn.execute(
                "SELECT * FROM products WHERE id = ?",
                (product_id,),
            ).fetchone()
        if not product:
            flash('Producto no encontrado', 'error')
            return redirect(url_for('list_products'))

        if request.method == 'POST':
            form = request.form
            sku = form.get('sku', '').strip()
            quantity = form.get('quantity') or 0
            status = form.get('status', 'activo')
            sale_price = form.get('sale_price') or 0
            category = form.get('category', '').strip()
            description = form.get('description', '').strip()
            inventory_policy = form.get('inventory_policy', '').strip()
            supplier = form.get('supplier', '').strip()
            unit_cost = form.get('unit_cost') or 0

            image_file = request.files.get('image')
            image_filename = product['image_filename']
            if image_file and image_file.filename:
                if allowed_file(image_file.filename):
                    filename = secure_filename(image_file.filename)
                    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    base, ext = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(save_path):
                        filename = f"{base}_{counter}{ext}"
                        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        counter += 1
                    image_file.save(save_path)
                    image_filename = filename
                else:
                    flash('Formato de imagen no permitido', 'error')
                    return redirect(request.url)

            try:
                with closing(get_db_connection()) as conn:
                    conn.execute(
                        """
                        UPDATE products
                        SET sku=?, image_filename=?, quantity=?, status=?, sale_price=?, category=?, description=?, inventory_policy=?, supplier=?, unit_cost=?, updated_at=CURRENT_TIMESTAMP
                        WHERE id=?
                        """,
                        (
                            sku,
                            image_filename,
                            int(quantity),
                            status,
                            float(sale_price),
                            category,
                            description,
                            inventory_policy,
                            supplier,
                            float(unit_cost),
                            product_id,
                        ),
                    )
                    conn.commit()
                flash('Producto actualizado', 'success')
                return redirect(url_for('product_detail', product_id=product_id))
            except sqlite3.IntegrityError:
                flash('SKU duplicado. Ingrese un SKU único.', 'error')
            except Exception as e:
                flash(f'Error al actualizar: {e}', 'error')

        return render_template('product_detail.html', product=product)

    # Delete (Baja)
    @app.route('/products/<int:product_id>/delete', methods=['POST'])
    def delete_product(product_id: int):
        try:
            with closing(get_db_connection()) as conn:
                conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
                conn.commit()
            flash('Producto eliminado', 'success')
        except Exception as e:
            flash(f'Error al eliminar: {e}', 'error')
        return redirect(url_for('list_products'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
