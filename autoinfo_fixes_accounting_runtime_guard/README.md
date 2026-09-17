# AUTO-INFO : Fixes Accounting Runtime Guard

## ภาพรวม

โมดูลนี้ใช้สำหรับช่วยผู้ดูแลระบบและโปรแกรมเมอร์ตรวจความพร้อมของระบบ Odoo 15 ก่อนและหลังการอัปเดตโมดูล โดยรวบรวมปัญหาที่เจอจริงจากการติดตั้งและ deploy บน Linux มาไว้ในเมนูเดียว พร้อมคำอธิบาย สาเหตุ และคำสั่งแก้แบบคัดลอกไปใช้ได้ทันที

โมดูลนี้เน้น 3 เรื่องหลัก

- ตรวจปัญหา runtime ที่เจอบ่อย
- สรุปวิธีเช็กและวิธีแก้แบบปลอดภัย
- เก็บร่องรอยการ review ภายใน Odoo

## เหมาะกับใคร

- แอดมินระบบ Odoo
- โปรแกรมเมอร์ที่ deploy หรือ upgrade โมดูล
- ผู้ดูแล environment Linux ที่ต้องไล่ปัญหา runtime จริง

## ปัญหาที่โมดูลนี้ช่วยตรวจ

- runtime path ที่ใช้รัน Odoo จริง
- Python package ที่จำเป็นต่อการบูตระบบ
- dependency chain ที่เสี่ยง เช่น field มาจากอีกโมดูลแต่ `depends` ไม่ครบ
- schema risk เช่น `actual_due_date` และ `is_customer_and_supplier`
- โมดูลค้างสถานะ `to upgrade`
- คำเตือนเรื่อง external DB target เก่า
- กรณีหน้าเว็บยัง error ทั้งที่ shell เห็น field แล้ว เพราะ service ถือ registry เก่า

## สิ่งที่โมดูลนี้ทำได้

- รันชุดตรวจผ่านปุ่ม `Run Checks`
- แสดงผลตรวจเป็น `ok`, `warning`, `error`, `review`
- เปิด `Fix Help` เพื่อดูคำสั่งแก้แบบ copy-paste
- บันทึกว่าใครเป็นผู้ `Mark Reviewed`

## สิ่งที่โมดูลนี้ไม่ทำ

- ไม่ติดตั้ง package Linux หรือ Python ให้อัตโนมัติ
- ไม่ restart service ให้อัตโนมัติ
- ไม่แก้ `/etc/odoo/odoo.conf` ให้อัตโนมัติ
- ไม่แก้ source module อื่นแบบเงียบ ๆ
- ไม่แก้ Odoo core

## โครงสร้างเอกสาร

- `docs/installation_guide.md` : คู่มือติดตั้งแบบละเอียดตั้งแต่ต้นจนจบ
- `docs/troubleshooting.md` : คู่มือแก้ปัญหาตามอาการ
- `docs/technical_guide.md` : คู่มือทางเทคนิคและโครงสร้างการทำงาน
- `docs/user_guide.md` : วิธีใช้งานเมนูในระบบ

## คำสั่งติดตั้งแบบเร็ว

ใช้เมื่อ path และ `addons_path` พร้อมแล้ว

```bash
cd /var/odoo
python3 /var/odoo/odoo15/odoo-bin \
  -c /etc/odoo/odoo.conf \
  -d odoo_golive \
  -i autoinfo_fixes_accounting_runtime_guard \
  --stop-after-init
sudo systemctl restart odoo
sudo systemctl status odoo --no-pager
```

## Runtime ที่พิสูจน์ใช้งานได้

คำสั่งมาตรฐานที่ใช้ในคู่มือนี้คือ

```bash
python3 /var/odoo/odoo15/odoo-bin -c /etc/odoo/odoo.conf
```

## Python Package ที่ควรตรวจ

- `PyPDF2`
- `Pillow`
- `reportlab`
- `Babel`
- `passlib`
- `pdfminer.six`

## เวอร์ชัน

### 15.0.1.0.0 - 2026-09-17

#### Added
- เพิ่มโมดูล `autoinfo_fixes_accounting_runtime_guard`
- เพิ่ม model สำหรับรอบตรวจและผลตรวจ
- เพิ่ม wizard `Fix Help`
- เพิ่มเมนู `Runtime Guard`
- เพิ่มชุดเอกสารติดตั้ง ใช้งาน เทคนิค และ troubleshooting

#### Changed
- รวมองค์ความรู้จากปัญหา deploy จริงมาไว้ในโมดูลเดียว
- เพิ่มการเก็บผลตรวจและสถานะ review

#### Fixed
- ลดเวลาไล่ปัญหา runtime ที่เกิดซ้ำ
- ทำให้ผู้ดูแลระบบมีคำสั่งเช็กและคำสั่งแก้แบบคัดลอกไปใช้ได้ทันที

## Credits

- The Auto-Info Co., Ltd. : Dev Team / Mr. Nattanon Vinyangkoon
- AI Coding Assistant: TRAE SOLO / MICROSOFT 365 COPILOT
