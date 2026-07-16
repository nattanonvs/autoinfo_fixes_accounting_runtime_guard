# คู่มือทางเทคนิค (Technical Guide)

## 1) ภาพรวมเชิงสถาปัตยกรรม

โมดูล `autoinfo_company_knowledge_platform` ถูกออกแบบเป็น knowledge layer บน Odoo 15 โดยมีเป้าหมายหลักดังนี้:

- เก็บองค์ความรู้เป็น record ที่มีโครงสร้าง
- บังคับ workflow และสิทธิ์ระดับแผนก/บทบาท/clearance
- รองรับไฟล์สแกนและ OCR extraction
- ทำ search และ AI answer บนข้อมูลที่ผ่าน permission filter แล้ว

## 2) โครงสร้างโมดูล

### Models

- `knowledge.item`
- `knowledge.version`
- `knowledge.department`
- `knowledge.type`
- `knowledge.tag`
- `knowledge.template`
- `knowledge.attachment`
- `knowledge.extraction`
- `knowledge.search.service`
- `knowledge.ai.service`
- `res.users` extension

### Wizards

- `knowledge.create.from.scan`
- `knowledge.submit.review`
- `knowledge.publish`

### Security

- `knowledge_security.xml`
- `knowledge_record_rules.xml`
- `ir.model.access.csv`

### Views

- `knowledge_item_views.xml`
- `knowledge_menu.xml`
- `knowledge_taxonomy_views.xml`
- `knowledge_template_views.xml`
- wizard views

### Current UI entry points

แม้โมดูลจะมี view/model/data หลายส่วน แต่ entry point ที่เปิดใช้ชัดเจนใน UI มาตรฐานตอนนี้ยังมีจำกัด:

- มีเมนู `Knowledge`
- มีเมนู `Knowledge > Search`
- มีฟอร์ม/รายการของ `knowledge.item`

ส่วนต่อไปนี้ยังถือเป็น backend/view assets ที่ยังไม่ถูกเปิดเป็น standard end-user menu:

- taxonomy management
- template management
- scan wizard entry point

## 3) Core Models

### 3.1 `knowledge.item`

เป็น aggregate root ของโมดูล มีหน้าที่เก็บข้อมูลหลักขององค์ความรู้

ฟิลด์สำคัญ:

- `name`
- `title`
- `summary`
- `body`
- `department_id`
- `knowledge_type_id`
- `classification`
- `state`
- `owner_id`
- `current_version_id`
- `attachment_rel_ids`
- `extraction_ids`

### 3.2 `knowledge.version`

ใช้เก็บ snapshot ของเอกสารแต่ละเวอร์ชัน เช่น:

- version number
- title snapshot
- body snapshot
- approved by
- approved at
- state

### 3.3 `knowledge.attachment`

เก็บ relation ระหว่าง knowledge item กับไฟล์แนบจริงใน `ir.attachment`

### 3.4 `knowledge.extraction`

เก็บผลการแปลงข้อความจากไฟล์ เช่น OCR/parsing โดยฟิลด์ที่สำคัญที่สุดคือ:

- `source_format`
- `extracted_text`
- `status`
- `confidence_score`

### 3.5 `knowledge.template`

เก็บ template เริ่มต้นสำหรับประเภทเอกสาร เช่น SOP, FAQ, Policy

## 4) Workflow

### สถานะหลัก

- `draft`
- `in_review`
- `approved`
- `published`
- `archived`

### Action ที่ใช้จริง

- `action_submit_review()`
- `action_publish(change_summary=None)`

### Current operational flow

ถึงแม้ state field จะยังมี `approved` อยู่ แต่ current operational flow ที่ผู้ใช้ควรยึดในเวอร์ชันนี้คือ:

- `draft -> in_review -> published -> archived`

ดังนั้น `approved` ให้ถือเป็น reserved state ที่ยังไม่ได้ถูกผูกเข้ากับ flow ทำงานหลักของโมดูลในตอนนี้

### กติกา publish ปัจจุบัน

- Admin publish ได้ทุกสถานะ
- Reviewer/Manager publish ได้เฉพาะ:
  - แผนกของตัวเอง
  - สถานะ `in_review`

### กติกาการแก้ไข

- Contributor แก้ได้เฉพาะ draft ของตัวเอง
- Reviewer/Manager แก้ได้เฉพาะเอกสารในแผนกตัวเอง
- Published item ถูกบล็อกไม่ให้แก้ตรง ๆ
- การแก้ `state` ผ่าน `.write()` ถูกบล็อก และต้องผ่าน workflow action เท่านั้น

## 5) Security Model

### 5.1 Security Groups

กลุ่มหลักที่โมดูลสร้าง:

- `Knowledge Viewer`
- `Knowledge Contributor`
- `Knowledge Reviewer`
- `Knowledge Department Manager`
- `Knowledge Admin`

กลุ่มเหล่านี้มีความสัมพันธ์แบบ implied group ต่อเนื่องกัน

