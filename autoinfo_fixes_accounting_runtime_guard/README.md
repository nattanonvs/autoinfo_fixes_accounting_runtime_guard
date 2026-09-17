# AUTO-INFO : Fixes Accounting Runtime Guard

## Purpose

โมดูลนี้ช่วยตรวจปัญหา runtime ที่เจอจริงระหว่างการอัปเดต Odoo 15 โดยไม่แก้ Odoo core และไม่แก้ environment ภายนอกแบบอัตโนมัติ

## What This Module Checks

- runtime path ที่ใช้จริง
- Python packages ที่เป็น blocker
- dependency chain ที่เสี่ยง เช่น `dtr_billing`
- schema risk เช่น `actual_due_date` และ `is_customer_and_supplier`
- โมดูลค้างสถานะ `to upgrade`
- คำเตือนเรื่อง external DB target

## Safety Rules

- ไม่ติดตั้ง package ให้อัตโนมัติ
- ไม่ restart service ให้อัตโนมัติ
- ไม่แก้ source module แบบเงียบ ๆ
- ให้คำสั่งแบบ copy-paste และบันทึกการ review ได้

## Credits

- The Auto-Info Co., Ltd. : Dev Team / Mr. Nattanon Vinyangkoon
- AI Coding Assistant: TRAE SOLO / MICROSOFT 365 COPILOT
