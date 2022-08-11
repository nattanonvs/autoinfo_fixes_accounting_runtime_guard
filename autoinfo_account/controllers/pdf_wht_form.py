# coding: utf-8
import io
import os
import re
from odoo import http
from odoo.http import request
from PyPDF2 import PdfFileWriter, PdfFileReader
from odoo.addons.dtr_common import bahttext as bht
from odoo import api, fields, models, _
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from odoo.addons.dtr_taxation.controllers import pdf
from odoo.addons.web.controllers.main import serialize_exception, content_disposition
from odoo.addons.dtr_taxation.controllers.pdf_wht_form import _render_seq, _render_grid

def get_print_by(wht):
    employee_ids = request.env.user.employee_ids.filtered(lambda x: x.company_id.id == wht.company_id.id or not x.company_id)
    if employee_ids:
        return employee_ids[0].name
    return ''

def gen_wht_form(wht):
    # create a mask PDF with Reportlab
    packet = io.BytesIO()
    can = canvas.Canvas(packet)

    # _render_grid(can)
    can.setFont('TH Sarabun New Bold', 28)
    can.drawRightString(19.5 * cm, 28.6 * cm, 'Original')

    # wht seq number
    can.setFont('TH Sarabun New', 9)
    can.drawRightString(19.9 * cm, 27.6 * cm, wht.name_book)
    can.drawRightString(19 * cm, 27.1 * cm, wht.name_seq)

    # vat number
    vat = wht.company_id.vat if wht.company_id.vat else '0000000000000'
    can.setFont('TH Sarabun New', 20)
    if len(vat) == 10:
        _render_seq(can, x=15.00, y=25.76, series=[vat[0], vat[1:5], vat[5:9], vat[9]], adjs=[-0.03, 0, 0])
    if len(vat) >= 13:
        _render_seq(can, x=13.45, y=26.35, series=[vat[0], vat[1:5], vat[5:10], vat[10:12], vat[12]])
    tid = wht.payee_tax_id
    if len(tid) == 10:
        _render_seq(can, x=15.00, y=23.25, series=[tid[0], tid[1:5], tid[5:9], tid[9]], adjs=[-0.03])
    if len(tid) >= 13:
        _render_seq(can, x=13.45, y=23.92, series=[tid[0], tid[1:5], tid[5:10], tid[10:12], tid[12]])
    c = wht.company_id
    can.setFont('TH Sarabun New', 12)
    can.drawString(1.8 * cm, 25.8 * cm, c.name)
    can.drawString(1.9 * cm, 23.25 * cm, wht.payee_name)
    addr_c = c.get_tax_address_line()
    addr_p = u'{0}{1}{2}'.format(
        wht.street + ' ' if wht.street else '',
        wht.street2 + ' ' if wht.street2 else '',
        wht.city + ' ' if wht.city else '')
    can.drawString(2 * cm, 24.95 * cm, addr_c)
    can.drawString(2.1 * cm, 22.3 * cm, addr_p)

    can.setFont('TH Sarabun New', 18)
    tax_type_xy = {
        u'1': (7.48*cm, 21.3*cm),
        # u'1AS': (10.22*cm, 21.3*cm),
        u'2': (14.02*cm, 21.3*cm),
        # u'2A': (7.48*cm, 20.65*cm),
        # u'3A': (10.22*cm, 20.65*cm),
        u'3': (16.75 * cm, 21.3 * cm),
        u'53': (14.02 * cm, 20.65 * cm),
    }
    loc = tax_type_xy[wht.tax_type]
    if loc:
        can.drawString(loc[0], loc[1], 'X')
    can.drawString(3 * cm, 4.26 * cm, 'X')
    pay_date_pos_x = 12.9 * cm
    tax_con_x = [17.1 * cm, 19.6 * cm]
    tax_con6_x = [17.0 * cm, 19.5 * cm]
    tax_con_y = {
        '1': 18.9 * cm,
        '2': 18.4 * cm,
        '3': 17.9 * cm,
        '4A': 17.4 * cm,
        '4B11': 15.3 * cm,
        '4B12': 14.8 * cm,
        '4B13': 14.26 * cm,
        '4B14': 13.78 * cm,
        '4B21': 12.75 * cm,
        '4B22': 11.73 * cm,
        '4B23': 10.71 * cm,
        '4B24': 10.15 * cm,
        '4B25': 9.68 * cm,
        '5': 7.65 * cm,
        '6': 7.15 * cm,
        '7': 8.15 * cm,
    }

    can.setFont('TH Sarabun New', 12)
    if wht.tax_condition == '4B14' and wht.income_type1:
        can.drawString(5.8 * cm, 13.75 * cm, wht.income_type1)
    elif wht.tax_condition2 == '4B14' and wht.income_type2:
        can.drawString(5.8 * cm, 13.75 * cm, wht.income_type2)
    elif wht.tax_condition3 == '4B14' and wht.income_type3:
        can.drawString(5.8 * cm, 13.75 * cm, wht.income_type3)

    if wht.tax_condition == '4B25' and wht.income_type1:
        can.drawString(5.2 * cm, 9.65 * cm, wht.income_type1)
    elif wht.tax_condition2 == '4B25' and wht.income_type2:
        can.drawString(5.2 * cm, 9.65 * cm, wht.income_type2)
    elif wht.tax_condition3 == '4B25' and wht.income_type3:
        can.drawString(5.2 * cm, 9.65 * cm, wht.income_type3)

    income_type = ''
    if wht.tax_condition == '6' and wht.income_type1:
        income_type += ', ' + wht.income_type1
    if wht.tax_condition2 == '6' and wht.income_type2:
        income_type += ', ' + wht.income_type2
    if wht.tax_condition3 == '6' and wht.income_type3:
        income_type += ', ' + wht.income_type3
    if income_type:
        can.drawString(3.3 * cm, 7.1 * cm, income_type[2:])

    cond5_count = 0
    cond6_count = 0
    cond5_pos_x1 = [0.35 * cm, 0.95 * cm, 1.55 * cm]
    cond5_pos_x2 = [0, 0.6 * cm, 1.2 * cm]
    cond6_pos_x2 = [0, 0.2 * cm, 0.4 * cm]
    can.setFont('TH Sarabun New', 11)
    if wht.tax_condition:
        tax_con_pos_y = tax_con_y[wht.tax_condition]
        if wht.tax_condition == '5':
            can.drawString(pay_date_pos_x - (1 * cm), tax_con_pos_y + cond5_pos_x1[cond5_count], wht.income_type1)
            can.drawCentredString(pay_date_pos_x, tax_con_pos_y, wht.pay_date_th)
            can.drawRightString(tax_con_x[0], tax_con_pos_y, '{0:,.2f}'.format(wht.pay_amount1))
            can.drawRightString(tax_con_x[1], tax_con_pos_y, '{0:,.2f}'.format(wht.wht_amount1))
            cond5_count += 1
        elif wht.tax_condition == '6':
            can.setFont('TH Sarabun New', 8)
            can.drawCentredString(pay_date_pos_x, tax_con_pos_y, wht.pay_date_th)
            can.drawRightString(tax_con6_x[0], tax_con_pos_y, '{0:,.2f}'.format(wht.pay_amount1))
            can.drawRightString(tax_con6_x[1], tax_con_pos_y, '{0:,.2f}'.format(wht.wht_amount1))
            cond6_count += 1
        else:
            can.drawCentredString(pay_date_pos_x, tax_con_pos_y, wht.pay_date_th)
            can.drawRightString(tax_con_x[0], tax_con_pos_y, '{0:,.2f}'.format(wht.pay_amount1))
            can.drawRightString(tax_con_x[1], tax_con_pos_y, '{0:,.2f}'.format(wht.wht_amount1))
    if wht.tax_condition2 and wht.pay_amount2 != 0:
        tax_con_pos_y = tax_con_y[wht.tax_condition2]
        if wht.tax_condition2 == '5':
            can.drawString(pay_date_pos_x - (1 * cm), tax_con_pos_y + cond5_pos_x1[cond5_count], wht.income_type2)
            can.drawCentredString(pay_date_pos_x, tax_con_pos_y + cond5_pos_x2[cond5_count], wht.pay_date_th)
            can.drawRightString(tax_con_x[0], tax_con_pos_y + cond5_pos_x2[cond5_count], '{0:,.2f}'.format(wht.pay_amount2))
            can.drawRightString(tax_con_x[1], tax_con_pos_y + cond5_pos_x2[cond5_count], '{0:,.2f}'.format(wht.wht_amount2))
            cond5_count += 1
        elif wht.tax_condition == '6':
            can.setFont('TH Sarabun New', 8)
            can.drawCentredString(pay_date_pos_x, tax_con_pos_y + cond6_pos_x2[cond6_count], wht.pay_date_th)
            can.drawRightString(tax_con6_x[0], tax_con_pos_y + cond6_pos_x2[cond6_count], '{0:,.2f}'.format(wht.pay_amount2))
            can.drawRightString(tax_con6_x[1], tax_con_pos_y + cond6_pos_x2[cond6_count], '{0:,.2f}'.format(wht.wht_amount2))
            cond6_count += 1
        else:
            can.drawCentredString(pay_date_pos_x, tax_con_pos_y, wht.pay_date_th)
            can.drawRightString(tax_con_x[0], tax_con_pos_y, '{0:,.2f}'.format(wht.pay_amount2))
            can.drawRightString(tax_con_x[1], tax_con_pos_y, '{0:,.2f}'.format(wht.wht_amount2))
    if wht.tax_condition3 and wht.pay_amount3 != 0:
        tax_con_pos_y = tax_con_y[wht.tax_condition3]
        if wht.tax_condition3 == '5':
            can.drawString(pay_date_pos_x - (1 * cm), tax_con_pos_y + cond5_pos_x1[cond5_count], wht.income_type3)
            can.drawCentredString(pay_date_pos_x, tax_con_pos_y + cond5_pos_x2[cond5_count], wht.pay_date_th)
            can.drawRightString(tax_con_x[0], tax_con_pos_y + cond5_pos_x2[cond5_count], '{0:,.2f}'.format(wht.pay_amount3))
            can.drawRightString(tax_con_x[1], tax_con_pos_y + cond5_pos_x2[cond5_count], '{0:,.2f}'.format(wht.wht_amount3))
            cond5_count += 1
        elif wht.tax_condition == '6':
            can.setFont('TH Sarabun New', 8)
            can.drawCentredString(pay_date_pos_x, tax_con_pos_y + cond6_pos_x2[cond6_count], wht.pay_date_th)
            can.drawRightString(tax_con6_x[0], tax_con_pos_y + cond6_pos_x2[cond6_count], '{0:,.2f}'.format(wht.pay_amount3))
            can.drawRightString(tax_con6_x[1], tax_con_pos_y + cond6_pos_x2[cond6_count], '{0:,.2f}'.format(wht.wht_amount3))
        else:
            can.drawCentredString(pay_date_pos_x, tax_con_pos_y, wht.pay_date_th)
            can.drawRightString(tax_con_x[0], tax_con_pos_y, '{0:,.2f}'.format(wht.pay_amount3))
            can.drawRightString(tax_con_x[1], tax_con_pos_y, '{0:,.2f}'.format(wht.wht_amount3))

    can.setFont('TH Sarabun New', 11)
    can.drawRightString(tax_con_x[0], 6.4 * cm, '{0:,.2f}'.format(wht.pay_amount))
    can.drawRightString(tax_con_x[1], 6.4 * cm, '{0:,.2f}'.format(wht.wht_amount))

    can.setFont('TH Sarabun New', 16)
    can.drawString(6.6 * cm, 5.7 * cm, bht.bahttext(wht.wht_amount))

    if wht.tax_type == '1':
        can.setFont('TH Sarabun New', 11)
        can.drawString(13.1 * cm, 5.1 * cm, '{0:,.2f}'.format(wht.sso_amount))
        can.drawString(17.7 * cm, 5.1 * cm, '{0:,.2f}'.format(wht.pvf_amount))

    can.drawString(12.5 * cm, 3.1 * cm, get_print_by(wht))
    date_today = fields.Date.from_string(wht.pay_date)
    year_th = int(date_today.year)+543
    can.drawString(12 * cm, 2.7 * cm, str(date_today.day))
    can.drawString(14 * cm, 2.7 * cm, str(date_today.month))
    can.drawString(15.5 * cm, 2.7 * cm, str(year_th))

    can.save()
    # move to the beginning of the StringIO buffer
    packet.seek(0)
    return PdfFileReader(packet)

