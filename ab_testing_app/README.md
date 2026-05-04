# A/B Testing App

Aplicacion educativa multipagina en Streamlit para ensenar A/B Testing en un curso de Analitica del Marketing a nivel posgrado.

## Instalacion

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecucion

Desde la carpeta `ab_testing_app`:

```bash
streamlit run app.py
```

## Estructura

- `app.py`: pagina de inicio.
- `pages/`: paginas multipagina de Streamlit.
- `src/ui/`: componentes visuales y estilos.
- `src/stats/`: funciones estadisticas para pruebas A/B.
- `src/simulation/`: funciones de simulacion.
- `src/data/`: datos ficticios para ejemplos.
