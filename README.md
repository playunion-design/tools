# UNION · Press tools

Sitio estático (HTML puro, sin build en el servidor) con las herramientas y archivos de la rueda de prensa del 26 Nov 2026. Funciona en ordenador y en móvil.

## Qué hay

| Ruta | Qué es |
|---|---|
| `/` | Página de inicio con las herramientas (`index.html`) |
| `/kol/` | **KOL Invite Maker**: escribes el nombre del invitado y descarga/comparte la invitación 1080×1350 con su nombre. Una sola página con la fuente y el fondo incrustados |
| `assets/fonts/` | Special Gothic Condensed One (licencia OFL incluida) para el título de la página de inicio |
| `source/` | Lo necesario para regenerar `/kol/` (plantilla, fondo exportado de Figma, fuentes, `build.py`) |
| `vercel.json`, `robots.txt` | Ajustes: no indexar en buscadores, cabeceras básicas |

## Publicar (GitHub + Vercel, sin terminal)

1. GitHub: nuevo repositorio **privado** (por ejemplo `union-press`). En la página del repo: *Add file → Upload files*, arrastra **el contenido** de esta carpeta (no la carpeta en sí, para que `index.html` quede en la raíz) y *Commit changes*.
2. Vercel: *Add New → Project*, importa el repo. Framework Preset: **Other**. Deja vacíos Build Command y Output Directory. *Deploy*.
3. Abre la URL (`nombre.vercel.app`) en una ventana privada y en el móvil, sin sesión iniciada. Si pide login de Vercel: Project → Settings → Deployment Protection → desactiva Vercel Authentication para producción.
4. Cada cambio nuevo en GitHub se publica solo.

Nota: el plan gratuito de Vercel (Hobby) es para uso personal no comercial. Si el proyecto cuenta como comercial, el mismo repo se conecta igual a Cloudflare Pages o Netlify (también gratis).

## Añadir otra herramienta o archivo

1. Crea una carpeta con su `index.html` (por ejemplo `press-kit/index.html`) o sube el archivo (PDF, imágenes…).
2. En `index.html` de la raíz copia el bloque `<li> … </li>` de KOL Invite Maker y cambia enlace, título y texto.

## Cambiar el diseño de la invitación KOL

1. En Figma: duplica el frame KOL, pon la capa "Name · KOL (type here)" a **opacity 0** (no `visible = false`: colapsa el panel) y exporta PNG @1× (1080×1350).
2. Reemplaza `source/bg.png`.
3. Regenera: `pip install fonttools brotli` y `python3 source/build.py` (o pídeselo a Claude). Sube `kol/index.html` y `source/bg.png` al repo.
4. Si cambia la posición del nombre, ajusta `NAME_X` / `NAME_Y` en `source/kol-page.html` y vuelve a generar.

## Límites conocidos

- La fuente de marca no tiene algunas letras (vietnamita con varias marcas, tailandés, jemer, birmano): usan una fuente de respaldo y se ven distintas. La herramienta lo avisa y ofrece "Remove accents".
- Solo formato 4:5 (1080×1350).
- Los nombres no salen del dispositivo: todo se dibuja en el navegador.
