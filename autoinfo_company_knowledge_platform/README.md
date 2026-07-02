# Autoinfo Company Knowledge Platform

## Overview

`autoinfo_company_knowledge_platform` เป็นโมดูล Odoo 15 สำหรับสร้างพื้นที่จัดเก็บองค์ความรู้กลางขององค์กร โดยออกแบบให้รองรับการทำงานจริงในระดับบริษัท ทั้งในด้านการกำหนดสิทธิ์ การกำกับดูแลเนื้อหา การนำเข้าความรู้จากเอกสารสแกน และการค้นหาความรู้แบบกึ่ง AI

โมดูลนี้เหมาะสำหรับองค์กรที่ต้องการ:

- แยกองค์ความรู้ตามแผนก
- กำหนดสิทธิ์ตามบทบาทงานและระดับความลับของเอกสาร
- เก็บความรู้ได้ทั้งแบบพิมพ์ในระบบและจากเอกสารสแกน
- ค้นหาแบบ permission-first เพื่อไม่ให้ข้อมูลรั่วข้ามแผนก
- ใช้ AI Answer พร้อม citation จากแหล่งข้อมูลที่ผู้ใช้มีสิทธิ์เห็นจริง

## Key Features

- พื้นที่จัดเก็บ knowledge item แบบแยกตามแผนก
- Workflow พื้นฐาน `draft -> in_review -> published -> archived`
- เวอร์ชันของเอกสารและ snapshot ของเนื้อหา
- Security model แบบ 3 มิติ:
  - Department
  - Role
  - Classification
- Scan ingestion wizard สำหรับสร้าง knowledge item จากไฟล์สแกน
- OCR extraction queue hook สำหรับต่อ OCR pipeline ภายนอก
- Search แบบ permission-first
- AI Answer พร้อม citation และ fallback เมื่อไม่พบข้อมูล

## Current UI Availability

สถานะปัจจุบันของโมดูลนี้ควรเข้าใจดังนี้:

- **มีเมนูพร้อมใช้ใน UI มาตรฐาน**
  - `Knowledge > Search`
  - ฟอร์ม `knowledge.item` และรายการเอกสารที่เกี่ยวข้อง
- **มี model/data พร้อม แต่ยังไม่มี standard menu entry ครบ**
  - `knowledge.template`
  - `knowledge.type`
  - `knowledge.department`
  - `knowledge.create.from.scan`
- **มี backend capability แต่ยังไม่ใช่ end-user flow เต็มรูปแบบ**
  - template-based creation flow
  - OCR processing engine ภายในโมดูล

ดังนั้น README และคู่มือชุดนี้จะอธิบายแยกชัดเจนระหว่าง:

- สิ่งที่ “ใช้งานผ่าน UI ได้ทันที”
- สิ่งที่ “มีใน backend/technical layer แล้ว”
- สิ่งที่ “ยังเป็น next phase”

## Current Scope

### Included in current module

- โมเดลหลักสำหรับ knowledge management
- Search service และ AI answer service
- สิทธิ์ตามกลุ่มผู้ใช้
- Record rules สำหรับ knowledge item และโมเดลลูกที่สำคัญ
- Seed data สำหรับ knowledge type และ template พื้นฐาน
- ชุดทดสอบอัตโนมัติของโมดูล

### Not included yet

- OCR engine ภายในโมดูล
- Semantic embedding / vector database
- User interface สำหรับใช้ template ในการสร้างเอกสารแบบครบ flow
- ระบบ approval หลายชั้น
- Dashboard / analytics เชิงบริหาร

## Dependencies

- Odoo 15
- โมดูลพื้นฐาน:
  - `mail`
  - `web`

## Directory

- โมดูลหลัก:
  - `/var/odoo/custom15_autoinfo/autoinfo_company_knowledge_platform`

## Documentation Set

เอกสารประกอบของโมดูลนี้ถูกแยกไว้ในโฟลเดอร์ `docs/` เพื่อให้ใช้งานและส่งมอบได้ง่าย:

- `docs/installation_guide.md`
- `docs/uninstallation_guide.md`
- `docs/user_guide.md`
- `docs/technical_guide.md`
- `docs/troubleshooting.md`
- `docs/timeline_and_changelog.md`

## Recommended Reading Order

1. `docs/installation_guide.md`
2. `docs/user_guide.md`
3. `docs/technical_guide.md`
4. `docs/troubleshooting.md`
5. `docs/timeline_and_changelog.md`

## Install Summary

1. วางโมดูลไว้ที่ `/var/odoo/custom15_autoinfo`
2. ตรวจสอบว่า path นี้อยู่ใน `addons_path` ของ `/etc/odoo/odoo.conf`
3. อัปเดต apps list
4. ติดตั้งโมดูล `Autoinfo Company Knowledge Platform`

ตัวอย่างคำสั่ง:

```bash
/var/odoo/odoo15/odoo-bin -c /etc/odoo/odoo.conf -d <db_name> -i autoinfo_company_knowledge_platform --stop-after-init
```

## Rollout Summary

1. สร้างหรือเตรียมรายการแผนกที่จะใช้จริง
2. ตรวจสอบ knowledge types และ templates เริ่มต้น
3. กำหนดกลุ่มสิทธิ์ให้ผู้ใช้
4. ทดลองใช้งานกับ 2-3 แผนกก่อน
5. ทดสอบกรณีข้ามแผนกและเอกสาร restricted/confidential
6. ทดสอบ scan ingestion และ search/AI answer จาก OCR text

## Important Notes

- Reviewer/Manager สามารถ publish ได้เฉพาะเอกสารในแผนกตัวเอง และต้องอยู่ในสถานะ `in_review`
- Admin สามารถ publish ได้ทุกสถานะ
- Published item ถูกออกแบบให้ห้ามแก้ตรง ๆ
- สถานะ `approved` ยังมีอยู่ใน model/state definition แต่ **ยังไม่ใช่ current operational flow หลัก** ของโมดูลในเวอร์ชันนี้
- OCR text จะถูกนำไปใช้ใน search/AI ได้เมื่อมีการเติมค่า `extracted_text` ลงใน `knowledge.extraction`
- โมดูลนี้มี OCR queue hook แต่ยังไม่ได้มี OCR engine ภายในตัวเอง

## Credits

Development Team: The Auto-Info Co., Ltd. : Dev Team / Mr. Nattanon Vinyangkoon - Project conception, implementation, and review of deliverables.

AI Coding Assistant: TRAE - Used to support implementation, testing workflow, and documentation under human oversight.
