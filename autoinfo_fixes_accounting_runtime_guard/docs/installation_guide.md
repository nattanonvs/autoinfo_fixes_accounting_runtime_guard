# Installation Guide

## วัตถุประสงค์

เอกสารนี้ใช้สำหรับติดตั้งโมดูล `autoinfo_fixes_accounting_runtime_guard` ตั้งแต่ต้นจนจบ โดยอิงจาก environment Linux ที่ใช้งานจริงของ Odoo 15 และใช้คำสั่งที่สามารถคัดลอกไปใช้งานได้ทันที

## กลุ่มผู้อ่าน

- แอดมินระบบ
- โปรแกรมเมอร์
- ผู้ดูแล Linux server ที่รัน Odoo

## ข้อมูลมาตรฐานที่ใช้ในคู่มือนี้

- Odoo path: `/var/odoo/odoo15/odoo-bin`
- config path: `/etc/odoo/odoo.conf`
- custom addons path: `/var/odoo/custom15_autoinfo`
- database ตัวอย่าง: `odoo_golive`

## ขั้นที่ 1 ตรวจ path ที่จำเป็น

รันคำสั่งนี้ก่อน เพื่อยืนยันว่า path หลักมีอยู่จริง

```bash
ls -ld /var/odoo
ls -ld /var/odoo/odoo15
ls -l /var/odoo/odoo15/odoo-bin
ls -ld /var/odoo/custom15_autoinfo
ls -l /etc/odoo/odoo.conf
```

ถ้า path ใดไม่มี ให้แก้ path ให้ถูกก่อนแล้วค่อยทำขั้นถัดไป

## ขั้นที่ 2 วางโมดูล

ถ้ายังไม่มีโมดูลใน server ให้คัดลอกโฟลเดอร์โมดูลไปไว้ที่

```text
/var/odoo/custom15_autoinfo/autoinfo_fixes_accounting_runtime_guard
```

ตัวอย่างคำสั่งตรวจว่าโมดูลอยู่ถูกที่แล้ว

```bash
ls -ld /var/odoo/custom15_autoinfo/autoinfo_fixes_accounting_runtime_guard
ls -l /var/odoo/custom15_autoinfo/autoinfo_fixes_accounting_runtime_guard/__manifest__.py
```

## ขั้นที่ 3 ตรวจ `addons_path`

ตรวจว่า `/var/odoo/custom15_autoinfo` อยู่ใน `addons_path`

```bash
grep -n "addons_path" /etc/odoo/odoo.conf
```

ถ้ายังไม่มี ให้แก้ไฟล์ `odoo.conf`

ตัวอย่างก่อนแก้

```text
addons_path = /var/odoo/odoo15/odoo/addons,/var/odoo/odoo15/addons
```

ตัวอย่างหลังแก้

```text
addons_path = /var/odoo/odoo15/odoo/addons,/var/odoo/odoo15/addons,/var/odoo/custom15_autoinfo
```

ถ้าต้องการใช้คำสั่ง Python ช่วยแก้แบบปลอดภัย

```bash
python3 - <<'PY'
from pathlib import Path
cfg = Path('/etc/odoo/odoo.conf')
text = cfg.read_text(encoding='utf-8')
needle = '/var/odoo/custom15_autoinfo'
if needle not in text:
    lines = []
    for line in text.splitlines():
        if line.strip().startswith('addons_path') and needle not in line:
            line = line.rstrip() + ',' + needle
        lines.append(line)
    cfg.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('updated')
else:
    print('already present')
PY
```

## ขั้นที่ 4 ตรวจ Python interpreter ที่ Odoo ใช้งานจริง

ต้องใช้ interpreter ตัวเดียวกับที่ใช้รัน Odoo เสมอ

```bash
which python3
head -n 1 /var/odoo/odoo15/odoo-bin
python3 -c "import sys; print(sys.executable)"
```

ผลที่ควรเห็นในระบบนี้คือ `python3` และ `/usr/bin/python3`

## ขั้นที่ 5 ตรวจ package ที่จำเป็น

ตรวจ package สำคัญก่อนติดตั้งโมดูล

```bash
python3 -m pip show PyPDF2 Pillow reportlab Babel passlib pdfminer.six
```

ถ้ายังไม่ครบ ให้ติดตั้ง

```bash
python3 -m pip install PyPDF2 Pillow reportlab Babel passlib pdfminer.six
```

ถ้าต้องการติดตั้งจาก requirements ของ Odoo ก่อน

```bash
python3 -m pip install -r /var/odoo/odoo15/requirements.txt
python3 -m pip install PyPDF2 Pillow reportlab Babel passlib pdfminer.six
```

## ขั้นที่ 6 ตรวจว่า Python import ได้จริง

```bash
python3 - <<'PY'
import sys
mods = ['PyPDF2', 'PIL', 'reportlab', 'babel', 'passlib']
print(sys.executable)
for name in mods:
    __import__(name)
    print('OK', name)
PY
```