### 5.2 User fields ที่มีผลต่อ security

โมดูลเพิ่มฟิลด์บน `res.users`:

- `knowledge_department_id`
- `knowledge_clearance_level`

ทั้งสองฟิลด์มีผลโดยตรงต่อ:

- การมองเห็น knowledge item
- การมองเห็น child models
- การ publish
- การใช้ scan wizard

### 5.3 ACL vs Record Rule

โมดูลนี้ใช้ทั้ง:

- ACL สำหรับกำหนดสิทธิ์ระดับ model
- Record rule สำหรับกำหนดสิทธิ์ระดับ record

แนวคิดสำคัญคือ:

- ACL เป็นด่านแรก
- Record rule เป็นด่านกรองตามแผนก/ระดับความลับ/ความสัมพันธ์กับ parent

### 5.4 Child model rules

เพิ่ม record rule สำหรับ:

- `knowledge.version`
- `knowledge.attachment`
- `knowledge.extraction`

เพื่อไม่ให้ผู้ใช้เข้าถึงข้อมูลลูกข้ามสิทธิ์ของ `knowledge.item`

## 6) Search Design

### โมเดลที่เกี่ยวข้อง

- `knowledge.search.service`

### หลักการทำงาน

1. รับ query
2. tokenize/normalize query
3. ถ้าคำค้นว่าง ให้คืนผลลัพธ์ว่าง
4. search เฉพาะ knowledge item ที่ `published`
5. กรองด้วยสิทธิ์ของผู้ใช้
6. match จาก:
   - title
   - summary
   - body
   - OCR `extracted_text`

### จุดเด่น

- เป็น permission-first search
- ป้องกันกรณี query ว่างแล้ว match ทั้งระบบ
- รองรับ OCR text ทันทีเมื่อมีข้อมูลใน extraction

## 7) AI Answer Design

### โมเดลที่เกี่ยวข้อง

- `knowledge.ai.service`

### หลักการทำงาน

1. เรียก `knowledge.search.service`
2. เลือก candidate แรกที่ match
3. สร้าง answer แบบสรุปสั้น
4. คืน:
   - `answer`
   - `citations`
   - `confidence`

### พฤติกรรม fallback

ถ้าไม่พบ source ที่ผู้ใช้มีสิทธิ์เห็น:

- ตอบข้อความ fallback
- ส่ง `citations = []`
- ส่ง `confidence = 0.0`

## 8) Scan Ingestion Design

### Wizard

`knowledge.create.from.scan`

### Flow การทำงาน

1. ผู้ใช้กรอก metadata เบื้องต้น
2. ระบบตรวจแผนกของผู้ใช้
3. สร้าง `knowledge.item`
4. สร้าง `ir.attachment`
5. สร้าง `knowledge.attachment`
6. เรียก `action_queue_extraction()`
7. สร้าง `knowledge.extraction` สถานะ `pending`

### ข้อจำกัด

- ยังไม่มี OCR engine ในตัวโมดูล
- ถ้าต้องการ OCR text จริง ต้องเติม `extracted_text` ผ่าน process ภายนอกหรือ custom extension
- wizard view ของ scan มีอยู่แล้ว แต่ยังไม่มี standard menu/action ใน UI หลักสำหรับ end users

## 9) Seed Data

ไฟล์ `data/knowledge_template_data.xml` สร้าง:

- knowledge types:
  - SOP
  - FAQ
  - Policy
- templates:
  - Default SOP Template
  - Default FAQ Template
  - Default Policy Template

## 10) Test Coverage Overview

โมดูลนี้มีชุดทดสอบครอบคลุมหัวข้อหลัก เช่น:

- core model creation
- workflow
- publish permissions
- record rules ของโมเดลลูก
- scan wizard ACL
- ingestion
- search
- AI answer
- write policy และ state bypass prevention

## 11) Known Limitations

- OCR ยังเป็น queue hook ไม่ใช่ OCR processor เต็มรูปแบบ
- AI answer ยังเป็น heuristic แบบง่าย ไม่ใช่ LLM orchestration เต็มระบบ
- UI ยังไม่มีหน้าจัดการ template-based creation flow แบบครบวงจร
- UI ยังไม่มี standard menu สำหรับ scan wizard และ taxonomy/template management
- ยังไม่มี dashboard เชิงวิเคราะห์

## 12) แนวทางขยายในอนาคต

ถ้าจะพัฒนาต่อ แนะนำลำดับดังนี้:

1. ต่อ OCR engine จริง
2. ทำ background job สำหรับ extraction
3. ทำ semantic search
4. ทำ approval หลายชั้น
5. ทำ analytics dashboard

## Credits

Development Team: The Auto-Info Co., Ltd. : Dev Team / Mr. Nattanon Vinyangkoon – Project conception, implementation, and thorough review of all deliverables.

AI Coding Assistant: TRAE SOLO / MICROSOFT 365 COPILOT - Utilized to support code generation and productivity improvements under human oversight.
