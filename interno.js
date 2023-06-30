const app = Vue.createApp({
    data() {
        return {
            productos: [],
            consultaNombre: '',
            consultaResultado: '',
            altaResultado: '',
            modificarResultado: '',
            altaNombre: '',
            altaDescripcion: '',
            altaStock: '',
            altaPrecio: '',
            modificarNombre: '',
            modificarNuevaDescripcion: '',
            modificarNuevoStock: '',
            modificarNuevoPrecio: '',
            mNombre: '',
            mDescripcion: '',
            mStock: '',
            mPrecio: '',
        };
    },
    methods: {
        consultarProducto() {
            fetch(`https://apiedison.pythonanywhere.com/productos/${this.consultaNombre}`)
                .then(response => response.json())
                .then(producto => {
                    if (producto) {
                        this.consultaResultado = `Nombre: ${producto.nombre}, Descripción: ${producto.descripcion}, Stock: ${producto.stock}, Precio: ${producto.precio}`;
                    } else {
                        this.consultaResultado = 'Producto no encontrado';
                    }
                })
                .catch(error => {
                    console.error(error);
                    this.consultaResultado = 'Error al realizar la consulta';
                });
        },
        altaProducto() {
            fetch('https://apiedison.pythonanywhere.com/productos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    nombre: this.altaNombre,
                    descripcion: this.altaDescripcion,
                    stock: this.altaStock,
                    precio: this.altaPrecio
                })
            })
                .then(response => {
                    if (response.ok) {
                        response.json()
                            .then(producto => {
                                this.altaNombre = '';
                                this.altaDescripcion = '';
                                this.altaStock = '';
                                this.altaPrecio = '';
                                this.listarProductos();
                                this.altaResultado = JSON.stringify(producto);
                            });
                    } else {
                        this.altaResultado = 'Alta no efectuada';
                    }
                })
                .catch(error => {
                    console.error(error);
                });
        },
        modificarProducto() {
            fetch(`https://apiedison.pythonanywhere.com/productos/${this.modificarNombre}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    descripcion: this.modificarNuevaDescripcion,
                    stock: this.modificarNuevoStock,
                    precio: this.modificarNuevoPrecio
                })
            })
                .then(response => {
                    if (response.ok) {
                        response.json()
                            .then(producto => {
                                this.modificarNombre = '';
                                this.modificarNuevaDescripcion = '';
                                this.modificarNuevoStock = '';
                                this.modificarNuevoPrecio = '';
                                this.listarProductos();
                                this.modificarResultado = JSON.stringify(producto);
                            });
                    } else {
                        this.modificarResultado = 'Modificación no efectuada';
                    }
                })
                .catch(error => {
                    console.error(error);
                });
        },
        listarProductos() {
            fetch('https://apiedison.pythonanywhere.com/productos')
                .then(response => response.json())
                .then(productos => {
                    this.productos = productos;
                })
                .catch(error => {
                    console.error(error);
                });
        },
        editarProducto(index) {
            const formulario = document.getElementById('formularioModificar');
            formulario.scrollIntoView({ behavior: 'smooth' });
            
            /*
            const producto = this.productos[index];
            this.mNombre = producto.nombre;
            this.mDescripcion = producto.descripcion;
            this.mStock = producto.stock;
            this.mPrecio = producto.precio;*/
        },
    },


    mounted() {
        this.listarProductos();
    }
});

app.mount('#app');
