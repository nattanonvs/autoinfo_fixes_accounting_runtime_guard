# Troubleshooting

## วิธีใช้เอกสารนี้

เอกสารนี้เรียงตามอาการที่เจอจริงในงานติดตั้งและอัปเดต Odoo 15 ให้เริ่มจากอาการที่ตรงที่สุด แล้วทำตามลำดับนี้

1. อ่านอาการ
2. ดูสาเหตุที่เป็นไปได้
3. รันคำสั่งเช็ก
4. รันคำสั่งแก้
5. ตรวจซ้ำ

## อาการ: `python3: can't open file '/var/odoo/odoo-15.0/src/odoo-bin'`

### สาเหตุ

- ใช้ path ของ `odoo-bin` ไม่ตรงกับเครื่องจริง

### วิธีเช็ก

```bash
find /var/odoo -name odoo-bin 2>/dev/null
```

### วิธีแก้

ใช้ path ที่พิสูจน์แล้ว

```bash
python3 /var/odoo/odoo15/odoo-bin -c /etc/odoo/odoo.conf
```

## อาการ: `ModuleNotFoundError` เช่น `PyPDF2`, `PIL`, `reportlab`, `babel`, `passlib`

### สาเหตุ

- package ยังไม่ถูกติดตั้ง
- package อยู่คนละ Python interpreter

### วิธีเช็ก

```bash
which python3
python3 -c "import sys; print(sys.executable)"
python3 -m pip show PyPDF2 Pillow reportlab Babel passlib pdfminer.six
```

### วิธีแก้

```bash
python3 -m pip install -r /var/odoo/odoo15/requirements.txt
python3 -m pip install PyPDF2 Pillow reportlab Babel passlib pdfminer.six
```

### วิธีตรวจซ้ำ

```bash
python3 - <<'PY'
mods = ['PyPDF2', 'PIL', 'reportlab', 'babel', 'passlib']
for name in mods:
    __import__(name)
    print('OK', name)
PY
```

## อาการ: `module 'lib' has no attribute 'X509_V_FLAG_NOTIFY_POLICY'`

### อาการที่เจอ

มักจะขึ้นตอนรัน Odoo หรือแม้แต่ตอนรัน `python3 -m pip ...` โดยจะมีข้อความคล้ายนี้

```text
Couldn't load module web
Couldn't load module base
AttributeError: module 'lib' has no attribute 'X509_V_FLAG_NOTIFY_POLICY'
```

บางครั้งจะเห็นต่อเนื่องไปถึง `OpenSSL/crypto.py` และทำให้ทั้ง `web`, `base`, `pip`, และ Odoo ใช้งานไม่ได้

### สาเหตุจริง

ปัญหานี้ไม่ได้เกิดจาก `addons_path` หรือจากโมดูล Odoo โดยตรง แต่เกิดจาก Python SSL stack ชนกัน โดยเฉพาะ

- `OpenSSL` ของระบบจาก `apt` อยู่ใน `/usr/lib/python3/dist-packages`
- แต่ `cryptography`, `cffi`, หรือ `_cffi_backend` ถูกลงทับจาก `pip` ใน `/usr/local/lib/python3.8/dist-packages`

ผลคือ package คนละแหล่ง คนละเวอร์ชัน ถูกโหลดผสมกัน จน `pyOpenSSL` ใช้งานกับ `cryptography` ไม่ได้

### หลักฐานที่ใช้ยืนยัน

กรณีที่เจอจริง มีลักษณะดังนี้

- `python = /usr/bin/python3`
- `OpenSSL_file = /usr/lib/python3/dist-packages/OpenSSL/__init__.py`
- `cryptography_file = /usr/local/lib/python3.8/dist-packages/cryptography/__init__.py`
- `cffi_file = /usr/local/lib/python3.8/dist-packages/cffi/__init__.py`

ถ้าเห็นรูปแบบนี้ แปลว่า environment ชนกันจริง

### Step 1 ตรวจ Python และ package path

รันคำสั่งนี้

```bash
which python3
python3 -c "import sys; print(sys.executable)"
```

แล้วตรวจ `cryptography` กับ `cffi`

