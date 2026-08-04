from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import BaseDocTemplate, Frame, Image, PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "Proyecto_Integrador_DevOps_Fase_1.pdf"
LOGO = ROOT / "docs" / "assets" / "logoespam.png"

GREEN = colors.HexColor("#006B58")
DARK_GREEN = colors.HexColor("#00483D")
NAVY = colors.HexColor("#12304A")
BLUE = colors.HexColor("#147EA3")
LIGHT_GREEN = colors.HexColor("#E9F5F1")
LIGHT_BLUE = colors.HexColor("#EAF4F8")
LIGHT_GRAY = colors.HexColor("#F3F5F7")
MID_GRAY = colors.HexColor("#667785")
WHITE = colors.white

PAGE_W, PAGE_H = A4
MARGIN = 1.45 * cm
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverTitle", fontName="Helvetica-Bold", fontSize=22, leading=27, textColor=NAVY, alignment=TA_CENTER, spaceAfter=9))
styles.add(ParagraphStyle(name="CoverSub", fontName="Helvetica", fontSize=12, leading=16, textColor=MID_GRAY, alignment=TA_CENTER, spaceAfter=6))
styles.add(ParagraphStyle(name="Kicker", fontName="Helvetica-Bold", fontSize=7.4, leading=9, textColor=GREEN, spaceAfter=2))
styles.add(ParagraphStyle(name="H1a", fontName="Helvetica-Bold", fontSize=16, leading=19, textColor=NAVY, spaceAfter=5))
styles.add(ParagraphStyle(name="H2a", fontName="Helvetica-Bold", fontSize=10.5, leading=12.5, textColor=GREEN, spaceBefore=4, spaceAfter=3))
styles.add(ParagraphStyle(name="Bodya", fontName="Helvetica", fontSize=8.15, leading=10.5, textColor=colors.HexColor("#263844"), alignment=TA_JUSTIFY, spaceAfter=4))
styles.add(ParagraphStyle(name="Smalla", fontName="Helvetica", fontSize=7.0, leading=8.4, textColor=colors.HexColor("#334954")))
styles.add(ParagraphStyle(name="Tinyaa", fontName="Helvetica", fontSize=6.35, leading=7.6, textColor=colors.HexColor("#334954")))
styles.add(ParagraphStyle(name="Callout", fontName="Helvetica-Bold", fontSize=8.0, leading=10, textColor=DARK_GREEN))


def p(text, style="Bodya"):
    return Paragraph(text, styles[style])


def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setFillColor(GREEN)
        canvas.rect(0, PAGE_H - 0.3 * cm, PAGE_W, 0.3 * cm, fill=1, stroke=0)
        canvas.setFont("Helvetica-Bold", 7)
        canvas.setFillColor(NAVY)
        canvas.drawString(MARGIN, PAGE_H - 0.82 * cm, "ESPAM MFL  |  DEVOPS  |  PROYECTO INTEGRADOR - FASE 1")
        canvas.setStrokeColor(colors.HexColor("#D5DEE3"))
        canvas.line(MARGIN, 0.95 * cm, PAGE_W - MARGIN, 0.95 * cm)
        canvas.setFont("Helvetica", 6.6)
        canvas.setFillColor(MID_GRAY)
        canvas.drawString(MARGIN, 0.58 * cm, "Cristhian Alfredo Zambrano Zambrano")
        canvas.drawRightString(PAGE_W - MARGIN, 0.58 * cm, f"Página {doc.page - 1} de 4")
    canvas.restoreState()


def table(headers, rows, widths, font=6.35):
    head_style = ParagraphStyle("head", parent=styles["Tinyaa"], fontName="Helvetica-Bold", fontSize=font, leading=font + 1.3, textColor=WHITE)
    body_style = ParagraphStyle("cell", parent=styles["Tinyaa"], fontSize=font, leading=font + 1.35)
    data = [[Paragraph(str(x), head_style) for x in headers]]
    data += [[Paragraph(str(x), body_style) for x in row] for row in rows]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CED8DE")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3.4), ("RIGHTPADDING", (0, 0), (-1, -1), 3.4),
        ("TOPPADDING", (0, 0), (-1, -1), 2.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.4),
    ]))
    return t


