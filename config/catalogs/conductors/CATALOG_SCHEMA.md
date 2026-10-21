# Esquema de catálogo de conductores (universal)

El motor **no depende de una marca**. Nexans/INDECO AAAC 6201 es solo la muestra
del artículo IEEE. Cada archivo JSON debe conservar trazabilidad documental y un
arreglo `conductors`.

## Campos obligatorios por conductor

- `section_mm2`
- `diameter_mm`
- `r20_ohm_km`
- `ampacity_a`

## Campos recomendados

- `id`: identificador único (obligatorio si hay varias construcciones por sección).
- `manufacturer`, `model`, `material`.
- `strands`, `wire_diameter_mm`.
- `gmr_mm`: opcional. Si la ficha lo entrega, el solver lo usa; si falta, se usa `GMR≈0.7788 r`.
- `mass_kg_km`.
- `alpha20_per_c`: coeficiente de variación de resistencia del material.
- `material_resistivity20_ohm_mm2_m`: resistividad intrínseca, si la fuente la publica.
- `max_continuous_temperature_c`: límite continuo IEEE 738.
- `datasheet_reference`: identificación documental de la ficha.

## Encabezado del catálogo

Incluir `name`, `manufacturer`, `product_family`, `source_url`, `source_note`,
`material_properties_source_url`, `material_properties_note` y `reference_conditions`
cuando estén disponibles.

## Cómo cargar

- Interfaz: `streamlit run streamlit_app.py` (subir JSON o elegir precargado).
- CLI: `--catalog ruta/al/catalogo.json` o `study.catalog_path` en YAML.
- Guía: `data/INPUTS.md`.

Los parámetros que no aparezcan en la ficha no deben inventarse como datos del
fabricante. Los supuestos geométricos o meteorológicos se declaran como escenario.
