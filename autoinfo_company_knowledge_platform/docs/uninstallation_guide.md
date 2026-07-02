# คู่มือถอนการติดตั้ง (Uninstallation Guide)

## 1) จุดประสงค์

เอกสารนี้อธิบายขั้นตอนการถอนการติดตั้งโมดูล `autoinfo_company_knowledge_platform` อย่างปลอดภัย โดยเน้นลดความเสี่ยงต่อข้อมูล knowledge item, version, attachments และข้อมูลที่เกี่ยวข้อง

## 2) สิ่งที่ต้องรู้ก่อนถอนการติดตั้ง

โมดูลนี้สร้างข้อมูลและโครงสร้างต่อไปนี้:

- knowledge items
- knowledge versions
- knowledge attachments
- knowledge extractions
- knowledge templates
- security groups และ record rules

การถอนการติดตั้งอาจทำให้:

- เมนูของโมดูลหายไป
- ฟิลด์และโมเดลของโมดูลไม่สามารถใช้งานต่อได้
- ข้อมูลเฉพาะของโมดูลถูกลบออกจากระบบตามพฤติกรรมของ Odoo

ดังนั้นก่อนถอนการติดตั้ง ต้องตัดสินใจชัดเจนว่าต้องการ:

- ลบโมดูลเพื่อหยุดใช้งานชั่วคราว
- ถอนเพื่อแทนที่ด้วยเวอร์ชันใหม่
- ถอนเพื่อเลิกใช้งานระบบ knowledge platform นี้ทั้งหมด

## 3) Checklist ก่อนถอนการติดตั้ง

ทำรายการต่อไปนี้ก่อนทุกครั้ง:

1. สำรองฐานข้อมูล
2. สำรอง filestore
3. export รายการ knowledge item ที่สำคัญ
4. export หรือ backup เอกสารแนบที่ต้องเก็บระยะยาว
5. แจ้งผู้ใช้งานที่เกี่ยวข้องว่าระบบ knowledge จะหยุดใช้งาน
6. ตรวจสอบว่าไม่มี process หรือ integration ภายนอกที่พึ่งพาโมเดลของโมดูลนี้

## 4) สิ่งที่แนะนำให้ backup เพิ่มเติม

ถ้าต้องการเก็บข้อมูลก่อนถอน แนะนำสำรองอย่างน้อย:

- รายการ knowledge items ที่ `published`
- รายการ knowledge templates
- attachments ที่ผู้ใช้ยังต้องเปิดดู
- extraction text ที่ถูกใช้ค้นหา
- รายชื่อผู้ใช้และกลุ่มสิทธิ์ที่ผูกกับการใช้งาน knowledge

## 5) ขั้นตอนถอนการติดตั้งผ่าน UI

1. เข้า Odoo ด้วยสิทธิ์ Administrator
2. ไปที่ Apps
3. ค้นหา `Autoinfo Company Knowledge Platform`
4. เปิดหน้ารายละเอียดของโมดูล
5. กด `Uninstall`
6. รอให้ Odoo ดำเนินการจนเสร็จ
7. รีสตาร์ท Odoo service 1 ครั้งหลังถอนเสร็จ

## 6) ขั้นตอนถอนการติดตั้งผ่านคำสั่ง

โดยทั่วไป Odoo จะจัดการถอนผ่าน UI ได้ง่ายกว่า แต่ถ้าต้องการรันใน maintenance flow ให้ใช้คำสั่งภายใต้ config จริงของระบบ

ตัวอย่าง:

```bash
/var/odoo/odoo15/odoo-bin shell -c /etc/odoo/odoo.conf -d <db_name>
```

เมื่อเข้า Odoo shell แล้ว สามารถใช้ตัวอย่างต่อไปนี้:

```python
module = env["ir.module.module"].search([("name", "=", "autoinfo_company_knowledge_platform")], limit=1)
if module:
    module.button_immediate_uninstall()
```

ขั้นตอนที่แนะนำ:

1. สำรองฐานข้อมูลก่อน
2. หยุดงานของผู้ใช้ในช่วง maintenance
3. เข้า shell ด้วย config จริง
4. รันคำสั่งถอนโมดูล
5. ออกจาก shell
6. รีสตาร์ท Odoo service
7. ตรวจ log หลัง restart

หมายเหตุ:

- ควรทำบนช่วง maintenance window
- ห้ามถอนบน production โดยไม่มี backup
- ถ้าระบบมี custom integration ที่อ้างถึงโมเดลของโมดูลนี้ ควรปิด integration ก่อนถอน

## 7) การตรวจสอบหลังถอนการติดตั้ง

หลังถอนแล้ว ให้ตรวจสอบ:

1. เมนู `Knowledge` หายไปจากระบบ
2. ไม่มีกลุ่มสิทธิ์ของโมดูลนี้ค้างใช้งานใน flow จริง
3. ไม่มีกระบวนการภายนอกเรียกโมเดลของโมดูลนี้แล้วเกิด error ซ้ำ
4. log ของ Odoo ไม่มี error จาก model/view/security ของโมดูลนี้หลัง restart

## 8) ถ้าต้องการติดตั้งกลับภายหลัง

ถ้าถอนการติดตั้งแล้วต้องการกลับมาใช้อีก:

1. ตรวจสอบไฟล์โมดูลยังอยู่ใน `/var/odoo/custom15_autoinfo`
2. ติดตั้งโมดูลใหม่ตามคู่มือติดตั้ง
3. restore ข้อมูลจาก backup หากต้องการข้อมูลเดิมกลับมา

## 9) แนวทางที่ปลอดภัยกว่าการถอนทันที

ถ้ายังไม่แน่ใจว่าจะเลิกใช้จริง แนะนำพิจารณาทางเลือกต่อไปนี้ก่อน:

- ปิดสิทธิ์เข้าถึงเมนู
- ย้ายผู้ใช้งานออกจากกลุ่มของโมดูล
- archive knowledge items แทนการถอน
- ปิดการใช้งาน process scan/OCR ชั่วคราว

แนวทางนี้ช่วยให้ไม่สูญเสียข้อมูลเร็วเกินไป

## 10) คำแนะนำสำหรับ production

- ห้ามถอนบน production โดยไม่มี backup ฐานข้อมูลและ filestore
- ถ้ามีข้อมูลที่ถูกอ้างอิงในงาน audit/compliance ควร export ออกก่อน
- ถ้ามีเอกสารที่ยังใช้จริง ให้เก็บสำเนาไฟล์แนบออกนอกระบบก่อนถอน

## Credits

Development Team: The Auto-Info Co., Ltd. : Dev Team / Mr. Nattanon Vinyangkoon - Project conception, implementation, and review of deliverables.

AI Coding Assistant: TRAE - Used to support implementation, testing workflow, and documentation under human oversight.