def flow(labels, caption):
    cells = []
    for idx, label in enumerate(labels):
        fill = LIGHT_GREEN if idx < len(labels) - 2 else colors.HexColor("#FFF2D9")
        cells.append(Table([[p(f"<b>{idx + 1}</b><br/>{label}", "Tinyaa")]], colWidths=[(16.7 * cm / len(labels)) - 0.08 * cm], style=[
            ("BACKGROUND", (0, 0), (-1, -1), fill), ("BOX", (0, 0), (-1, -1), 0.7, GREEN),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
    outer = Table([cells], colWidths=[16.7 * cm / len(labels)] * len(labels), hAlign="LEFT")
    outer.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 1), ("RIGHTPADDING", (0, 0), (-1, -1), 1)]))
    return [outer, p(caption, "Tinyaa")]


def callout(label, text, fill=LIGHT_GREEN):
    t = Table([[p(label, "Callout"), p(text, "Smalla")]], colWidths=[3.2 * cm, 13.5 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), fill), ("BOX", (0, 0), (-1, -1), 0.7, GREEN), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("PADDING", (0, 0), (-1, -1), 6)]))
    return t


doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN, topMargin=1.35 * cm, bottomMargin=1.2 * cm,
                      title="Proyecto integrador DevOps - Fase 1", author="Cristhian Alfredo Zambrano Zambrano")
frame = Frame(MARGIN, 1.2 * cm, PAGE_W - 2 * MARGIN, PAGE_H - 2.55 * cm, id="frame")
doc.addPageTemplates(PageTemplate(id="pages", frames=[frame], onPage=header_footer))
story = []

# Portada
story += [Spacer(1, 1.5 * cm), Image(str(LOGO), width=7.2 * cm, height=2.5 * cm), Spacer(1, 1.35 * cm),
          p("MAESTRÍA EN DISEÑO WEB Y DESARROLLO DE APPS", "CoverSub"),
          p("PROYECTO INTEGRADOR DEVOPS", "CoverTitle"), p("Fase 1: diagnóstico y planificación", "CoverSub"), Spacer(1, 1.0 * cm)]
meta = table(["Datos académicos", "Información"], [
    ["Estudiante", "Cristhian Alfredo Zambrano Zambrano"], ["Docente", "Mg. Enrique Javier Macías Arias"],
    ["Asignatura", "DevOps"], ["Cohorte", "II Cohorte - Paralelo A"],
], [4.1 * cm, 10.0 * cm], 8.2)
story += [meta, Spacer(1, 2.1 * cm), p("ESPAM MFL  |  2026", "CoverSub"), PageBreak()]

# Página 1
story += [p("01 · CONTEXTO Y FLUJO", "Kicker"), p("Sistema web CRUD para la gestión de usuarios", "H1a"),
          p("Aplicación académica que centraliza la creación, consulta, actualización y eliminación de usuarios y la asignación de roles. Beneficia a administradores y personal de soporte que requieren mantener registros consistentes mediante una interfaz web.")]
story += [table(["Capa", "Tecnologías", "Responsabilidad"], [
    ["Frontend", "React 18, TypeScript, Vite y Mantine", "Interfaz, formularios, tabla y consumo de la API."],
    ["Backend", "Node.js, Fastify, TypeScript y Prisma", "Reglas del CRUD, validación y acceso a datos."],
    ["Datos", "PostgreSQL 17", "Persistencia de usuarios."],
    ["Ejecución", "Docker y Docker Compose", "Construcción y coordinación de tres servicios."],
], [2.4 * cm, 6.0 * cm, 8.3 * cm]), p("Arquitectura actual", "H2a")]
story += flow(["Administrador", "Frontend<br/>React", "API<br/>Fastify", "Prisma", "PostgreSQL"], "Figura 1. Flujo de solicitudes en la arquitectura actual.")
story += [p("Flujo actual del código al despliegue", "H2a"), p("No existe CI/CD: una persona modifica, construye, valida y publica. Las esperas no están medidas y la evidencia se limita a la consola y a la comprobación visual.")]
story += flow(["Modificar<br/>código", "Guardar<br/>cambios", "Compose<br/>build", "Instalar<br/>dependencias", "Prisma<br/>db push", "Prueba<br/>manual", "Publicar<br/>manual"], "Figura 2. Si falla, se corrige y repite manualmente el flujo.")
story += [table(["Etapa", "Responsable/evidencia", "Actividad manual o riesgo"], [
    ["Código/integración", "Desarrollador; archivos y commit", "Revisión sin validación automática."],
    ["Build/datos", "Contenedores; consola", "Dependencias y db push al arrancar."],
    ["Prueba/aprobación", "Desarrollador; navegador", "CRUD manual, sin suite independiente."],
    ["Despliegue/operación", "Desarrollador; logs", "Sin pipeline, rollback, alertas o métricas."],
], [3.0 * cm, 6.2 * cm, 7.5 * cm]), PageBreak()]

