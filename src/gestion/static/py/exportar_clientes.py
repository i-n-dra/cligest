from openpyxl import Workbook
from openpyxl.styles import Font, Border, Alignment, Side
from openpyxl.worksheet.dimensions import Dimension, RowDimension, ColumnDimension
from tempfile import NamedTemporaryFile
from django.http import Http404

titulo_font = Font(
    name='Century Gothic',
    size=20,
    bold=True,
    italic=False,
    vertAlign=None,
    underline='none',
    strike=False,
    color='808080')
subtitle_font = Font(
    name='Century Gothic',
    size=11,
    bold=True,
    italic=False,
    vertAlign=None,
    underline='none',
    strike=False,
    color='203764'
)
center_align = Alignment(
    horizontal='center',
    vertical='center',
    indent=0
)
thick_border = Border(
    right=Side(border_style='thick', color='808080'),
)
ficha_border = Border(
    outline=Side(
        border_style='thin',
        color='bfbfbf'
    )
)

wb = Workbook(write_only=False)

# grab the active worksheet
ws = wb.active
ws.title = "Clientes"
ws.freeze_panes = 'A3' # freeze top rows

ws['A1'] = 'CLIENTES'
titulo_cell = ws['A1']
titulo_cell.font = titulo_font
titulo_cell.alignment = center_align
ws.merge_cells('A1:S1')

# Rows can also be appended
subtitles = [
    # Datos Representante Legal #
    'Nombre(s)', # preguntar sobre esto ??
    'Apellido Paterno',
    'Apellido Materno',
    'RUN',
    'Tipo de Empresa',
    # Datos Empresa #
    'Razón Social',
    'Nombre de fantasía',
    'RUN',
    'Régimen Tributario',
    'Giro / Rubro',
    'Código S.I.I.',
    # Datos Financieros #
    'Tipo de contabilidad',
    'Cuenta corriente',
    'N° Cuenta Corriente',
    # Datos Contacto #
    'Correo electrónico',
    'Teléfono / Celular',
    'Región',
    'Comuna',
    'Dirección'
] # borde thick por cada categoria de datos
subtitle_row = ws.append(subtitles)
subtitle_cells = ws['A2:S2']
for row in subtitle_cells:
    for c in row:
        c.font = subtitle_font

for column in ws.columns:
    max_length = 0
    col = column[1].column_letter # Get the column letter (e.g., 'A', 'B')
    for cell in column:
        if cell.value is not None:
            curr_length = len(str(cell.value))
            if curr_length > max_length:
                max_length = curr_length
    
    # Add padding to the width
    adjusted_width = (max_length + 2) * 1.2 
    ws.column_dimensions[col].width = adjusted_width

ws.row_dimensions[1].height = 24

# wip
cliente_rows = {'nombre':'juan'}
for k,v in cliente_rows.items():
    for r in ws.iter_rows(min_row=3,min_col=1):
        for c in r:
            c = v

# Save the file

# opción 1
# with NamedTemporaryFile() as tmp:
#         wb.save(tmp.name)
#         tmp.seek(0)
#         stream = tmp.read()

# opción 2
try:
    wb.save('Clientes.xlsx')
except PermissionError:
    raise Http404('Por favor, cierre el archivo antes de confirmar los cambios')