import streamlit as st
from dataclasses import dataclass
from typing import List

# 1. DEFINICIÓN DEL REGISTRO PRINCIPAL (Concepto Unidad 2)
@dataclass
class ProductoServicio:
    id_item: str           # CLAVE PRIMARIA: Alfanumérica y unívoca
    nombre: str            # Nombre comercial
    categoria: str         # 'Producto' o 'Servicio'
    tipo_mascota: str      # Especie destino
    precio: float          # Costo/Tarifa
    stock_disponible: int  # Unidades o cupos restantes
    es_personalizado: bool # Control de lógica para personalización

# 2. INICIALIZACIÓN DEL ESTADO DE LA SESIÓN (Mantiene los datos vivos en la web)
if "catalogo" not in st.session_state:
    st.session_state.catalogo = [
        ProductoServicio("PROD-001", "Identificador de Acero Grabado", "Producto", "Todos", 1450.00, 150, True),
        ProductoServicio("PROD-002", "Pretal Ergonómico Bordado", "Producto", "Perro", 4800.00, 3, True),
        ProductoServicio("SERV-101", "Adiestramiento Canino (4 Sesiones)", "Servicio", "Perro", 18000.00, 12, True),
        ProductoServicio("SERV-102", "Estadía de Guardería (Finde)", "Servicio", "Perro", 7500.00, 8, False)
    ]

# --- INTERFAZ GRÁFICA CON STREAMLIT ---
st.set_page_config(page_title="PetMatch e-Commerce", page_icon="🐾", layout="centered")

st.title("🐾 PetMatch: Experiencias & Cuidados a Medida")
st.write("**Materia:** Algoritmos y Estructuras de Datos / Sistemas")
st.markdown("---")

# SECCIÓN A: Visualización del Catálogo (Lectura de Registros)
st.header("🛒 Catálogo de la Plataforma")
st.caption("Los datos están organizados internamente como un arreglo de registros estructurados.")

for item in st.session_state.catalogo:
    with st.container():
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader(f"[{item.id_item}] {item.nombre}")
            st.write(f"🔹 **Categoría:** {item.categoria} | **Mascota:** {item.tipo_mascota}")
            if item.es_personalizado:
                st.info("✨ Este ítem permite personalización con los datos de tu mascota.")
        with col2:
            st.metric(label="Precio", value=f"${item.precio:,.2f}")
            st.metric(label="Stock / Cupos", value=item.stock_disponible)
        st.markdown("---")

# SECCIÓN B: Operación del Sistema (Búsqueda y Modificación por Clave Primaria)
st.header("🛍️ Panel de Transacciones")
st.write("Seleccioná la clave única para modificar el stock del registro correspondiente:")

# Selector visual que toma las claves del registro como índice
id_seleccionado = st.selectbox(
    "Clave del Registro (id_item):",
    options=[item.id_item for item in st.session_state.catalogo]
)

# Algoritmo de búsqueda por clave primaria
registro_encontrado = next((item for item in st.session_state.catalogo if item.id_item == id_seleccionado), None)

if registro_encontrado:
    st.write(f"**Ítem apuntado:** {registro_encontrado.nombre}")
    
    # Campo dinámico condicionado por el valor booleano del registro
    if registro_encontrado.es_personalizado:
        nombre_mascota = st.text_input("📝 Nombre de la mascota y detalles del grabado/bordado:")
    
    # Botón de acción que impacta la estructura de datos
    if st.button("Confirmar Compra / Reserva"):
        if registro_encontrado.stock_disponible > 0:
            # Modificación directa sobre el campo del registro
            registro_encontrado.stock_disponible -= 1
            st.success(f"✅ Éxito. Se descontó 1 unidad de la clave '{id_seleccionado}'.")
            st.rerun() # Recarga los componentes visuales para reflejar el nuevo stock arriba
        else:
            st.error("❌ Error: Stock insuficiente para procesar la solicitud.")