def gen_wht_form_without_date(wht):
    # create a mask PDF with Reportlab
    packet = io.BytesIO()
    can = canvas.Canvas(packet)

    can.setFont('TH Sarabun New Bold', 28)
    can.drawRightString(19.5 * cm, 28.6 * cm, 'Original')

    # _render_grid(can)

    # wht seq number
    can.setFont('TH Sarabun New', 9)
    can.drawRightString(19.9 * cm, 27.6 * cm, wht.name_book)
    can.drawRightString(19 * cm, 27.1 * cm, wht.name_seq)

    # vat number
    vat = wht.company_id.vat if wht.company_id.vat else '0000000000000'
    can.setFont('TH Sarabun New', 20)
    if len(vat) == 10:
        _render_seq(can, x=15.00, y=25.76, series=[vat[0], vat[1:5], vat[5:9], vat[9]], adjs=[-0.03, 0, 0])
    if len(vat) >= 13:
        _render_seq(can, x=13.45, y=26.35, series=[vat[0], vat[1:5], vat[5:10], vat[10:12], vat[12]])
    tid = wht.payee_tax_id
    if len(tid) == 10:
        _render_seq(can, x=15.00, y=23.25, series=[tid[0], tid[1:5], tid[5:9], tid[9]], adjs=[-0.03])
    if len(tid) >= 13:
        _render_seq(can, x=13.45, y=23.92, series=[tid[0], tid[1:5], tid[5:10], tid[10:12], tid[12]])
    c = wht.company_id
    can.setFont('TH Sarabun New', 12)
    can.drawString(1.8 * cm, 25.8 * cm, c.name)
    can.drawString(1.9 * cm, 23.25 * cm, wht.payee_name)
    addr_c = c.get_tax_address_line()
    addr_p = u'{0}{1}{2}'.format(
        wht.street + ' ' if wht.street else '',
        wht.street2 + ' ' if wht.street2 else '',
        wht.city + ' ' if wht.city else '')
    can.drawString(2 * cm, 24.95 * cm, addr_c)
    can.drawString(2.1 * cm, 22.3 * cm, addr_p)

    can.setFont('TH Sarabun New', 18)
    tax_type_xy = {
        u'1': (7.48*cm, 21.3*cm),
        # u'1AS': (10.22*cm, 21.3*cm),
        # u'2': (14.02*cm, 21.3*cm),
        # u'2A': (7.48*cm, 20.65*cm),
        # u'3A': (10.22*cm, 20.65*cm),
        u'3': (16.75 * cm, 21.3 * cm),
        u'53': (14.02 * cm, 20.65 * cm),
    }
    loc = tax_type_xy[wht.tax_type]
    if loc:
        can.drawString(loc[0], loc[1], 'X')
    can.drawString(3 * cm, 4.26 * cm, 'X')
    pay_date_pos_x = 12.9 * cm
    tax_con_x = [17.1 * cm, 19.6 * cm]
    tax_con6_x = [17.0 * cm, 19.5 * cm]
    tax_con_y = {
        '1': 18.9 * cm,
        '2': 18.4 * cm,
        '3': 17.9 * cm,
        '4A': 17.4 * cm,
        '4B11': 15.3 * cm,
        '4B12': 14.8 * cm,
        '4B13': 14.26 * cm,
        '4B14': 13.78 * cm,
        '4B21': 12.75 * cm,
        '4B22': 11.73 * cm,
        '4B23': 10.71 * cm,
        '4B24': 10.15 * cm,
        '4B25': 9.68 * cm,
        '5': 7.65 * cm,
        '6': 7.15 * cm,
    }

    can.setFont('TH Sarabun New', 12)
    if wht.tax_condition == '4B14' and wht.income_type1:
        can.drawString(5.8 * cm, 13.75 * cm, wht.income_type1)
    elif wht.tax_condition2 == '4B14' and wht.income_type2:
        can.drawString(5.8 * cm, 13.75 * cm, wht.income_type2)
    elif wht.tax_condition3 == '4B14' and wht.income_type3:
        can.drawString(5.8 * cm, 13.75 * cm, wht.income_type3)

    if wht.tax_condition == '4B25' and wht.income_type1:
        can.drawString(5.2 * cm, 9.65 * cm, wht.income_type1)
    elif wht.tax_condition2 == '4B25' and wht.income_type2:
        can.drawString(5.2 * cm, 9.65 * cm, wht.income_type2)
    elif wht.tax_condition3 == '4B25' and wht.income_type3:
        can.drawString(5.2 * cm, 9.65 * cm, wht.income_type3)

    income_type = ''
    if wht.tax_condition == '6' and wht.income_type1:
        income_type += ', ' + wht.income_type1
    if wht.tax_condition2 == '6' and wht.income_type2:
        income_type += ', ' + wht.income_type2
    if wht.tax_condition3 == '6' and wht.income_type3:
        income_type += ', ' + wht.income_type3
    if income_type:
        can.drawString(3.3 * cm, 7.1 * cm, income_type[2:])

    cond5_count = 0
    cond6_count = 0
    cond5_pos_x1 = [0.35 * cm, 0.95 * cm, 1.55 * cm]
    cond5_pos_x2 = [0, 0.6 * cm, 1.2 * cm]
    cond6_pos_x2 = [0, 0.2 * cm, 0.4 * cm]
    can.setFont('TH Sarabun New', 11)
    if wht.tax_condition:
        tax_con_pos_y = tax_con_y[wht.tax_condition]
        if wht.tax_condition == '5':
            can.drawString(pay_date_pos_x - (1 * cm), tax_con_pos_y + cond5_pos_x1[cond5_count], wht.income_type1)
            can.drawRightString(tax_con_x[0], tax_con_pos_y, '{0:,.2f}'.format(wht.pay_amount1))
            can.drawRightString(tax_con_x[1], tax_con_pos_y, '{0:,.2f}'.format(wht.wht_amount1))
            cond5_count += 1
        elif wht.tax_condition == '6':
            can.setFont('TH Sarabun New', 8)
            can.drawRightString(tax_con6_x[0], tax_con_pos_y, '{0:,.2f}'.format(wht.pay_amount1))
            can.drawRightString(tax_con6_x[1], tax_con_pos_y, '{0:,.2f}'.format(wht.wht_amount1))
            cond6_count += 1
        else:
            can.drawRightString(tax_con_x[0], tax_con_pos_y, '{0:,.2f}'.format(wht.pay_amount1))
            can.drawRightString(tax_con_x[1], tax_con_pos_y, '{0:,.2f}'.format(wht.wht_amount1))
    if wht.tax_condition2 and wht.pay_amount2 != 0:
        tax_con_pos_y = tax_con_y[wht.tax_condition2]
        if wht.tax_condition2 == '5':
            can.drawString(pay_date_pos_x - (1 * cm), tax_con_pos_y + cond5_pos_x1[cond5_count], wht.income_type2)
            can.drawRightString(tax_con_x[0], tax_con_pos_y + cond5_pos_x2[cond5_count], '{0:,.2f}'.format(wht.pay_amount2))
            can.drawRightString(tax_con_x[1], tax_con_pos_y + cond5_pos_x2[cond5_count], '{0:,.2f}'.format(wht.wht_amount2))
            cond5_count += 1
        elif wht.tax_condition == '6':
            can.setFont('TH Sarabun New', 8)
            can.drawRightString(tax_con6_x[0], tax_con_pos_y + cond6_pos_x2[cond6_count], '{0:,.2f}'.format(wht.pay_amount2))
            can.drawRightString(tax_con6_x[1], tax_con_pos_y + cond6_pos_x2[cond6_count], '{0:,.2f}'.format(wht.wht_amount2))
            cond6_count += 1
        else:
            can.drawRightString(tax_con_x[0], tax_con_pos_y, '{0:,.2f}'.format(wht.pay_amount2))
            can.drawRightString(tax_con_x[1], tax_con_pos_y, '{0:,.2f}'.format(wht.wht_amount2))
    if wht.tax_condition3 and wht.pay_amount3 != 0:
        tax_con_pos_y = tax_con_y[wht.tax_condition3]
        if wht.tax_condition3 == '5':
            can.drawString(pay_date_pos_x - (1 * cm), tax_con_pos_y + cond5_pos_x1[cond5_count], wht.income_type3)
            can.drawRightString(tax_con_x[0], tax_con_pos_y + cond5_pos_x2[cond5_count], '{0:,.2f}'.format(wht.pay_amount3))
            can.drawRightString(tax_con_x[1], tax_con_pos_y + cond5_pos_x2[cond5_count], '{0:,.2f}'.format(wht.wht_amount3))
            cond5_count += 1
        elif wht.tax_condition == '6':
            can.setFont('TH Sarabun New', 8)
            can.drawRightString(tax_con6_x[0], tax_con_pos_y + cond6_pos_x2[cond6_count], '{0:,.2f}'.format(wht.pay_amount3))
            can.drawRightString(tax_con6_x[1], tax_con_pos_y + cond6_pos_x2[cond6_count], '{0:,.2f}'.format(wht.wht_amount3))
        else:
            can.drawRightString(tax_con_x[0], tax_con_pos_y, '{0:,.2f}'.format(wht.pay_amount3))
            can.drawRightString(tax_con_x[1], tax_con_pos_y, '{0:,.2f}'.format(wht.wht_amount3))

    can.setFont('TH Sarabun New', 11)
    can.drawRightString(tax_con_x[0], 6.4 * cm, '{0:,.2f}'.format(wht.pay_amount))
    can.drawRightString(tax_con_x[1], 6.4 * cm, '{0:,.2f}'.format(wht.wht_amount))

    can.setFont('TH Sarabun New', 16)
    can.drawString(6.6 * cm, 5.7 * cm, bht.bahttext(wht.wht_amount))

    if wht.tax_type == '1':
        can.setFont('TH Sarabun New', 11)
        can.drawString(13.1 * cm, 5.1 * cm, '{0:,.2f}'.format(wht.sso_amount))
        can.drawString(17.7 * cm, 5.1 * cm, '{0:,.2f}'.format(wht.pvf_amount))

    can.drawString(12.5 * cm, 3.1 * cm, get_print_by(wht))
    date_today = fields.Date.from_string(wht.pay_date)
    year_th = int(date_today.year)+543
    can.drawString(12 * cm, 2.7 * cm, str(date_today.day))
    can.drawString(14 * cm, 2.7 * cm, str(date_today.month))
    can.drawString(15.5 * cm, 2.7 * cm, str(year_th))

    can.save()
    # move to the beginning of the StringIO buffer
    packet.seek(0)
    return PdfFileReader(packet)

