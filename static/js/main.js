// JavaScript principal para el sistema de productos

document.addEventListener('DOMContentLoaded', function() {
    // Agregar animación de fade-in a las tarjetas
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'opacity 0.5s ease-in-out, transform 0.5s ease-in-out';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });

    // Validación de formularios
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
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
            if (!confirm('¿Está seguro de que desea eliminar este elemento?')) {
                e.preventDefault();
            }
        });
    });

    // Formateo automático de números de moneda
    const currencyInputs = document.querySelectorAll('input[type="number"][step="0.01"]');
    currencyInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value) {
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
    });

    // Validación de SKU único
    const skuInput = document.getElementById('sku');
    if (skuInput) {
        skuInput.addEventListener('blur', function() {
            const sku = this.value;
            if (sku) {
                // Aquí podrías agregar una validación AJAX para verificar si el SKU ya existe
                // Por ahora, solo validamos el formato
                if (sku.length < 3) {
                    this.setCustomValidity('El SKU debe tener al menos 3 caracteres');
                } else {
                    this.setCustomValidity('');
                }
            }
        });
    }

    // Tooltips para botones de acción
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Mejorar la experiencia de la tabla
    const tableRows = document.querySelectorAll('.producto-row');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#f8f9fa';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });

    // Cargar imagen de preview
    const imagenInput = document.getElementById('imagen');
    if (imagenInput) {
        imagenInput.addEventListener('input', function() {
            const url = this.value;
            if (url) {
                // Crear elemento de preview si no existe
                let preview = document.getElementById('imagen-preview');
                if (!preview) {
                    preview = document.createElement('img');
                    preview.id = 'imagen-preview';
                    preview.className = 'img-thumbnail mt-2';
                    preview.style.maxWidth = '200px';
                    preview.style.maxHeight = '200px';
                    preview.style.objectFit = 'cover';
                    this.parentNode.appendChild(preview);
                }
                
                preview.src = url;
                preview.onerror = function() {
                    this.style.display = 'none';
                };
                preview.onload = function() {
                    this.style.display = 'block';
                };
            }
        });
    }

    // Calcular margen automáticamente
    const precioVentaInput = document.getElementById('precio_venta');
    const costoUnitarioInput = document.getElementById('costo_unitario');
    
    if (precioVentaInput && costoUnitarioInput) {
        function calcularMargen() {
            const precio = parseFloat(precioVentaInput.value) || 0;
            const costo = parseFloat(costoUnitarioInput.value) || 0;
            
            if (precio > 0 && costo > 0) {
                const margen = precio - costo;
                const porcentaje = ((margen / costo) * 100).toFixed(1);
                
                // Mostrar información del margen
                let margenInfo = document.getElementById('margen-info');
                if (!margenInfo) {
                    margenInfo = document.createElement('div');
                    margenInfo.id = 'margen-info';
                    margenInfo.className = 'alert alert-info mt-2';
                    costoUnitarioInput.parentNode.appendChild(margenInfo);
                }
                
                margenInfo.innerHTML = `
                    <small>
                        <i class="fas fa-chart-line"></i> 
                        Margen: $${margen.toFixed(2)} (${porcentaje}%)
                    </small>
                `;
            }
        }
        
        precioVentaInput.addEventListener('input', calcularMargen);
        costoUnitarioInput.addEventListener('input', calcularMargen);
    }

    // Mejorar la experiencia de búsqueda en la tabla
    const searchInput = document.getElementById('search-productos');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = document.querySelectorAll('.producto-row');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    // Animación de carga para botones
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando...';
            this.disabled = true;
            
            // Revertir después de 3 segundos si no hay respuesta
            setTimeout(() => {
                this.innerHTML = originalText;
                this.disabled = false;
            }, 3000);
        });
    });

    // Mejorar la accesibilidad
    const focusableElements = document.querySelectorAll('button, input, select, textarea, a[href]');
    focusableElements.forEach(element => {
        element.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && this.tagName === 'BUTTON') {
                this.click();
            }
        });
    });

    // Notificaciones toast (si se implementan en el futuro)
    function showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toast-container') || createToastContainer();
        const toast = createToast(message, type);
        toastContainer.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        toast.addEventListener('hidden.bs.toast', function() {
            toast.remove();
        });
    }
    
    function createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '1055';
        document.body.appendChild(container);
        return container;
    }
    
    function createToast(message, type) {
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        return toast;
    }

    // Hacer disponible la función showToast globalmente
    window.showToast = showToast;
});

// Funciones utilitarias globales
window.formatCurrency = function(amount) {
    return new Intl.NumberFormat('es-AR', {
        style: 'currency',
        currency: 'ARS'
    }).format(amount);
};

window.formatDate = function(date) {
    return new Intl.DateTimeFormat('es-AR').format(new Date(date));
};

window.validateSKU = function(sku) {
    return /^[A-Z0-9]{3,}$/.test(sku);
};

window.validateURL = function(url) {
    try {
        new URL(url);
        return true;
    } catch {
        return false;
    }
};