ถ้า import ไม่ผ่าน ให้แก้ package ก่อน แล้วจึงไปขั้นถัดไป

## ขั้นที่ 7 หยุด service ก่อนติดตั้งหรืออัปเดต

ป้องกันปัญหา port ชน และลดความเสี่ยงเรื่อง worker ถือ registry เก่า

```bash
sudo systemctl stop odoo
sudo systemctl status odoo --no-pager
```

## ขั้นที่ 8 ติดตั้งโมดูล

```bash
cd /var/odoo
python3 /var/odoo/odoo15/odoo-bin \
  -c /etc/odoo/odoo.conf \
  -d odoo_golive \
  -i autoinfo_fixes_accounting_runtime_guard \
  --stop-after-init
```

ถ้าจะอัปเดตโมดูลเดิมภายหลัง ให้ใช้

```bash
cd /var/odoo
python3 /var/odoo/odoo15/odoo-bin \
  -c /etc/odoo/odoo.conf \
  -d odoo_golive \
  -u autoinfo_fixes_accounting_runtime_guard \
  --stop-after-init
```

## ขั้นที่ 9 เปิด service กลับ

```bash
sudo systemctl start odoo
sudo systemctl status odoo --no-pager
```

ถ้าต้องการ restart ตรง ๆ หลัง update ใช้

```bash
sudo systemctl restart odoo
sudo systemctl status odoo --no-pager
```

## ขั้นที่ 10 ตรวจผลหลังติดตั้ง

เช็กจาก shell ว่าโมดูลถูกติดตั้งแล้ว

```bash
python3 /var/odoo/odoo15/odoo-bin shell -c /etc/odoo/odoo.conf -d odoo_golive
```

จากนั้นรัน

```python
mod = env['ir.module.module'].search([('name', '=', 'autoinfo_fixes_accounting_runtime_guard')], limit=1)
print(mod.name, mod.state)
```

ผลที่ควรได้คือ `autoinfo_fixes_accounting_runtime_guard installed`

## ขั้นที่ 11 วิธีใช้งานหลังติดตั้ง

1. เข้าเมนู `Technical`
2. เปิดเมนู `Runtime Guard`
3. กด `Run Checks`
4. เปิดรายการที่ขึ้น `warning`, `error`, หรือ `review`
5. กด `Open Fix Help`
6. คัดลอกคำสั่งไปใช้
7. กลับมากด `Mark Reviewed`

## คำสั่งรวมแบบ copy-paste ตั้งแต่ต้นจนจบ

ใช้เมื่อ path ถูกต้องและมีโมดูลอยู่ใน `/var/odoo/custom15_autoinfo` แล้ว

```bash
cd /var/odoo
ls -l /var/odoo/odoo15/odoo-bin
ls -l /etc/odoo/odoo.conf
ls -ld /var/odoo/custom15_autoinfo/autoinfo_fixes_accounting_runtime_guard
grep -n "addons_path" /etc/odoo/odoo.conf
python3 -m pip install -r /var/odoo/odoo15/requirements.txt
python3 -m pip install PyPDF2 Pillow reportlab Babel passlib pdfminer.six
sudo systemctl stop odoo
python3 /var/odoo/odoo15/odoo-bin \
  -c /etc/odoo/odoo.conf \
  -d odoo_golive \
  -i autoinfo_fixes_accounting_runtime_guard \
  --stop-after-init
sudo systemctl start odoo
sudo systemctl status odoo --no-pager
```

## Remark สำคัญ

- Runtime command ที่พิสูจน์ใช้งานได้คือ `python3 /var/odoo/odoo15/odoo-bin -c /etc/odoo/odoo.conf`
- ถ้าจะติดตั้ง Python package ต้องใช้ interpreter ตัวเดียวกับที่ Odoo ใช้งานจริง
- ไม่ควรใช้ `pip install --upgrade cryptography pyOpenSSL cffi` ทับ system Python ตรง ๆ เพราะอาจทำให้ `OpenSSL`, `cryptography`, และ `cffi` ชนกันจน Odoo และ `pip` พังทั้งระบบ
- ถ้าจำเป็นต้องใช้ `pip` กับ package กลุ่ม SSL ให้ใช้ `venv` แยกจาก system Python
- โมดูลนี้ไม่ติดตั้ง package ให้เอง และไม่แก้ manifest ของโมดูลต้นทางให้อัตโนมัติ
- ถ้า shell เห็น field แล้ว แต่หน้าเว็บยัง error ให้ restart Odoo service ก่อนสงสัยปัญหาอื่น
- ถ้ามีปัญหา dependency chain ของโมดูลต้นทาง ต้องแก้ที่โมดูลต้นทางจริงก่อน โมดูลนี้ช่วยแค่ตรวจและแนะนำคำสั่งแก้
