import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from werkzeug.utils import secure_filename

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'products.db')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key'  # reemplazar en prod
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB

    def get_db_connection():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db():
        conn = get_db_connection()
        conn.execute(
            """
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
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            );
            """
        )
        conn.commit()
        conn.close()

    @app.cli.command('init-db')
    def init_db_command():
        init_db()
        print('Base de datos inicializada en', DB_PATH)

    def allowed_file(filename: str) -> bool:
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    @app.route('/products/new', methods=['GET', 'POST'])
    def create_product():
        if request.method == 'POST':
            sku = request.form.get('sku', '').strip()
            quantity = request.form.get('quantity', '0').strip()
            status = request.form.get('status', 'activo').strip()
            sale_price = request.form.get('sale_price', '0').strip()
            category = request.form.get('category', '').strip()
            description = request.form.get('description', '').strip()
            inventory_policy = request.form.get('inventory_policy', '').strip()
            supplier = request.form.get('supplier', '').strip()
            unit_cost = request.form.get('unit_cost', '0').strip()

            if not sku:
                flash('SKU es requerido', 'danger')
                return redirect(request.url)

            image_file = request.files.get('image')
            image_filename = None
            if image_file and image_file.filename:
                if not allowed_file(image_file.filename):
                    flash('Formato de imagen no permitido', 'danger')
                    return redirect(request.url)
                filename = secure_filename(image_file.filename)
                base, ext = os.path.splitext(filename)
                safe_name = f"{sku}{ext.lower()}"
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)
                image_file.save(save_path)
                image_filename = safe_name

            try:
                conn = get_db_connection()
                conn.execute(
                    """
                    INSERT INTO products (
                        sku, image_filename, quantity, status, sale_price, category,
                        description, inventory_policy, supplier, unit_cost, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
                    """,
                    (
                        sku, image_filename, int(quantity or 0), status, float(sale_price or 0),
                        category, description, inventory_policy, supplier, float(unit_cost or 0)
                    ),
                )
                conn.commit()
            except sqlite3.IntegrityError:
                flash('SKU duplicado. Debe ser único.', 'danger')
                return redirect(request.url)
            finally:
                conn.close()

            flash('Producto creado', 'success')
            return redirect(url_for('list_products'))

        return render_template('create_product.html')

    @app.route('/products', methods=['GET'])
    def list_products():
        q = request.args.get('q', '').strip()
        conn = get_db_connection()
        if q:
            rows = conn.execute(
                """
                SELECT * FROM products
                WHERE sku LIKE ? OR category LIKE ? OR supplier LIKE ? OR description LIKE ?
                ORDER BY created_at DESC
                """,
                (f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%"),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM products ORDER BY created_at DESC"
            ).fetchall()
        conn.close()
        return render_template('list_products.html', products=rows, q=q)

    @app.route('/products/<int:product_id>')
    def product_detail(product_id: int):
        conn = get_db_connection()
        row = conn.execute(
            "SELECT * FROM products WHERE id = ?",
            (product_id,),
        ).fetchone()
        conn.close()
        if not row:
            flash('Producto no encontrado', 'warning')
            return redirect(url_for('list_products'))
        return render_template('product_detail.html', p=row)

    @app.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
    def edit_product(product_id: int):
        conn = get_db_connection()
        row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
        if not row:
            conn.close()
            flash('Producto no encontrado', 'warning')
            return redirect(url_for('list_products'))

        if request.method == 'POST':
            sku = request.form.get('sku', row['sku']).strip()
            quantity = request.form.get('quantity', row['quantity'])
            status = request.form.get('status', row['status']).strip()
            sale_price = request.form.get('sale_price', row['sale_price'])
            category = request.form.get('category', row['category'] or '').strip()
            description = request.form.get('description', row['description'] or '').strip()
            inventory_policy = request.form.get('inventory_policy', row['inventory_policy'] or '').strip()
            supplier = request.form.get('supplier', row['supplier'] or '').strip()
            unit_cost = request.form.get('unit_cost', row['unit_cost'])

            image_file = request.files.get('image')
            image_filename = row['image_filename']
            if image_file and image_file.filename:
                if not allowed_file(image_file.filename):
                    flash('Formato de imagen no permitido', 'danger')
                    return redirect(request.url)
                filename = secure_filename(image_file.filename)
                base, ext = os.path.splitext(filename)
                safe_name = f"{sku}{ext.lower()}"
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)
                image_file.save(save_path)
                image_filename = safe_name

            try:
                conn.execute(
                    """
                    UPDATE products SET
                        sku = ?, image_filename = ?, quantity = ?, status = ?,
                        sale_price = ?, category = ?, description = ?, inventory_policy = ?,
                        supplier = ?, unit_cost = ?, updated_at = datetime('now')
                    WHERE id = ?
                    """,
                    (
                        sku, image_filename, int(quantity or 0), status, float(sale_price or 0),
                        category, description, inventory_policy, supplier, float(unit_cost or 0),
                        product_id,
                    ),
                )
                conn.commit()
            except sqlite3.IntegrityError:
                flash('SKU duplicado. Debe ser único.', 'danger')
                return redirect(request.url)
            finally:
                conn.close()

            flash('Producto actualizado', 'success')
            return redirect(url_for('product_detail', product_id=product_id))

        conn.close()
        return render_template('edit_product.html', p=row)

    @app.route('/products/<int:product_id>/delete', methods=['POST'])
    def delete_product(product_id: int):
        conn = get_db_connection()
        row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
        if not row:
            conn.close()
            flash('Producto no encontrado', 'warning')
            return redirect(url_for('list_products'))
        image_filename = row['image_filename']
        conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        conn.close()

        if image_filename:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            except FileNotFoundError:
                pass

        flash('Producto eliminado', 'success')
        return redirect(url_for('list_products'))

    # API mínima para tabla dinámica (opcional)
    @app.route('/api/products')
    def api_products():
        q = request.args.get('q', '').strip()
        conn = get_db_connection()
        if q:
            rows = conn.execute(
                """
                SELECT * FROM products
                WHERE sku LIKE ? OR category LIKE ? OR supplier LIKE ? OR description LIKE ?
                ORDER BY created_at DESC
                """,
                (f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%"),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM products ORDER BY created_at DESC"
            ).fetchall()
        conn.close()
        return jsonify([dict(r) for r in rows])

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # Asegura que la BD exista en el primer arranque
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.close()
    app.run(host='0.0.0.0', port=5000, debug=True)
