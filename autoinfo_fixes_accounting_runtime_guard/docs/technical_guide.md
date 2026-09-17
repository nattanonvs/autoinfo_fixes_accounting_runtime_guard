# Technical Guide

## วัตถุประสงค์ทางเทคนิค

โมดูลนี้ถูกออกแบบให้เป็นชั้นตรวจสอบและสรุปแนวทางแก้สำหรับปัญหา runtime ของ Odoo 15 โดยไม่ไปแตะ Odoo core และไม่ทำงานอัตโนมัติกับระบบปฏิบัติการภายนอก

เป้าหมายหลักคือ

- ทำให้ปัญหาที่เคยเจอจริงตรวจซ้ำได้
- ลดเวลาไล่ root cause
- ให้คำสั่งแก้แบบ copy-paste
- มี audit trail ว่าใคร review อะไรแล้ว

## โครงสร้างหลักของโมดูล

### Models

- `autoinfo.runtime.guard.run`
  - เก็บหัวรอบการตรวจ
  - เก็บชื่อรอบตรวจ วันที่ และผู้ review
- `autoinfo.runtime.guard.check`
  - เก็บผลตรวจรายรายการ
  - เก็บ `check_code`, `severity`, `summary`, `details`, และข้อมูลคำแนะนำ
- `autoinfo.runtime.guard.fix.help`
  - เป็น transient model สำหรับ popup ช่วยแก้ปัญหา
  - ใช้แสดงสาเหตุ คำสั่งแก้ คำสั่งตรวจซ้ำ และหมายเหตุความเสี่ยง

### Service Layer

service หลักอยู่ที่ `runtime_guard_service.py`

หน้าที่หลัก

- สร้างรอบตรวจใหม่
- สร้าง check records ตาม check set v1
- จัดระดับผลตรวจ
- เตรียมข้อมูลสำหรับ wizard `Fix Help`

## Check Set V1

### 1. Runtime Path

ตรวจว่า command มาตรฐานที่ใช้ในงาน deploy คือ

```text
python3 /var/odoo/odoo15/odoo-bin -c /etc/odoo/odoo.conf
```

### 2. Python Package

ตรวจ package ที่เป็น blocker ในงานจริง

- `PyPDF2`
- `Pillow`
- `reportlab`
- `Babel`
- `passlib`
- `pdfminer.six`

### 3. Dependency Chain

ใช้เพื่อเตือนกรณีโมดูลปลายทางเรียก field จากโมดูลต้นทาง แต่ `depends` ไม่ครบ เช่นกรณี `dtr_billing`

### 4. Schema Risk

ใช้เตือนกรณี field สำคัญหาย เช่น

- `actual_due_date`
- `is_customer_and_supplier`

### 5. Module State

ใช้สรุปความเสี่ยงกรณีมีโมดูลค้างสถานะ `to upgrade`

### 6. External DB Warning

ใช้เตือนกรณีระบบภายนอกยังอ้างฐานข้อมูลเก่า

## หลักการออกแบบ

### Non-Invasive

โมดูลนี้ไม่ทำงานต่อไปนี้

- ไม่ติดตั้ง package ให้อัตโนมัติ
- ไม่ restart service ให้อัตโนมัติ
- ไม่แก้ `odoo.conf` ให้อัตโนมัติ
- ไม่แก้ source module อื่นแบบเงียบ ๆ

### Auditability

ทุกการตรวจควรย้อนดูได้ว่ารันเมื่อไร ใคร review แล้ว และผลตรวจคืออะไร

### Copy-Paste First

คำสั่งแก้ใน wizard ต้องคัดลอกไปใช้ได้จริงบน Linux

## UI Flow

1. ผู้ใช้เปิดเมนู `Runtime Guard`
2. กด `Run Checks`
3. ระบบสร้าง check records
4. ผู้ใช้เปิดรายการที่ต้องดู
5. กด `Open Fix Help`
6. คัดลอกคำสั่งไปใช้
7. เมื่อจัดการแล้วให้กด `Mark Reviewed`

## ไฟล์สำคัญ

- `models/runtime_guard_check.py`
- `models/runtime_guard_service.py`
- `wizard/runtime_guard_fix_help.py`
- `views/runtime_guard_views.xml`
- `security/ir.model.access.csv`
- `data/runtime_guard_cron.xml`

## ข้อจำกัดที่ต้องรู้

- ถ้าปัญหาเกิดจาก source module พังก่อนโหลด โมดูลนี้ช่วยได้แค่บอกสาเหตุและแนะนำวิธีแก้
- ถ้า dependency chain ของโมดูลต้นทางผิด ต้องแก้ที่ manifest ของโมดูลต้นทางจริง
- ถ้า package Python ขาด ต้องติดตั้งที่ OS หรือ interpreter จริงด้วยมือ
- ถ้า service ถือ registry เก่า ต้อง restart Odoo service เอง

## แนวทางทดสอบ

การทดสอบหลักแบ่งเป็น 2 ส่วน

- service tests
  - ตรวจการสร้าง check records
  - ตรวจ severity
  - ตรวจ summary และ guidance
- UI tests
  - ตรวจเมนู
  - ตรวจปุ่ม
  - ตรวจ `Fix Help`
  - ตรวจ `Mark Reviewed`

## แนวทางขยายในอนาคต

- เพิ่ม check สำหรับ config validation
- เพิ่ม check สำหรับ service/runtime mismatch
- เพิ่ม check สำหรับ dependency chain แบบอ่าน manifest จริง
- เพิ่ม export ผลตรวจเป็นไฟล์สำหรับส่งทีม infra หรือทีม dev
