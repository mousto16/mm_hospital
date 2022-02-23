# -*- coding: utf-8 -*-
from odoo import models
import base64
import io

class PatientCardXlsx(models.AbstractModel):
    _name = 'report.mm_hospital.report_patient_id_card_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patients):
        # les textes doivent etre en gras
        bold = workbook.add_format({'bold': True})
        merge_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'yellow'})

        for obj in patients:
            # Titre du pied de page dans excel
            sheet = workbook.add_worksheet(obj.name)
            # fusion de deux colonne
            # Create a format to use in the merged range.

            row = 2
            col = 1

            # la case B doit etre de largeur 12
            sheet.set_column('B:C', 12)

            sheet.merge_range('B2:C3','ID Card', merge_format)

            # insertion de l'image
            row +=1
            if obj.image:
                patient_image = io.BytesIO(base64.b64decode(obj.image))
                sheet.insert_image(row, col, "image.png", {'image_data': patient_image, 'x_scale':0.5, 'y_scale':0.5})
                row +=5

            row +=6
            sheet.write(row, col, 'Name', bold)
            sheet.write(row, col + 1, obj.name)

            row += 1
            sheet.write(row, col, 'Age', bold)
            sheet.write(row, col + 1, obj.age)

            row += 1
            sheet.write(row, col, 'Reference', bold)
            sheet.write(row, col + 1, obj.reference)

            row += 2