```bash
python3 - <<'PY'
import cryptography, cffi, ssl, sys
print("python =", sys.executable)
print("cryptography =", cryptography.__version__)
print("cryptography_file =", cryptography.__file__)
print("cffi_file =", cffi.__file__)
print("ssl =", ssl.OPENSSL_VERSION)
PY
```

ตรวจ package ฝั่งระบบ

```bash
dpkg -l | grep -E "python3-openssl|python3-cryptography|python3-cffi|libssl"
```

ตรวจ path ที่เสี่ยงชน

```bash
ls -ld /usr/local/lib/python3.8/dist-packages/cryptography* /usr/local/lib/python3.8/dist-packages/OpenSSL* 2>/dev/null
ls -ld /usr/local/lib/python3.8/dist-packages/cffi* /usr/local/lib/python3.8/dist-packages/_cffi_backend* 2>/dev/null
ls -ld /usr/lib/python3/dist-packages/cryptography* /usr/lib/python3/dist-packages/OpenSSL* 2>/dev/null
ls -ld /usr/lib/python3/dist-packages/cffi* /usr/lib/python3/dist-packages/_cffi_backend* 2>/dev/null
```

### Step 2 ย้าย package ฝั่ง `/usr/local` ออกไปก่อน

สร้างโฟลเดอร์ backup

```bash
mkdir -p /root/pyssl_fix_backup_20260917
```

ย้าย package ที่ชนออกทีละรายการ

```bash
mv -v /usr/local/lib/python3.8/dist-packages/cryptography* /root/pyssl_fix_backup_20260917/ 2>/dev/null
mv -v /usr/local/lib/python3.8/dist-packages/cffi* /root/pyssl_fix_backup_20260917/ 2>/dev/null
mv -v /usr/local/lib/python3.8/dist-packages/_cffi_backend* /root/pyssl_fix_backup_20260917/ 2>/dev/null
mv -v /usr/local/lib/python3.8/dist-packages/OpenSSL* /root/pyssl_fix_backup_20260917/ 2>/dev/null
```

ตรวจว่าไฟล์ถูกย้ายจริง

```bash
ls -la /root/pyssl_fix_backup_20260917
```

### Step 3 ติดตั้ง package ฝั่งระบบกลับให้ครบ

```bash
apt update
apt install --reinstall -y python3-cffi python3-cffi-backend python3-cryptography python3-openssl libssl1.1
```

ถ้าเครื่องแจ้งว่า package ตัวใดมีอยู่แล้ว ก็ให้ปล่อยผ่านได้ เพราะจุดสำคัญคือให้ระบบ reinstall ชุดมาตรฐานของ `apt`

### Step 4 ตรวจซ้ำว่า Python SSL stack กลับมาเป็นของระบบทั้งหมดแล้ว

```bash
python3 - <<'PY'
import OpenSSL, cryptography, cffi, ssl, sys
print("python =", sys.executable)
print("OpenSSL_file =", OpenSSL.__file__)
print("cryptography =", cryptography.__version__)
print("cryptography_file =", cryptography.__file__)
print("cffi_file =", cffi.__file__)
print("ssl =", ssl.OPENSSL_VERSION)
PY
```

ผลที่ควรเห็น

- `OpenSSL_file` อยู่ใต้ `/usr/lib/python3/dist-packages`
- `cryptography_file` อยู่ใต้ `/usr/lib/python3/dist-packages`
- `cffi_file` อยู่ใต้ `/usr/lib/python3/dist-packages`
- ไม่ error อีก

### Step 5 ทดสอบ Odoo หลังซ่อม environment

```bash
systemctl stop odoo
python3 /var/odoo/odoo15/odoo-bin -c /etc/odoo/odoo.conf -d odoo_golive --stop-after-init
systemctl start odoo
systemctl status odoo --no-pager
```

ถ้า Odoo ผ่านขั้นนี้ แปลว่า environment กลับมาปกติแล้ว

### Step 6 ทดสอบ update module หลังซ่อมแล้ว

ถ้าต้องการอัปเดตโมดูลต่อ ให้ใช้รูปแบบนี้

```bash
systemctl stop odoo
python3 /var/odoo/odoo15/odoo-bin \
  -c /etc/odoo/odoo.conf \
  -d odoo_golive \
  -u autoinfo_fixes_accounting_runtime_guard,dtr_stock_form,dtr_taxes,autoinfo_stock_picking_sale_person_tier \
  --stop-after-init
systemctl start odoo
systemctl status odoo --no-pager
```