def gen_wht_form_copy(wht):
    # create a mask PDF with Reportlab
    packet = io.BytesIO()
    can = canvas.Canvas(packet)

    # _render_grid(can)
    can.setFont('TH Sarabun New Bold', 28)
    can.drawRightString(19.5 * cm, 28.6 * cm, 'Copy')

    # wht seq number
    can.setFont('TH Sarabun New', 9)
    can.drawRightString(19.9 * cm, 27.6 * cm, wht.name_book)
    can.drawRightString(19 * cm, 27.1 * cm, wht.name_seq)

    # vat number
    vat = wht.company_id.vat if wht.company_id.vat else '0000000000000'
    can.setFont('TH Sarabun New', 20)
    if len(vat) == 10:
        _render_seq(can, x=15.00, y=25.76, series=[vat[0], vat[1:5], vat[5:9], vat[9]], adjs=[-0.03, 0, 0])
    if len(vat) >= 13:
        _render_seq(can, x=13.45, y=26.35, series=[vat[0], vat[1:5], vat[5:10], vat[10:12], vat[12]])
    tid = wht.payee_tax_id
    if len(tid) == 10:
        _render_seq(can, x=15.00, y=23.25, series=[tid[0], tid[1:5], tid[5:9], tid[9]], adjs=[-0.03])
    if len(tid) >= 13:
        _render_seq(can, x=13.45, y=23.92, series=[tid[0], tid[1:5], tid[5:10], tid[10:12], tid[12]])
    c = wht.company_id
    can.setFont('TH Sarabun New', 12)
    can.drawString(1.8 * cm, 25.8 * cm, c.name)
    can.drawString(1.9 * cm, 23.25 * cm, wht.payee_name)
    addr_c = c.get_tax_address_line()
    addr_p = u'{0}{1}{2}'.format(
        wht.street + ' ' if wht.street else '',
        wht.street2 + ' ' if wht.street2 else '',
        wht.city + ' ' if wht.city else '')
    can.drawString(2 * cm, 24.95 * cm, addr_c)
    can.drawString(2.1 * cm, 22.3 * cm, addr_p)

    can.setFont('TH Sarabun New', 18)
    tax_type_xy = {
        u'1': (7.48*cm, 21.3*cm),
        # u'1AS': (10.22*cm, 21.3*cm),
        u'2': (14.02*cm, 21.3*cm),
        # u'2A': (7.48*cm, 20.65*cm),
        # u'3A': (10.22*cm, 20.65*cm),
        u'3': (16.75 * cm, 21.3 * cm),
        u'53': (14.02 * cm, 20.65 * cm),
    }
    loc = tax_type_xy[wht.tax_type]
    if loc:
        can.drawString(loc[0], loc[1], 'X')
    can.drawString(3 * cm, 4.26 * cm, 'X')
    pay_date_pos_x = 12.9 * cm
    tax_con_x = [17.1 * cm, 19.6 * cm]
    tax_con6_x = [17.0 * cm, 19.5 * cm]
    tax_con_y = {
        '1': 18.9 * cm,
        '2': 18.4 * cm,
        '3': 17.9 * cm,
        '4A': 17.4 * cm,
        '4B11': 15.3 * cm,
        '4B12': 14.8 * cm,
        '4B13': 14.26 * cm,
        '4B14': 13.78 * cm,
        '4B21': 12.75 * cm,
        '4B22': 11.73 * cm,
        '4B23': 10.71 * cm,
        '4B24': 10.15 * cm,
        '4B25': 9.68 * cm,
        '5': 7.65 * cm,
        '6': 7.15 * cm,
        '7': 8.15 * cm,
    }

    can.setFont('TH Sarabun New', 12)
    if wht.tax_condition == '4B14' and wht.income_type1:
        can.drawString(5.8 * cm, 13.75 * cm, wht.income_type1)
    elif wht.tax_condition2 == '4B14' and wht.income_type2:
        can.drawString(5.8 * cm, 13.75 * cm, wht.income_type2)
    elif wht.tax_condition3 == '4B14' and wht.income_type3:
        can.drawString(5.8 * cm, 13.75 * cm, wht.income_type3)

    if wht.tax_condition == '4B25' and wht.income_type1:
        can.drawString(5.2 * cm, 9.65 * cm, wht.income_type1)
    elif wht.tax_condition2 == '4B25' and wht.income_type2:
        can.drawString(5.2 * cm, 9.65 * cm, wht.income_type2)
    elif wht.tax_condition3 == '4B25' and wht.income_type3:
        can.drawString(5.2 * cm, 9.65 * cm, wht.income_type3)

    income_type = ''
    if wht.tax_condition == '6' and wht.income_type1:
        income_type += ', ' + wht.income_type1
    if wht.tax_condition2 == '6' and wht.income_type2:
        income_type += ', ' + wht.income_type2
    if wht.tax_condition3 == '6' and wht.income_type3:
        income_type += ', ' + wht.income_type3
    if income_type:
        can.drawString(3.3 * cm, 7.1 * cm, income_type[2:])

    cond5_count = 0
    cond6_count = 0
    cond5_pos_x1 = [0.35 * cm, 0.95 * cm, 1.55 * cm]
    cond5_pos_x2 = [0, 0.6 * cm, 1.2 * cm]
    cond6_pos_x2 = [0, 0.2 * cm, 0.4 * cm]
    can.setFont('TH Sarabun New', 11)
    if wht.tax_condition:
        tax_con_pos_y = tax_con_y[wht.tax_condition]
        if wht.tax_condition == '5':
            can.drawString(pay_date_pos_x - (1 * cm), tax_con_pos_y + cond5_pos_x1[cond5_count], wht.income_type1)
            can.drawCentredString(pay_date_pos_x, tax_con_pos_y, wht.pay_date_th)
            can.drawRightString(tax_con_x[0], tax_con_pos_y, '{0:,.2f}'.format(wht.pay_amount1))
            can.drawRightString(tax_con_x[1], tax_con_pos_y, '{0:,.2f}'.format(wht.wht_amount1))
            cond5_count += 1
        elif wht.tax_condition == '6':
            can.setFont('TH Sarabun New', 8)
            can.drawCentredString(pay_date_pos_x, tax_con_pos_y, wht.pay_date_th)
            can.drawRightString(tax_con6_x[0], tax_con_pos_y, '{0:,.2f}'.format(wht.pay_amount1))
            can.drawRightString(tax_con6_x[1], tax_con_pos_y, '{0:,.2f}'.format(wht.wht_amount1))
            cond6_count += 1
        else:
            can.drawCentredString(pay_date_pos_x, tax_con_pos_y, wht.pay_date_th)
            can.drawRightString(tax_con_x[0], tax_con_pos_y, '{0:,.2f}'.format(wht.pay_amount1))
            can.drawRightString(tax_con_x[1], tax_con_pos_y, '{0:,.2f}'.format(wht.wht_amount1))
    if wht.tax_condition2 and wht.pay_amount2 != 0:
        tax_con_pos_y = tax_con_y[wht.tax_condition2]
        if wht.tax_condition2 == '5':
            can.drawString(pay_date_pos_x - (1 * cm), tax_con_pos_y + cond5_pos_x1[cond5_count], wht.income_type2)
            can.drawCentredString(pay_date_pos_x, tax_con_pos_y + cond5_pos_x2[cond5_count], wht.pay_date_th)
            can.drawRightString(tax_con_x[0], tax_con_pos_y + cond5_pos_x2[cond5_count], '{0:,.2f}'.format(wht.pay_amount2))
            can.drawRightString(tax_con_x[1], tax_con_pos_y + cond5_pos_x2[cond5_count], '{0:,.2f}'.format(wht.wht_amount2))
            cond5_count += 1
        elif wht.tax_condition == '6':
            can.setFont('TH Sarabun New', 8)
            can.drawCentredString(pay_date_pos_x, tax_con_pos_y + cond6_pos_x2[cond6_count], wht.pay_date_th)
            can.drawRightString(tax_con6_x[0], tax_con_pos_y + cond6_pos_x2[cond6_count], '{0:,.2f}'.format(wht.pay_amount2))
            can.drawRightString(tax_con6_x[1], tax_con_pos_y + cond6_pos_x2[cond6_count], '{0:,.2f}'.format(wht.wht_amount2))
            cond6_count += 1
        else:
            can.drawCentredString(pay_date_pos_x, tax_con_pos_y, wht.pay_date_th)
            can.drawRightString(tax_con_x[0], tax_con_pos_y, '{0:,.2f}'.format(wht.pay_amount2))
            can.drawRightString(tax_con_x[1], tax_con_pos_y, '{0:,.2f}'.format(wht.wht_amount2))
    if wht.tax_condition3 and wht.pay_amount3 != 0:
        tax_con_pos_y = tax_con_y[wht.tax_condition3]
        if wht.tax_condition3 == '5':
            can.drawString(pay_date_pos_x - (1 * cm), tax_con_pos_y + cond5_pos_x1[cond5_count], wht.income_type3)
            can.drawCentredString(pay_date_pos_x, tax_con_pos_y + cond5_pos_x2[cond5_count], wht.pay_date_th)
            can.drawRightString(tax_con_x[0], tax_con_pos_y + cond5_pos_x2[cond5_count], '{0:,.2f}'.format(wht.pay_amount3))
            can.drawRightString(tax_con_x[1], tax_con_pos_y + cond5_pos_x2[cond5_count], '{0:,.2f}'.format(wht.wht_amount3))
            cond5_count += 1
        elif wht.tax_condition == '6':
            can.setFont('TH Sarabun New', 8)
            can.drawCentredString(pay_date_pos_x, tax_con_pos_y + cond6_pos_x2[cond6_count], wht.pay_date_th)
            can.drawRightString(tax_con6_x[0], tax_con_pos_y + cond6_pos_x2[cond6_count], '{0:,.2f}'.format(wht.pay_amount3))
            can.drawRightString(tax_con6_x[1], tax_con_pos_y + cond6_pos_x2[cond6_count], '{0:,.2f}'.format(wht.wht_amount3))
        else:
            can.drawCentredString(pay_date_pos_x, tax_con_pos_y, wht.pay_date_th)
            can.drawRightString(tax_con_x[0], tax_con_pos_y, '{0:,.2f}'.format(wht.pay_amount3))
            can.drawRightString(tax_con_x[1], tax_con_pos_y, '{0:,.2f}'.format(wht.wht_amount3))

    can.setFont('TH Sarabun New', 11)
    can.drawRightString(tax_con_x[0], 6.4 * cm, '{0:,.2f}'.format(wht.pay_amount))
    can.drawRightString(tax_con_x[1], 6.4 * cm, '{0:,.2f}'.format(wht.wht_amount))

    can.setFont('TH Sarabun New', 16)
    can.drawString(6.6 * cm, 5.7 * cm, bht.bahttext(wht.wht_amount))

    if wht.tax_type == '1':
        can.setFont('TH Sarabun New', 11)
        can.drawString(13.1 * cm, 5.1 * cm, '{0:,.2f}'.format(wht.sso_amount))
        can.drawString(17.7 * cm, 5.1 * cm, '{0:,.2f}'.format(wht.pvf_amount))

    can.drawString(12.5 * cm, 3.1 * cm, get_print_by(wht))
    date_today = fields.Date.from_string(wht.pay_date)
    year_th = int(date_today.year)+543
    can.drawString(12 * cm, 2.7 * cm, str(date_today.day))
    can.drawString(14 * cm, 2.7 * cm, str(date_today.month))
    can.drawString(15.5 * cm, 2.7 * cm, str(year_th))

    can.save()
    # move to the beginning of the StringIO buffer
    packet.seek(0)
    return PdfFileReader(packet)

