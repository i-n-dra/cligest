import base64
from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.styles import Font, Border, Alignment, Side, PatternFill
from tempfile import NamedTemporaryFile
from django.http import Http404
from django.db.models.query import QuerySet
from django.db.models.base import Model
from datetime import datetime, time
from .aes import AES

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
    right=Side(border_style='thin', color='808080'),
)
ficha_border = Border(
    left=Side(
        border_style='thin',
        color='808080'
    ),
    right=Side(
        border_style='thin',
        color='808080'
    ),
    bottom=Side(
        border_style='thin',
        color='808080'
    ),
    top=Side(
        border_style='thin',
        color='808080'
    )
)

def add_row(run=str, rut=str, claves=list):
    path = 'D:/py_venvs/proyectos/proyecto_integracion/cligest/src/Claves.xlsx'
    msg = []

    # añade a excel
    print(f"cliente (run/rut): {run}, {rut}\nclaves: {claves}")

def exportar_claves_all(claves=QuerySet, key=bytes, aes=AES):
    msg = []

    for obj in claves:
        iv = obj.iv
        run = obj.client.run_rep_legal
        rut = obj.client.run_empresa
        enc_claves = [
            base64.b64decode(obj.unica),
            base64.b64decode(obj.sii),
            base64.b64decode(obj.factura_electronica),
            base64.b64decode(obj.dir_trabajo)
        ]
        dec_claves = []

        for c in enc_claves:
            decrypted = aes.decrypt_cfb(c, iv)
            print("decryption test: ", decrypted, type(decrypted))
            decrypted = str(decrypted).removeprefix("b'").removesuffix("'")
            dec_claves.append(decrypted)
        add_row(run, rut, dec_claves)
    
    if decrypted:
        msg.append('Se ha creado "Claves.xlsx" exitosamente')
    return msg
    return None

def exportar_clave(client=Model, key=str, iv=str):
    print(
        "client: ", client,
        "key: ", key,
        "iv: ", iv
    )

    enc_unica = client.unica
    enc_sii = client.sii
    enc_fac = client.factura_electronica
    enc_dir = client.dir_trabajo
    claves = [
        enc_unica,
        enc_sii,
        enc_fac,
        enc_dir
    ]

    for c in claves:
        str_clave = AES(key).decrypt_cfb(c, iv).decode('utf-8')
        print("str_clave: ",str_clave)
    
    msg = "funcionó ????"
    return msg

def create_file(wb=Workbook):
    # grab the active worksheet
    ws = wb.active
    ws.title = "CLAVES"
    ws.freeze_panes = 'A2' # freeze top rows

    cat1 = ws['E1:E2']
    for row in cat1:
        for cell in row:
            cell.border = thick_border

    subtitles = [
        'Cliente',
        'Única',
        'S.I.I.',
        'Factura Electrónica',
        'Dirección de Trabajo',
    ]

    subt_index = 0
    subtitle_cells = ws['A1:E2']
    for row in subtitle_cells:
        for c in row:
            c.value = subtitles[subt_index]
            c.font = subtitle_font
            c.fill = PatternFill("solid", fgColor="DCE6F1")
            subt_index +=1
    
    return