### หมายเหตุสำคัญ

- อย่าใช้ `pip install --upgrade cryptography pyOpenSSL cffi` ทับ system Python ตรง ๆ
- ถ้าจำเป็นต้องใช้ `pip` ให้ใช้ `venv`
- ถ้าระบบ Odoo พังพร้อม `web` และ `base` ด้วย error นี้ ให้สงสัย package ชนใน `/usr/local/lib/python3.8/dist-packages` ก่อน
- โฟลเดอร์ backup `/root/pyssl_fix_backup_20260917` ควรเก็บไว้ก่อนจนกว่าจะยืนยันได้ว่าระบบปกติจริง

## อาการ: `OSError: [Errno 98] Address already in use`

### สาเหตุ

- Odoo service เดิมยังรันอยู่
- port `8069` ยังถูกใช้งาน

### วิธีเช็ก

```bash
sudo systemctl status odoo --no-pager
ss -ltnp | grep 8069
```

### วิธีแก้

```bash
sudo systemctl stop odoo
sudo systemctl status odoo --no-pager
```

จากนั้นค่อยรันคำสั่ง `-i` หรือ `-u`

## อาการ: `Field "actual_due_date" does not exist in model "account.move"`

### สาเหตุ

- โมดูลที่ใช้ field นี้อ้าง field จาก `dtr_billing`
- `depends` ของโมดูลต้นทางไม่ครบ
- โมดูลเจ้าของ field ยังไม่ได้อัปเดต

### วิธีเช็ก

```bash
grep -Rns "actual_due_date" /var/odoo/odoo15_mods /var/odoo/odoo15_mods_accounting /var/odoo/custom15_autoinfo
```

ตรวจ manifest ของโมดูลที่พัง

```bash
grep -n "'depends'" /var/odoo/odoo15_mods_accounting/dtr_customer_invoices_with_sales/__manifest__.py
grep -n "'depends'" /var/odoo/odoo15_mods_accounting/dtr_payment_invoice/__manifest__.py
grep -n "'depends'" /var/odoo/odoo15_mods_accounting/dtr_vendor_bills_with_purchase/__manifest__.py
```

### วิธีแก้

ต้องเพิ่ม `dtr_billing` ลงใน `depends` ของโมดูลที่เรียกใช้ field นี้

ตัวอย่าง Python auto-fix

```bash
python3 - <<'PY'
from pathlib import Path
targets = [
    Path('/var/odoo/odoo15_mods_accounting/dtr_customer_invoices_with_sales/__manifest__.py'),
    Path('/var/odoo/odoo15_mods_accounting/dtr_payment_invoice/__manifest__.py'),
    Path('/var/odoo/odoo15_mods_accounting/dtr_vendor_bills_with_purchase/__manifest__.py'),
]
for path in targets:
    text = path.read_text(encoding='utf-8')
    if 'dtr_billing' not in text:
        text = text.replace('],\n    \'application\'', ", 'dtr_billing'],\n    'application'")
        path.write_text(text, encoding='utf-8')
        print('updated', path)
    else:
        print('already ok', path)
PY
```

จากนั้นอัปเดตโมดูลที่เกี่ยวข้อง

```bash
sudo systemctl stop odoo
python3 /var/odoo/odoo15/odoo-bin \
  -c /etc/odoo/odoo.conf \
  -d odoo_golive \
  -u dtr_billing,dtr_customer_invoices_with_sales,dtr_payment_invoice,dtr_vendor_bills_with_purchase \
  --stop-after-init
sudo systemctl start odoo
```

## อาการ: `column res_partner.is_customer_and_supplier does not exist`

### สาเหตุ

- field นี้มาจากโมดูลต้นทางที่ยังไม่ถูกอัปเดตในฐานข้อมูล
- dependency chain ฝั่ง partner/master ยังไม่ครบ

### วิธีเช็ก

```bash
grep -Rns "is_customer_and_supplier" /var/odoo/odoo15_mods /var/odoo/odoo15_mods_accounting /var/odoo/custom15_autoinfo
```

### วิธีแก้

อัปเดตโมดูลที่เป็นเจ้าของ field และโมดูลที่ใช้ field ต่อ