def gen_wht_form_without_date_copy(wht):
    # create a mask PDF with Reportlab
    packet = io.BytesIO()
    can = canvas.Canvas(packet)

    can.setFont('TH Sarabun New Bold', 28)
    can.drawRightString(19.5 * cm, 28.6 * cm, 'Copy')

    # _render_grid(can)

    # wht seq number
    can.setFont('TH Sarabun New', 9)
    can.drawRightString(19.9 * cm, 27.6 * cm, wht.name_book)
    can.drawRightString(19 * cm, 27.1 * cm, wht.name_seq)

    # vat number
    vat = wht.company_id.vat if wht.company_id.vat else '0000000000000'
    can.setFont('TH Sarabun New', 20)
    if len(vat) == 10:
        _render_seq(can, x=15.00, y=25.76, series=[vat[0], vat[1:5], vat[5:9], vat[9]], adjs=[-0.03, 0, 0])
    if len(vat) >= 13:
        _render_seq(can, x=13.45, y=26.35, series=[vat[0], vat[1:5], vat[5:10], vat[10:12], vat[12]])
    tid = wht.payee_tax_id
    if len(tid) == 10:
        _render_seq(can, x=15.00, y=23.25, series=[tid[0], tid[1:5], tid[5:9], tid[9]], adjs=[-0.03])
    if len(tid) >= 13:
        _render_seq(can, x=13.45, y=23.92, series=[tid[0], tid[1:5], tid[5:10], tid[10:12], tid[12]])
    c = wht.company_id
    can.setFont('TH Sarabun New', 12)
    can.drawString(1.8 * cm, 25.8 * cm, c.name)
    can.drawString(1.9 * cm, 23.25 * cm, wht.payee_name)
    addr_c = c.get_tax_address_line()
    addr_p = u'{0}{1}{2}'.format(
        wht.street + ' ' if wht.street else '',
        wht.street2 + ' ' if wht.street2 else '',
        wht.city + ' ' if wht.city else '')
    can.drawString(2 * cm, 24.95 * cm, addr_c)
    can.drawString(2.1 * cm, 22.3 * cm, addr_p)

    can.setFont('TH Sarabun New', 18)
    tax_type_xy = {
        u'1': (7.48*cm, 21.3*cm),
        # u'1AS': (10.22*cm, 21.3*cm),
        # u'2': (14.02*cm, 21.3*cm),
        # u'2A': (7.48*cm, 20.65*cm),
        # u'3A': (10.22*cm, 20.65*cm),
        u'3': (16.75 * cm, 21.3 * cm),
        u'53': (14.02 * cm, 20.65 * cm),
    }
    loc = tax_type_xy[wht.tax_type]
    if loc:
        can.drawString(loc[0], loc[1], 'X')
    can.drawString(3 * cm, 4.26 * cm, 'X')
    pay_date_pos_x = 12.9 * cm
    tax_con_x = [17.1 * cm, 19.6 * cm]
    tax_con6_x = [17.0 * cm, 19.5 * cm]
    tax_con_y = {
        '1': 18.9 * cm,
        '2': 18.4 * cm,
        '3': 17.9 * cm,
        '4A': 17.4 * cm,
        '4B11': 15.3 * cm,
        '4B12': 14.8 * cm,
        '4B13': 14.26 * cm,
        '4B14': 13.78 * cm,
        '4B21': 12.75 * cm,
        '4B22': 11.73 * cm,
        '4B23': 10.71 * cm,
        '4B24': 10.15 * cm,
        '4B25': 9.68 * cm,
        '5': 7.65 * cm,
        '6': 7.15 * cm,
    }

    can.setFont('TH Sarabun New', 12)
    if wht.tax_condition == '4B14' and wht.income_type1:
        can.drawString(5.8 * cm, 13.75 * cm, wht.income_type1)
    elif wht.tax_condition2 == '4B14' and wht.income_type2:
        can.drawString(5.8 * cm, 13.75 * cm, wht.income_type2)
    elif wht.tax_condition3 == '4B14' and wht.income_type3:
        can.drawString(5.8 * cm, 13.75 * cm, wht.income_type3)

    if wht.tax_condition == '4B25' and wht.income_type1:
        can.drawString(5.2 * cm, 9.65 * cm, wht.income_type1)
    elif wht.tax_condition2 == '4B25' and wht.income_type2:
        can.drawString(5.2 * cm, 9.65 * cm, wht.income_type2)
    elif wht.tax_condition3 == '4B25' and wht.income_type3:
        can.drawString(5.2 * cm, 9.65 * cm, wht.income_type3)

    income_type = ''
    if wht.tax_condition == '6' and wht.income_type1:
        income_type += ', ' + wht.income_type1
    if wht.tax_condition2 == '6' and wht.income_type2:
        income_type += ', ' + wht.income_type2
    if wht.tax_condition3 == '6' and wht.income_type3:
        income_type += ', ' + wht.income_type3
    if income_type:
        can.drawString(3.3 * cm, 7.1 * cm, income_type[2:])

    cond5_count = 0
    cond6_count = 0
    cond5_pos_x1 = [0.35 * cm, 0.95 * cm, 1.55 * cm]
    cond5_pos_x2 = [0, 0.6 * cm, 1.2 * cm]
    cond6_pos_x2 = [0, 0.2 * cm, 0.4 * cm]
    can.setFont('TH Sarabun New', 11)
    if wht.tax_condition:
        tax_con_pos_y = tax_con_y[wht.tax_condition]
        if wht.tax_condition == '5':
            can.drawString(pay_date_pos_x - (1 * cm), tax_con_pos_y + cond5_pos_x1[cond5_count], wht.income_type1)
            can.drawRightString(tax_con_x[0], tax_con_pos_y, '{0:,.2f}'.format(wht.pay_amount1))
            can.drawRightString(tax_con_x[1], tax_con_pos_y, '{0:,.2f}'.format(wht.wht_amount1))
            cond5_count += 1
        elif wht.tax_condition == '6':
            can.setFont('TH Sarabun New', 8)
            can.drawRightString(tax_con6_x[0], tax_con_pos_y, '{0:,.2f}'.format(wht.pay_amount1))
            can.drawRightString(tax_con6_x[1], tax_con_pos_y, '{0:,.2f}'.format(wht.wht_amount1))
            cond6_count += 1
        else:
            can.drawRightString(tax_con_x[0], tax_con_pos_y, '{0:,.2f}'.format(wht.pay_amount1))
            can.drawRightString(tax_con_x[1], tax_con_pos_y, '{0:,.2f}'.format(wht.wht_amount1))
    if wht.tax_condition2 and wht.pay_amount2 != 0:
        tax_con_pos_y = tax_con_y[wht.tax_condition2]
        if wht.tax_condition2 == '5':
            can.drawString(pay_date_pos_x - (1 * cm), tax_con_pos_y + cond5_pos_x1[cond5_count], wht.income_type2)
            can.drawRightString(tax_con_x[0], tax_con_pos_y + cond5_pos_x2[cond5_count], '{0:,.2f}'.format(wht.pay_amount2))
            can.drawRightString(tax_con_x[1], tax_con_pos_y + cond5_pos_x2[cond5_count], '{0:,.2f}'.format(wht.wht_amount2))
            cond5_count += 1
        elif wht.tax_condition == '6':
            can.setFont('TH Sarabun New', 8)
            can.drawRightString(tax_con6_x[0], tax_con_pos_y + cond6_pos_x2[cond6_count], '{0:,.2f}'.format(wht.pay_amount2))
            can.drawRightString(tax_con6_x[1], tax_con_pos_y + cond6_pos_x2[cond6_count], '{0:,.2f}'.format(wht.wht_amount2))
            cond6_count += 1
        else:
            can.drawRightString(tax_con_x[0], tax_con_pos_y, '{0:,.2f}'.format(wht.pay_amount2))
            can.drawRightString(tax_con_x[1], tax_con_pos_y, '{0:,.2f}'.format(wht.wht_amount2))
    if wht.tax_condition3 and wht.pay_amount3 != 0:
        tax_con_pos_y = tax_con_y[wht.tax_condition3]
        if wht.tax_condition3 == '5':
            can.drawString(pay_date_pos_x - (1 * cm), tax_con_pos_y + cond5_pos_x1[cond5_count], wht.income_type3)
            can.drawRightString(tax_con_x[0], tax_con_pos_y + cond5_pos_x2[cond5_count], '{0:,.2f}'.format(wht.pay_amount3))
            can.drawRightString(tax_con_x[1], tax_con_pos_y + cond5_pos_x2[cond5_count], '{0:,.2f}'.format(wht.wht_amount3))
            cond5_count += 1
        elif wht.tax_condition == '6':
            can.setFont('TH Sarabun New', 8)
            can.drawRightString(tax_con6_x[0], tax_con_pos_y + cond6_pos_x2[cond6_count], '{0:,.2f}'.format(wht.pay_amount3))
            can.drawRightString(tax_con6_x[1], tax_con_pos_y + cond6_pos_x2[cond6_count], '{0:,.2f}'.format(wht.wht_amount3))
        else:
            can.drawRightString(tax_con_x[0], tax_con_pos_y, '{0:,.2f}'.format(wht.pay_amount3))
            can.drawRightString(tax_con_x[1], tax_con_pos_y, '{0:,.2f}'.format(wht.wht_amount3))

    can.setFont('TH Sarabun New', 11)
    can.drawRightString(tax_con_x[0], 6.4 * cm, '{0:,.2f}'.format(wht.pay_amount))
    can.drawRightString(tax_con_x[1], 6.4 * cm, '{0:,.2f}'.format(wht.wht_amount))

    can.setFont('TH Sarabun New', 16)
    can.drawString(6.6 * cm, 5.7 * cm, bht.bahttext(wht.wht_amount))

    if wht.tax_type == '1':
        can.setFont('TH Sarabun New', 11)
        can.drawString(13.1 * cm, 5.1 * cm, '{0:,.2f}'.format(wht.sso_amount))
        can.drawString(17.7 * cm, 5.1 * cm, '{0:,.2f}'.format(wht.pvf_amount))

    can.drawString(12.5 * cm, 3.1 * cm, get_print_by(wht))
    date_today = fields.Date.from_string(wht.pay_date)
    year_th = int(date_today.year)+543
    can.drawString(12 * cm, 2.7 * cm, str(date_today.day))
    can.drawString(14 * cm, 2.7 * cm, str(date_today.month))
    can.drawString(15.5 * cm, 2.7 * cm, str(year_th))

    can.save()
    # move to the beginning of the StringIO buffer
    packet.seek(0)
    return PdfFileReader(packet)

