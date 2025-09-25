from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.styles import Font, Border, Alignment, Side
from openpyxl.worksheet.dimensions import Dimension, RowDimension, ColumnDimension
from tempfile import NamedTemporaryFile
from django.http import Http404
from django.db.models.query import QuerySet

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

def exportar_clientes_main(clientes=QuerySet):
    path = 'D:/py_venvs/proyectos/proyecto_integracion/cligest/FichasClientes.xlsx'
    try:
        wb = load_workbook(path)
    except FileNotFoundError:
        msg = 'No se encontró el archivo "FichasClientes.xlsx" en el directorio, se ha creado uno nuevo'
        wb = Workbook(write_only=False)
        create_file(wb)

    # grab the active worksheet
    ws = wb.active

    # agregar clientes
    # falta probar con mas de uno xd
    n_row = 3
    while n_row<(clientes.__len__())+3:
        for c in clientes.all():
            print(f'ingresando cliente: {c.id}')
            ws.cell(
                n_row,
                column = 1,
                value = c.nombre_rep_legal
            )
            ws.cell(
                n_row,
                2,
                c.last_name_1_rep_legal
            )
            ws.cell(
                n_row,
                3,
                c.last_name_2_rep_legal
            )
            ws.cell(
                n_row,
                4,
                c.razon_social
            )
            ws.cell(
                n_row,
                5,
                c.nombre_fantasia
            )
            ws.cell(
                n_row,
                6,
                c.run_rep_legal
            )
            ws.cell(
                n_row,
                7,
                c.run_empresa
            )
            ws.cell(
                n_row,
                8,
                c.tipo_empresa
            )
            ws.cell(
                n_row,
                9,
                str(c.reg_tributario)
            )
            ws.cell(
                n_row,
                10,
                c.giro_rubro
            )
            ws.cell(
                n_row,
                11,
                c.codigo_sii.code
            )
            ws.cell(
                n_row,
                12,
                str(c.tipo_contabilidad)
            )
            ws.cell(
                n_row,
                13,
                c.cuenta_corriente
            )
            ws.cell(
                n_row,
                14,
                c.n_cuenta_corriente
            )
            ws.cell(
                n_row,
                15,
                c.email
            )
            ws.cell(
                n_row,
                16,
                c.phone_number
            )
            ws.cell(
                n_row,
                17,
                str(c.region)
            )
            ws.cell(
                n_row,
                18,
                str(c.comuna)
            )
            ws.cell(
                n_row,
                19,
                c.address
            )

            n_row += 1

    for column in ws.columns:
        max_length = 0
        col = column[1].column_letter # Get the column letter (e.g., 'A', 'B')
        for cell in column:
            if cell.value is not None:
                curr_length = len(str(cell.value))
                if curr_length > max_length and max_length < 80:
                    max_length = curr_length

        # Add padding to the width
        adjusted_width = (max_length + 2) * 1.2 
        ws.column_dimensions[col].width = adjusted_width

    ws.row_dimensions[1].height = 24

    # Save the file

    # opción 1
    # with NamedTemporaryFile() as tmp:
    #         wb.save(tmp.name)
    #         tmp.seek(0)
    #         stream = tmp.read()

    # opción 2
    try:
        wb.save('FichasClientes.xlsx') 
        # + guardar una copia en el escritorio?
        if not msg:
            msg = 'Se ha creado "FichasClientes.xlsx" exitosamente'
            return msg
    except PermissionError:
        raise Http404('Por favor, cierre el archivo antes de confirmar los cambios')

def create_file(wb):
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
    ws.append(subtitles)
    subtitle_cells = ws['A2:S2']
    for row in subtitle_cells:
        for c in row:
            c.font = subtitle_font