# Timeline and Changelog

## 1) Purpose

เอกสารนี้สรุปลำดับการพัฒนาโมดูล `autoinfo_company_knowledge_platform` และบันทึกการเปลี่ยนแปลงสำคัญ เพื่อใช้สำหรับ:

- ส่งมอบงาน
- audit ย้อนหลัง
- วางแผนอัปเกรดในอนาคต
- อ้างอิงเวลาทำ troubleshooting

## 2) Project Timeline

### 2026-06-27 - Initial design and implementation cycle

ออกแบบและพัฒนาโมดูลพื้นฐานสำหรับระบบคลังความรู้ของบริษัท โดยมีหัวข้อสำคัญดังนี้:

- ออกแบบแนวคิด `Knowledge Item` เป็นแกนกลาง
- กำหนด workflow พื้นฐานของเอกสาร
- กำหนด security model แบบ department + role + classification
- เพิ่มการนำเข้าจาก scan
- เพิ่ม search และ AI answer
- เพิ่ม hardening เพื่อกัน bypass สิทธิ์และ workflow
- เพิ่มเอกสารประกอบโมดูล

## 3) Changelog by Functional Area

### 3.1 Core Module

เพิ่มโครงโมดูลพื้นฐาน:

- manifest
- init files
- models package
- views package
- wizards
- security
- tests

### 3.2 Core Data Model

เพิ่มโมเดลหลัก:

- `knowledge.item`
- `knowledge.version`
- `knowledge.department`
- `knowledge.type`
- `knowledge.tag`
- `knowledge.template`
- `knowledge.attachment`
- `knowledge.extraction`

### 3.3 Workflow

เพิ่ม workflow หลัก:

- draft
- in_review
- published
- archived

หมายเหตุ:

- state `approved` ยังมีอยู่ใน model แต่ยังไม่ถูกใช้เป็น current operational flow หลักของโมดูลในเวอร์ชันนี้

พร้อม methods:

- `action_submit_review()`
- `action_publish()`

### 3.4 Security

เพิ่ม security groups:

- Knowledge Viewer
- Knowledge Contributor
- Knowledge Reviewer
- Knowledge Department Manager
- Knowledge Admin

เพิ่ม:

- ACL
- record rules
- child-model record rules
- write policy แบบเข้ม
- state bypass protection

### 3.5 Scan / OCR

เพิ่ม scan wizard และ ingestion flow:

- สร้าง knowledge item จากไฟล์สแกน
- สร้าง attachment relation
- สร้าง extraction record
- รองรับ OCR text ผ่าน `extracted_text`

### 3.6 Search / AI

เพิ่ม:

- permission-first search
- tokenized query matching
- OCR text search support
- blank query guard
- AI answer พร้อม citation
- fallback behavior

### 3.7 Documentation

จัดทำเอกสารของโมดูลให้ครบ:

- README
- installation guide
- uninstallation guide
- user guide
- technical guide
- troubleshooting guide
- timeline and changelog

พร้อมทั้งปรับ wording ให้แยกชัดระหว่าง:

- ฟีเจอร์ที่ใช้งานผ่าน UI ได้ทันที
- ฟีเจอร์ที่มี backend capability/data แล้ว
- ฟีเจอร์ที่ยังต้องต่อ UI flow เพิ่ม

## 4) Hardening Milestones

### Milestone: Publish permission tightening

เปลี่ยน policy ให้:

- Reviewer/Manager publish ได้เฉพาะแผนกตัวเอง
- Reviewer/Manager publish ได้เฉพาะตอน `in_review`
- Admin publish ได้ทุกสถานะ

### Milestone: Safe chatter posting

คืนการใช้ chatter ใน workflow โดย:

- พยายามโพสต์ลง chatter ตามปกติ
- ถ้าเกิดปัญหาด้าน mail/author ระบบไม่ทำให้ workflow ล้ม

### Milestone: Strict write policy

เพิ่ม policy:

- Contributor แก้ได้เฉพาะ draft ของตัวเอง
- Reviewer/Manager แก้ได้เฉพาะเอกสารในแผนกตัวเอง
- Published item ห้ามแก้ตรง ๆ

### Milestone: Child-model protection

เพิ่ม record rules ให้โมเดลลูกเพื่อกัน:

- อ่าน OCR text ข้ามแผนก
- อ่าน version snapshot ข้ามแผนก
- แก้ attachment relation ของเอกสารที่ไม่มีสิทธิ์

### Milestone: Scan department restriction

จำกัด scan wizard ไม่ให้ contributor สร้างเอกสารข้ามแผนก

### Milestone: OCR-aware search and AI

ให้ search และ AI สามารถใช้ `extracted_text` ได้ทันที เมื่อมีข้อมูลอยู่ในระบบ

## 5) Test Progress Summary

มีการพัฒนาชุดทดสอบแบบ TDD ต่อเนื่องระหว่างการพัฒนา:

- เริ่มจาก core model tests
- เพิ่ม workflow tests
- เพิ่ม permission tests
- เพิ่ม ingestion tests
- เพิ่ม search tests
- เพิ่ม AI answer tests
- เพิ่ม publish permission tests
- เพิ่ม write policy tests
- เพิ่ม child record rules tests
- เพิ่ม scan wizard ACL/escalation tests

สถานะล่าสุด:

- full module test suite ผ่าน

## 6) Known Functional Boundaries

สิ่งที่โมดูลนี้ทำได้แล้ว:

- knowledge management พื้นฐาน
- workflow
- security
- scan ingestion
- OCR text integration
- search
- AI answer แบบพื้นฐาน

สิ่งที่ยังไม่ได้ทำ:

- OCR engine ภายใน
- semantic/vector search
- approval chain หลายชั้น
- dashboard วิเคราะห์การใช้งาน

## 7) Recommended Next Phase

สำหรับเฟสถัดไป แนะนำลำดับนี้:

1. ทำ OCR pipeline จริง
2. เพิ่ม background job processing
3. ทำ UI สำหรับใช้ templates แบบสมบูรณ์
4. เพิ่ม analytics
5. เพิ่ม semantic search / retrieval ranking ที่ลึกขึ้น

## Credits

Development Team: The Auto-Info Co., Ltd. : Dev Team / Mr. Nattanon Vinyangkoon - Project conception, implementation, and review of deliverables.

AI Coding Assistant: TRAE - Used to support implementation, testing workflow, and documentation under human oversight.
