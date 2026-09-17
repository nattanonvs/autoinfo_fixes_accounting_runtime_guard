# Installation Guide

## Overview

โมดูลนี้ใช้สำหรับผู้ดูแลระบบเพื่อเช็กความพร้อมก่อนอัปเดตโมดูลบัญชีและโมดูล custom

## Install Steps

1. วางโมดูลไว้ที่ `/var/odoo/custom15_autoinfo`
2. เพิ่ม path นี้ใน `addons_path` ถ้ายังไม่มี
3. อัปเดต Apps List
4. ติดตั้งโมดูล `AUTO-INFO : Fixes Accounting Runtime Guard`

## Linux Command

```bash
cd /var/odoo
python3 /var/odoo/odoo15/odoo-bin -c /etc/odoo/odoo.conf -d odoo_golive -i autoinfo_fixes_accounting_runtime_guard --stop-after-init
```

## Remark

- Runtime command ที่พิสูจน์ใช้งานได้คือ `python3 /var/odoo/odoo15/odoo-bin -c /etc/odoo/odoo.conf`
- ถ้าจะติดตั้ง Python package ต้องใช้ interpreter ตัวเดียวกับที่ Odoo ใช้งานจริง
- โมดูลนี้ไม่ติดตั้ง package ให้เอง และไม่แก้ manifest ของโมดูลต้นทางให้อัตโนมัติ
