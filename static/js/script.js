// JavaScript para el CRUD de Productos

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Validación de formularios
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Auto-dismiss alerts después de 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirmación antes de eliminar
    const deleteButtons = document.querySelectorAll('[data-action="delete"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productName = this.dataset.productName;
            if (confirm(`¿Estás seguro de que deseas eliminar el producto "${productName}"?`)) {
                this.closest('form').submit();
            }
        });
    });

    // Cálculo automático de margen de ganancia en formularios
    const precioVentaInput = document.getElementById('precio_venta');
    const costoUnitarioInput = document.getElementById('costo_unitario');
    
    if (precioVentaInput && costoUnitarioInput) {
        function calcularMargen() {
            const precio = parseFloat(precioVentaInput.value) || 0;
            const costo = parseFloat(costoUnitarioInput.value) || 0;
            
            if (precio > 0 && costo > 0) {
                const margen = precio - costo;
                const porcentaje = ((margen / costo) * 100).toFixed(1);
                
                // Mostrar información de margen si existe un elemento para ello
                const margenElement = document.getElementById('margen-info');
                if (margenElement) {
                    margenElement.innerHTML = `
                        <small class="text-muted">
                            Margen: $${margen.toFixed(2)} (${porcentaje}%)
                        </small>
                    `;
                }
            }
        }
        
        precioVentaInput.addEventListener('input', calcularMargen);
        costoUnitarioInput.addEventListener('input', calcularMargen);
    }

    // Búsqueda en tiempo real en la tabla
    const searchInput = document.getElementById('searchInput');
    const table = document.getElementById('tablaProductos');
    
    if (searchInput && table) {
        searchInput.addEventListener('input', function() {
            const filter = this.value.toLowerCase();
            const rows = table.getElementsByTagName('tr');
            
            for (let i = 1; i < rows.length; i++) { // Empezar desde 1 para omitir el header
                const row = rows[i];
                const text = row.textContent.toLowerCase();
                
                if (text.includes(filter)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            }
        });
    }

    // Animación de entrada para las tarjetas
    const cards = document.querySelectorAll('.card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });

    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
});

// Función para mostrar información de producto en modal
function mostrarInfoProducto(productoId) {
    fetch(`/api/producto/${productoId}`)
        .then(response => response.json())
        .then(data => {
            // Llenar modal con datos del producto
            document.getElementById('modalSku').textContent = data.sku;
            document.getElementById('modalDescripcion').textContent = data.descripcion || 'Sin descripción';
            document.getElementById('modalCategoria').textContent = data.categoria;
            document.getElementById('modalCantidad').textContent = data.cantidad;
            document.getElementById('modalPrecio').textContent = `$${data.precio_venta}`;
            document.getElementById('modalEstado').textContent = data.estado;
            document.getElementById('modalProveedor').textContent = data.proveedor;
            
            // Mostrar modal
            const modal = new bootstrap.Modal(document.getElementById('modalInfoProducto'));
            modal.show();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al cargar la información del producto');
        });
}

// Función para confirmar eliminación
function confirmarEliminacion(productoId, sku) {
    if (confirm(`¿Estás seguro de que deseas eliminar el producto "${sku}"?`)) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/eliminar_producto/${productoId}`;
        document.body.appendChild(form);
        form.submit();
    }
}

// Función para copiar al portapapeles
function copiarAlPortapapeles(texto) {
    navigator.clipboard.writeText(texto).then(() => {
        // Mostrar notificación de éxito
        const toast = document.createElement('div');
        toast.className = 'toast-notification';
        toast.textContent = 'Copiado al portapapeles';
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #28a745;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            z-index: 9999;
            animation: slideIn 0.3s ease;
        `;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 2000);
    });
}

// Función para exportar datos (placeholder)
function exportarDatos(formato) {
    alert(`Función de exportación en formato ${formato} será implementada próximamente`);
}

// Función para validar SKU único
function validarSkuUnico(sku, productoId = null) {
    return fetch('/api/validar-sku', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            sku: sku,
            producto_id: productoId
        })
    })
    .then(response => response.json())
    .then(data => {
        return data.disponible;
    })
    .catch(error => {
        console.error('Error:', error);
        return true; // En caso de error, permitir continuar
    });
}

// Validación en tiempo real del SKU
const skuInput = document.getElementById('sku');
if (skuInput) {
    let timeoutId;
    skuInput.addEventListener('input', function() {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            const sku = this.value.trim();
            if (sku.length > 0) {
                validarSkuUnico(sku).then(disponible => {
                    const feedback = this.nextElementSibling;
                    if (disponible) {
                        this.classList.remove('is-invalid');
                        this.classList.add('is-valid');
                        if (feedback) feedback.textContent = 'SKU disponible';
                    } else {
                        this.classList.remove('is-valid');
                        this.classList.add('is-invalid');
                        if (feedback) feedback.textContent = 'SKU ya existe';
                    }
                });
            }
        }, 500);
    });
}