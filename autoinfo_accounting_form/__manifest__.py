# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'AUTO INFO - Account Form',
    'version': '1.31',
    'category': 'DTR - ERP Accounting',
    'license': 'OPL-1',
    'website': 'https://www.dataroot.asia/support-odoo',
    'summary': 'Customize Report Accounting.',
    'description': """
Description
-----------
Customize Report Accounting.
    - Customer invoice Form (autoinfo)
    - Customer Receipt Form (autoinfo)

Changelog
---------

**Version 1.31**
    - Add page number in invoice report

**Version 1.30**
    - Add display branch code in invoice preprint
    - Changed display department in invoice preprint

**Version 1.29**
    - Fixed issue not display signature

**Version 1.28**
    - Fixed template invoice preprint

**Version 1.27-1.27b**
    - Fixed A21B-T127
    - Fixed tax invoice preprint report

**Version 1.26**
    - Fix task A21B-T207, A21B-T275

**Version 1.25**
    - Fix task A21B-T225, A21B-T33
    - Fix task A21B-T181 #2

**Version 1.24**
    - Fix task A21B-T183
    - Fix task A21B-T181

**Version 1.23**
    - Fix task A21B-T175

**Version 1.22**
    - Fix A21B-T33 Z-020
    - Fixed issue display purchase order number in prepayment report

**Version 1.21**
    - Fix task A21B-T147 (Prepayment Form)

**Version 1.20**
    - Fix task A21B-T127

**Version 1.19**
    - Fixed issue deduct deposit payment line show in report

**Version 1.18**
    - Fix task A21B-T69
    - Fix task A21B-T127

**Version 1.17**
    - Fix task A21B-T127 form Customer invoice (autoinfo) ใบกำกับภาษี (สินค้า)

**Version 1.16**
    - Fixed issue display amount total in footer is null

**Version 1.15**
    - Fixed issue display amount total in footer case down payment

**Version 1.14**
    - Display amount THB in invoice report

**Version 1.13**
    - Fix task A21B-T99, A21B-T101

**Version 1.12**
    - Fixed issue not display down payment amount in report

**Version 1.11**
    - Task A21B-T17, A21B-T26, A21B-T33, A21B-T36, A21B-T47, A21B-T60, A21B-T59
    - Fixed wrong wording in invoice report, billing report, prepayment report and debit note report

**Version 1.10**
    - Task A433-T100, A433-T109, A433-T92, A433-T93, A433-T94

**Version 1.9**
    - Revise template credit note and debit note report (A433-T100)

**Version 1.8**
    - Add new selection date format
    - Revise template report receipt and invoice
    - Add field remark payment for display in report

**Version 1.7**
    - Fix 
    
**Version 1.6**
    - Fix task A433-T64

**Version 1.5**
    - Fix task A433-T92 #3

**Version 1.4**
    - Fix task A433-T92, A433-T93, A433-T94
    
**Version 1.3**
    - Fix task A433-T92 ,Customer invoice Form (autoinfo)

**Version 1.2**
    - Fix task A433-T63 ,add Customer Receipt Preprint Form (autoinfo)
    
**Version 1.1**
    - Fix task A433-T63 ,add form Customer invoice Preprint Form (autoinfo)

**Version 1.0**
    - Initial

    """,
    'author': 'Dataroot Asia Co., Ltd.',
    'created_by': 'Varawit Termwaraporn',
    'depends': [
        'dtr_accounting_form',
        'autoinfo_employees',
        'account'
    ],
    'application': False,
    'data': [
        'security/ir.model.access.csv',
        'reports/autoinfo_tax_invoice_pp_form.xml',
        'reports/autoinfo_receipt_pp_form.xml',
        'reports/receipt_form.xml',
        'reports/autoinfo_invoice_form.xml',
        'views/account_payment_view.xml',
        'reports/autoinfo_tax_receipt_form.xml',
    ],
}