# Página 2
story += [p("02 · DIAGNÓSTICO", "Kicker"), p("Cuellos de botella, actividades manuales y riesgos", "H1a"),
          p("La prioridad combina impacto y probabilidad de 1 (bajo) a 3 (alto). La puntuación es su producto; los valores 9 se atienden primero.")]
story += [table(["Hallazgo/tipo", "Causa/evidencia", "Consecuencia", "I×P"], [
    ["Sin CI/CD<br/>Proceso/herramienta", "Validación mediante comandos locales.", "Errores tardíos y baja trazabilidad.", "3×3=9"],
    ["Sin pruebas<br/>Proceso", "No existen suites unitarias, API o e2e.", "Regresiones, retrabajo y aprobación subjetiva.", "3×3=9"],
    ["Dependencias vulnerables<br/>Seguridad", "npm audit: 2 frontend y 6 altos backend.", "Riesgo de cadena de suministro.", "3×3=9"],
    ["Credenciales originales<br/>Seguridad", "Contraseña en .env/Compose; retirada.", "Exposición y acceso no autorizado.", "3×2=6"],
    ["Sin observabilidad<br/>Operación", "Logs reactivos, sin métricas o alertas.", "Detección y diagnóstico tardíos.", "2×3=6"],
    ["Sin rollback/respaldo<br/>Continuidad", "Sin runbook o restauración probada.", "Mayor indisponibilidad o pérdida.", "3×2=6"],
], [4.0 * cm, 5.0 * cm, 5.9 * cm, 1.8 * cm], 6.2), p("Diagnóstico CALMS", "H2a")]
story += [table(["Dimensión", "Estado actual", "Brecha y respuesta"], [
    ["Cultura", "Responsabilidad concentrada.", "Compartir decisiones y revisar fallos sin culpa."],
    ["Automatización", "Compose reproduce servicios.", "Automatizar build, pruebas, seguridad y entrega."],
    ["Lean", "Arquitectura simple.", "Reducir lotes y retrabajo con validación temprana."],
    ["Medición", "Logs, sin línea base.", "Recopilar DORA, cobertura e incidentes."],
    ["Sharing", "Código recibido como ZIP.", "Repositorio, README, diagramas y runbook."],
], [2.6 * cm, 5.0 * cm, 9.1 * cm]), Spacer(1, 0.1 * cm),
          callout("Prioridad inmediata", "Automatizar compilación y pruebas, bloquear secretos y visibilizar dependencias vulnerables antes de automatizar el despliegue."), PageBreak()]

# Página 3
story += [p("03 · PROPUESTA INICIAL", "Kicker"), p("Adopción DevOps incremental y medible", "H1a"),
          callout("Objetivo", "Reducir errores manuales y hacer reproducible, segura y medible la entrega mediante validación temprana, configuración protegida y retroalimentación operativa."),
          p("Alcance y arquitectura preliminar", "H2a")]