_parent_dir = os.path.dirname(pdf.__file__)


class CustomPdf(pdf.Pdf):

    @http.route('/web/pdf/wht_form', type='http', auth="user")
    @serialize_exception
    def wht_form(self, id, copy, **kw):
        res = super(CustomPdf, self).wht_form(id, **kw)
        wht = request.env['dtr.wht'].browse(int(id))
        if not wht.name:
            return request.not_found()
        if copy == 'False':
            content_pdf = gen_wht_form(wht)
        else:
            content_pdf = gen_wht_form_copy(wht)
        template_file = os.path.join(_parent_dir, 'form', 'wht.pdf')
        template_pdf = PdfFileReader(open(template_file, 'rb'))
        # add the "watermark", "mask" (which is the content pdf) on the existing page
        page = template_pdf.getPage(0)
        page.mergePage(content_pdf.getPage(0))
        output = PdfFileWriter()
        output.addPage(page)
        # write "output" to a stream
        outputStream = io.BytesIO()
        output.write(outputStream)
        valid_fname = re.sub('[^a-zA-Z0-9 \n\.]', '_', wht.name)+'.pdf'
        return request.make_response(outputStream.getvalue(),[('Content-Type', 'application/pdf'),('Content-Disposition', content_disposition(valid_fname))])


    @http.route('/web/pdf/wht_form_without_date', type='http', auth="user")
    @serialize_exception
    def wht_form_without_date(self, id, copy, **kw):
        res = super(CustomPdf, self).wht_form_without_date(id, **kw)

        wht = request.env['dtr.wht'].browse(int(id))
        if not wht.name:
            return request.not_found()

        if copy == 'False':
            content_pdf = gen_wht_form_without_date(wht)
        else:
            content_pdf = gen_wht_form_without_date_copy(wht)
        template_file = os.path.join(_parent_dir, 'form', 'wht.pdf')
        template_pdf = PdfFileReader(open(template_file, 'rb'))
        # add the "watermark", "mask" (which is the content pdf) on the existing page
        page = template_pdf.getPage(0)
        page.mergePage(content_pdf.getPage(0))
        output = PdfFileWriter()
        output.addPage(page)
        # write "output" to a stream
        outputStream = io.BytesIO()
        output.write(outputStream)
        valid_fname = re.sub('[^a-zA-Z0-9 \n\.]', '_', wht.name)+'.pdf'
        return request.make_response(outputStream.getvalue(),
                [('Content-Type', 'application/pdf'),
                 ('Content-Disposition', content_disposition(valid_fname))])
