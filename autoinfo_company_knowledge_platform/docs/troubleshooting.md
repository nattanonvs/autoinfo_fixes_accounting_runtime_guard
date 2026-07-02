# Troubleshooting Guide

## 1) ภาพรวม

เอกสารนี้รวบรวมปัญหาที่พบบ่อยในการติดตั้ง ใช้งาน และทดสอบโมดูล `autoinfo_company_knowledge_platform` พร้อมแนวทางตรวจสอบและแก้ไขเบื้องต้น

## 2) ติดตั้งโมดูลไม่ขึ้นใน Apps

### อาการ

- ค้นหาโมดูลไม่เจอ
- กด Update Apps List แล้วโมดูลไม่ปรากฏ

### ตรวจสอบ

1. โมดูลอยู่ใน path นี้จริงหรือไม่:
   - `/var/odoo/custom15_autoinfo/autoinfo_company_knowledge_platform`
2. path นี้อยู่ใน `addons_path` ของ `/etc/odoo/odoo.conf` หรือไม่
3. มีไฟล์ `__manifest__.py` อยู่จริงหรือไม่
4. รีสตาร์ท Odoo แล้วหรือยัง

### แนวทางแก้

- เพิ่ม path ลงใน `addons_path`
- รีสตาร์ท service
- กด Update Apps List ใหม่

## 3) ติดตั้งแล้ว error เรื่อง XML / Access / External ID

### อาการ

- ติดตั้งไม่ผ่าน
- เจอ error ลักษณะ:
  - `External ID not found`
  - `ParseError`
  - `AccessError`

### ตรวจสอบ

1. ไฟล์ XML ใน manifest ถูกอ้างอิงครบหรือไม่
2. security files ถูกโหลดลำดับถูกต้องหรือไม่
3. record rules / groups / ACL ใช้ XML ID ที่มีอยู่จริงหรือไม่

### แนวทางแก้

- ตรวจ `__manifest__.py`
- ตรวจ `security/knowledge_security.xml`
- ตรวจ `security/knowledge_record_rules.xml`
- ตรวจ `security/ir.model.access.csv`

## 4) ผู้ใช้มองไม่เห็นเอกสารที่ควรเห็น

### อาการ

- ค้นหาไม่เจอ
- เปิด knowledge item ไม่ได้
- list view ไม่มีข้อมูล

### สาเหตุที่เป็นไปได้

- ผู้ใช้ไม่มี group ที่เหมาะสม
- ผู้ใช้ยังไม่ได้ตั้ง `knowledge_department_id`
- ผู้ใช้มี `knowledge_clearance_level` ต่ำเกินไป
- เอกสารยังไม่ `published`
- เอกสารอยู่คนละแผนกและไม่ได้ company-wide

### แนวทางแก้

1. ตรวจกลุ่มสิทธิ์ของ user
2. ตรวจ `knowledge_department_id`
3. ตรวจ `knowledge_clearance_level`
4. ตรวจ `department_id` ของเอกสาร
5. ตรวจ `classification`
6. ตรวจ `state`

## 5) ผู้ใช้ publish ไม่ได้

### อาการ

- กด Publish แล้วขึ้น `AccessError`
- ปุ่ม Publish ไม่ปรากฏ

### สาเหตุที่เป็นไปได้

- ผู้ใช้ไม่ใช่ Reviewer / Department Manager / Admin
- เอกสารยังไม่อยู่สถานะ `in_review`
- เอกสารอยู่คนละแผนกกับ reviewer/manager

### กติกาปัจจุบัน

- Reviewer/Manager ต้อง:
  - อยู่แผนกเดียวกับเอกสาร
  - เอกสารอยู่ `in_review`
- Admin publish ได้ทุกสถานะ

### แนวทางแก้

- ถ้าเป็น reviewer/manager ให้ส่งเอกสารเข้า review ก่อน
- ตรวจแผนกของ user และเอกสารให้ตรงกัน
- ถ้าต้องการ override ข้ามแผนก ให้ใช้ admin

## 6) Contributor แก้เอกสารไม่ได้

### อาการ

- เปิดฟอร์มแล้วแก้ไม่ได้
- save แล้วขึ้น AccessError

### คำอธิบาย

โมดูลนี้ใช้ policy แบบเข้ม:

- Contributor แก้ได้เฉพาะ draft ของตัวเอง
- Published item ห้ามแก้ตรง ๆ

### แนวทางแก้

- ตรวจว่าเอกสารเป็นของผู้ใช้จริงหรือไม่
- ตรวจว่า state ยังเป็น `draft` หรือไม่
- ถ้าต้องการแก้ published item ให้ใช้ flow สร้างเวอร์ชัน/แก้ผ่าน process ที่กำหนด

## 7) Scan Wizard ใช้งานไม่ได้

### อาการ

- เปิด wizard ไม่ได้
- สร้างเอกสารจาก scan ไม่สำเร็จ
- ได้ AccessError ตอนกด Create

### ตรวจสอบ

1. user อยู่ในกลุ่ม Contributor ขึ้นไปหรือไม่
2. department ที่เลือกตรงกับ `knowledge_department_id` ของ user หรือไม่
3. ไฟล์สแกนถูกแนบมาจริงหรือไม่

### คำอธิบาย

- Contributor ถูกจำกัดให้สร้างได้เฉพาะแผนกตัวเอง
- Admin/System สามารถข้ามข้อจำกัดนี้ได้

## 7.1) หาเมนู Scan Wizard หรือ Template ไม่เจอ

### อาการ