story += [table(["Dentro del alcance", "Fuera del alcance inicial"], [[
    "GitHub; commits/revisión; CI; pruebas; SAST; dependencias/secretos; imágenes Docker; QA; observabilidad y rollback.",
    "Kubernetes, multirregión y despliegue automático a producción: añadirían complejidad antes de estabilizar el flujo.",
]], [8.6 * cm, 8.1 * cm])]
story += flow(["Push", "Build", "Pruebas", "Seguridad", "Imagen", "QA", "Desplegar", "Observar"], "Figura 3. Flujo propuesto con retroalimentación desde operación.")
story += [p("Trazabilidad problema-práctica-métrica", "H2a"), table(["Problema", "Práctica/herramienta", "Métrica", "Resultado"], [
    ["Validación manual", "CI con GitHub Actions o Jenkins.", "Lead time/frecuencia", "Evidencia automática."],
    ["Pruebas inexistentes", "Pruebas unitarias y API.", "Cobertura/fallos", "Menos regresión."],
    ["Dependencias/secretos", "npm audit, Dependabot, SAST y Secrets.", "Hallazgos/versión", "Riesgo visible temprano."],
    ["Detección tardía", "Logs, métricas y OpenTelemetry.", "Detección/MTTR", "Respuesta más rápida."],
    ["Recuperación", "Imágenes, rollback, respaldo y runbook.", "MTTR/restauración", "Continuidad verificable."],
], [3.2 * cm, 5.6 * cm, 3.5 * cm, 4.4 * cm]), p("Roadmap de 90 días", "H2a")]
story += [table(["Periodo", "Cultura", "Proceso", "Técnica/evidencia"], [
    ["0-30", "Responsabilidad compartida.", "Commits, revisión y criterios.", "CI build + secretos; resultado por cambio."],
    ["31-60", "Revisión sin culpa.", "Aceptación y rollback.", "Pruebas, SAST y dependencias visibles."],
    ["61-90", "Revisión de métricas.", "Cambios pequeños y QA.", "Imágenes, observabilidad y runbook."],
], [2.0 * cm, 3.5 * cm, 4.6 * cm, 6.6 * cm]), PageBreak()]

# Página 4
story += [p("04 · MEDICIÓN Y CIERRE", "Kicker"), p("Línea base, metas y gestión de riesgos", "H1a"),
          p("No se inventan cifras históricas: la ausencia de medición es parte del diagnóstico. En los primeros 30 días el pipeline y el registro de incidentes generarán una línea base reproducible.")]
story += [table(["Métrica", "Base", "Obtención", "Meta a 90 días"], [
    ["Lead time", "No medido", "Commit a despliegue según CI/CD.", "Línea base y tendencia descendente."],
    ["Frecuencia", "No registrada", "Despliegues exitosos/mes.", "Al menos 2 controlados/mes."],
    ["Fallos", "No medida", "Rollback o corrección / total.", "Menor al 20 % tras la base."],
    ["Recuperación", "No medido", "Incidente a restauración.", "Runbook y menos de 60 min."],
    ["Cobertura", "0 % / sin suite", "Reporte automático del pipeline.", "60 % en lógica crítica."],
], [3.0 * cm, 2.4 * cm, 5.3 * cm, 6.0 * cm]), p("Riesgos del cambio y controles", "H2a")]
story += [table(["Riesgo", "Control y evidencia"], [
    ["Seguridad/privacidad", ".env excluido, secretos protegidos, escaneo, minimización y retención de logs."],
    ["Continuidad", "Healthchecks, respaldo/restauración, imágenes versionadas, rollback y runbook."],
    ["Adopción", "Automatización gradual, guía de contribución y revisión mensual de métricas."],
], [4.0 * cm, 12.7 * cm]), p("Conclusiones", "H2a"),
          p("El sistema es apropiado porque integra interfaz, API y base de datos, pero su flujo original depende de validaciones y despliegues manuales. Los cuellos críticos deben resolverse primero con compilación, pruebas y seguridad tempranas; después, entrega controlada, observabilidad y recuperación. La propuesta conecta cada problema con una práctica, evidencia y métrica, por lo que permite evaluar mejoras sin comparar personas ni inventar datos."),
          p("Referencias (APA 7)", "H2a"),
          p("DORA. (2024). <i>Accelerate State of DevOps Report 2024</i>. Google Cloud.<br/>ESPAM MFL. (2026). <i>Guía de estudio: Unidad 1 DevOps</i>.<br/>ESPAM MFL. (2026). <i>Presentación DevOps, Unidad 1, Sesiones 1-3</i> [Diapositivas].<br/>Kim, G., Humble, J., Debois, P., Willis, J., &amp; Forsgren, N. (2021). <i>The DevOps handbook</i> (2nd ed.). IT Revolution.", "Tinyaa"),
          Spacer(1, 0.12 * cm), callout("Repositorio público", "https://github.com/cazzSoft/proyecto-integrador-devops-fase1", LIGHT_BLUE)]

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.build(story)
print(OUT)