```bash
sudo systemctl stop odoo
python3 /var/odoo/odoo15/odoo-bin \
  -c /etc/odoo/odoo.conf \
  -d odoo_golive \
  -u dtr_partner_master,dtr_taxation \
  --stop-after-init
sudo systemctl start odoo
```

## อาการ: มีโมดูลค้างสถานะ `to upgrade`

### สาเหตุ

- เคยมีการกด upgrade หรือเปลี่ยน source code แต่ยังไม่ได้อัปเดตจนครบ
- มี dependency chain ค้างกลางทาง

### วิธีเช็ก

```bash
psql -U autoerp -d odoo_golive -c "select name, state from ir_module_module where state='to upgrade' order by name;"
```

ถ้าต้องการ list แบบคัดลอกง่าย

```bash
psql -U autoerp -d odoo_golive -t -A -c "select string_agg(name, ',') from ir_module_module where state='to upgrade';"
```

### วิธีแก้

อัปเดตตามชุดที่เกี่ยวข้อง หรืออัปเดตทั้งหมดตามรายการที่ query ได้

```bash
sudo systemctl stop odoo
python3 /var/odoo/odoo15/odoo-bin \
  -c /etc/odoo/odoo.conf \
  -d odoo_golive \
  -u module1,module2,module3 \
  --stop-after-init
sudo systemctl start odoo
```

## อาการ: `Invalid field 'is_invoiced' on model 'stock.picking'`

### สาเหตุ

- service หรือ worker ยังถือ registry เก่า
- shell เห็น field แล้ว แต่หน้าเว็บยังใช้ process เก่า

### วิธีเช็ก

```bash
python3 /var/odoo/odoo15/odoo-bin shell -c /etc/odoo/odoo.conf -d odoo_golive
```

แล้วรัน

```python
print('is_invoiced' in env['stock.picking']._fields)
```

ถ้าผลเป็น `True` แต่หน้าเว็บยัง error ให้สงสัย stale registry

### วิธีแก้

```bash
sudo systemctl restart odoo
sudo systemctl status odoo --no-pager
```

จากนั้น hard refresh หน้าเว็บ

## อาการ: shell เห็น field แต่หน้าเว็บยัง error

### สาเหตุ

- worker ของเว็บยังไม่ reload หลังมีการอัปเดตโมดูล

### วิธีแก้

```bash
sudo systemctl restart odoo
sudo systemctl status odoo --no-pager
```

### แนวทางป้องกัน

หลังรัน `-u` กับโมดูลที่แตะ model หรือ view สำคัญ ให้ restart Odoo service ทุกครั้ง

## อาการ: attachment indexation แจ้งว่าไม่มี `pdfminer`

### สาเหตุ

- ระบบสามารถรัน Odoo ได้ แต่การ index PDF ยังทำงานไม่ครบ

### วิธีแก้

```bash
python3 -m pip install pdfminer.six
sudo systemctl restart odoo
```

## อาการ: external system ยังเรียก DB เก่า เช่น `FROMGOLIVE_15MAR2026`

### สาเหตุ

- มีระบบภายนอกหรือ script เก่าที่ยังชี้ฐานข้อมูลเดิม

### วิธีเช็ก

```bash
grep -Rns "FROMGOLIVE_15MAR2026" /var/odoo /etc 2>/dev/null
```

### วิธีแก้

- แก้ config ฝั่ง client, integration, API, cron, หรือ script ภายนอกให้ชี้ DB ปัจจุบัน
- ปัญหานี้ไม่ใช่ตัวบล็อกการติดตั้งโมดูลโดยตรง แต่ควรปิดให้ครบ

## เช็กภาพรวมแบบเร็ว

ถ้าต้องการเช็กสภาพแวดล้อมรอบเดียว ให้ใช้ชุดคำสั่งนี้

```bash
cd /var/odoo
which python3
python3 -c "import sys; print(sys.executable)"
ls -l /var/odoo/odoo15/odoo-bin
ls -l /etc/odoo/odoo.conf
grep -n "addons_path" /etc/odoo/odoo.conf
python3 -m pip show PyPDF2 Pillow reportlab Babel passlib pdfminer.six
sudo systemctl status odoo --no-pager
psql -U autoerp -d odoo_golive -c "select name, state from ir_module_module where state='to upgrade' order by name;"
```