- ติดตั้งโมดูลแล้ว แต่ไม่เห็นเมนูสำหรับ scan wizard
- หาเมนู templates / taxonomy ไม่เจอ

### คำอธิบาย

ในเวอร์ชันปัจจุบัน โมดูลนี้มี:

- model
- view
- seed data
- backend capability

แต่ยัง **ไม่ได้เปิด standard menu entry ครบทุกส่วน** ใน UI หลัก

ดังนั้นกรณีต่อไปนี้ถือว่าเป็นพฤติกรรมปกติ:

- มีเมนู Search แต่ไม่มีเมนู scan wizard
- มี template data แต่ไม่มีเมนู template management

### แนวทางแก้

- ถ้าต้องการใช้งาน scan wizard จริง ให้เพิ่ม menu/action เอง หรือเรียกผ่าน technical/developer flow
- ถ้าต้องการให้ business users ใช้งาน template ได้จากเมนู ควรเพิ่ม UI flow เพิ่มเติม

## 8) เอกสารสแกนค้นหาไม่เจอ

### อาการ

- สร้าง scan item ได้
- แต่ search หา keyword ที่อยู่ในไฟล์ไม่เจอ

### สาเหตุ

โมดูลนี้ไม่ได้มี OCR engine ภายในตัวเอง

search จะใช้ OCR text ได้ก็ต่อเมื่อ:

- `knowledge.extraction` ถูกสร้างแล้ว
- field `extracted_text` ถูกเติมข้อความจริง

### แนวทางแก้

1. ตรวจว่ามี extraction record แล้วหรือยัง
2. ตรวจค่า `status`
3. ตรวจว่ามี `extracted_text` หรือยัง
4. ถ้ายังไม่มี ให้เติมผ่าน OCR pipeline ภายนอก

## 9) AI Answer ตอบว่าไม่พบข้อมูล ทั้งที่มีเอกสารอยู่

### สาเหตุที่พบบ่อย

- เอกสารยังไม่ `published`
- user ไม่มีสิทธิ์เห็นเอกสาร
- คำค้นไม่ match ข้อความใน `title/summary/body/extracted_text`
- question ว่างหรือมีแต่ช่องว่าง

### แนวทางแก้

1. เปิดเอกสารตรวจ `state`
2. ตรวจสิทธิ์ของ user
3. ตรวจว่ามี OCR text หรือไม่
4. ทดสอบด้วยคำค้นที่ตรงขึ้น

## 10) Chatter ไม่ขึ้นข้อความ แต่ workflow สำเร็จ

### คำอธิบาย

โมดูลนี้ใช้ safe chatter posting:

- จะพยายามโพสต์ข้อความลง chatter
- ถ้าเจอปัญหาบางอย่าง เช่น sender email ไม่พร้อม ระบบจะไม่ทำให้ workflow ล้ม

### สิ่งที่ควรทำ

- ตรวจ `email` ของผู้ใช้
- ตรวจการตั้งค่าฝั่ง mail
- ถ้าต้องการ audit trail ที่เข้มกว่านี้ ควรเพิ่ม server log หรือ business log เสริม

## 11) เทสต์โมดูลไม่ผ่าน

### คำสั่งตัวอย่าง

```bash
/var/odoo/odoo15/odoo-bin -c /etc/odoo/odoo.conf -d <test_db> -i autoinfo_company_knowledge_platform --test-enable --test-tags /autoinfo_company_knowledge_platform --stop-after-init
```

### สิ่งที่ต้องตรวจ

1. ใช้ config จริงของ Odoo หรือไม่
2. addons path โหลดโมดูลนี้ได้หรือไม่
3. test database สะอาดหรือไม่
4. dependency modules พร้อมหรือไม่

## 12) หลังอัปเกรดโมดูลแล้ว view แปลกหรือ security เพี้ยน

### แนวทางตรวจ

1. อัปเกรดโมดูลใหม่ด้วยคำสั่ง:

```bash
/var/odoo/odoo15/odoo-bin -c /etc/odoo/odoo.conf -d <db_name> -u autoinfo_company_knowledge_platform --stop-after-init
```

2. รีสตาร์ท Odoo
3. ล้าง browser cache
4. ตรวจ log ว่ามี XML/ACL error หรือไม่

## 12.1) เห็นสถานะ `approved` แต่ไม่แน่ใจว่าต้องใช้เมื่อไร

### คำอธิบาย

แม้ model จะยังมี state `approved` อยู่ แต่ current operational flow ของโมดูลนี้ยังเน้น:

- `draft`
- `in_review`
- `published`
- `archived`

ดังนั้นถ้าเห็น `approved` ในบางส่วนของระบบ ให้ถือว่าเป็น reserved state ที่ยังไม่ได้ถูกใช้เป็นขั้นตอนหลักในคู่มือการทำงานของเวอร์ชันนี้

## 13) Checklist เวลาหาสาเหตุ

เมื่อเกิดปัญหา ให้ไล่ลำดับนี้:

1. ปัญหาเกิดที่ model, view, security หรือ data
2. user คนนี้อยู่กลุ่มอะไร
3. user คนนี้อยู่แผนกอะไร
4. clearance ระดับไหน
5. เอกสารอยู่สถานะอะไร
6. เอกสารเป็น company-wide หรือไม่
7. มี extraction text หรือไม่

## Credits

Development Team: The Auto-Info Co., Ltd. : Dev Team / Mr. Nattanon Vinyangkoon - Project conception, implementation, and review of deliverables.

AI Coding Assistant: TRAE - Used to support implementation, testing workflow, and documentation under human oversight.
