# คู่มือการใช้งาน (User Guide)

## 1) โมดูลนี้คืออะไร

`Autoinfo Company Knowledge Platform` เป็นโมดูลสำหรับเก็บและแบ่งปันองค์ความรู้ของบริษัทใน Odoo โดยรองรับทั้ง:

- การเขียนบทความโดยตรงในระบบ
- การจัดเอกสารตามแผนก
- การควบคุมสิทธิ์ตามบทบาทงาน
- การกำหนดระดับความลับของเอกสาร
- การนำเข้าเอกสารสแกน
- การค้นหาและถาม AI จากความรู้ที่ผู้ใช้มีสิทธิ์เห็น

## 2) แนวคิดการใช้งานหลัก

ระบบนี้ออกแบบให้ “ความรู้ 1 ชิ้น” ถูกเก็บในรูปแบบ `knowledge item` ซึ่งมีองค์ประกอบหลักดังนี้:

- ชื่อเรื่อง
- สรุป
- เนื้อหา
- แผนกเจ้าของ
- ประเภทความรู้
- ระดับความลับ
- สถานะเอกสาร
- เวอร์ชัน
- ไฟล์แนบ
- ข้อความ OCR

## 3) บทบาทผู้ใช้

### 3.1 Knowledge Viewer

- อ่านเอกสารที่ตนมีสิทธิ์เห็น
- ใช้ search และ AI answer ได้ในขอบเขตสิทธิ์ของตัวเอง

### 3.2 Knowledge Contributor

- สร้าง knowledge item ใหม่ได้
- แก้ได้เฉพาะ draft ของตัวเอง
- ใช้ scan wizard ได้ในแผนกของตัวเอง

### 3.3 Knowledge Reviewer

- ตรวจทานเอกสารในแผนกตัวเอง
- publish ได้เฉพาะเอกสารในแผนกตัวเอง และต้องอยู่สถานะ `in_review`

### 3.4 Knowledge Department Manager

- ทำงานในขอบเขตเดียวกับ reviewer แต่เหมาะกับหัวหน้าแผนก
- publish ได้เฉพาะเอกสารในแผนกตัวเอง และต้องอยู่สถานะ `in_review`

### 3.5 Knowledge Admin

- เห็นและจัดการได้ทุกแผนก
- publish ได้ทุกสถานะ
- ใช้งาน scan wizard ข้ามแผนกได้

## 4) ระดับความลับของเอกสาร

เอกสารมี 4 ระดับ:

- `public`
- `internal`
- `restricted`
- `confidential`

ระบบจะกรองการมองเห็นตามค่า clearance ของผู้ใช้เสมอ

## 5) การสร้าง knowledge item แบบปกติ

### ขั้นตอน

1. ไปที่เมนู `Knowledge`
2. เปิดรายการ knowledge item
3. กด `Create`
4. กรอกข้อมูลหลัก:
   - `Title`
   - `Summary`
   - `Department`
   - `Knowledge Type`
   - `Classification`
   - `Owner`
5. กรอกเนื้อหาในแท็บ `Content`
6. กด `Save`

### ผลลัพธ์ที่ควรรู้

- ระบบจะสร้างเลขที่เอกสารให้อัตโนมัติ
- ระบบจะสร้างเวอร์ชันแรกให้โดยอัตโนมัติ
- เอกสารเริ่มต้นที่สถานะ `draft`

## 5.1) current operational flow ของสถานะเอกสาร

แม้ model จะยังมีสถานะ `approved` อยู่ แต่ในเวอร์ชันปัจจุบันของโมดูล การใช้งานจริงควรยึด flow นี้เป็นหลัก:

- `draft`
- `in_review`
- `published`
- `archived`

สถานะ `approved` ในปัจจุบันให้ถือว่าเป็น **reserved state / future-use state** และยังไม่ใช่ขั้นตอนปฏิบัติงานหลักของ end user

## 6) การส่งเอกสารเข้า review

### ใช้เมื่อไหร่

เมื่อผู้สร้างเขียนเนื้อหาครบแล้วและต้องการส่งต่อให้ผู้ตรวจทาน

### ขั้นตอน

1. เปิด knowledge item ที่เป็น `draft`
2. กดปุ่ม `Submit Review`
3. ระบบจะเปลี่ยนสถานะเป็น `in_review`
4. ระบบจะพยายามบันทึกข้อความลง chatter ของเอกสาร

## 7) การ publish เอกสาร

### กติกาสำคัญ

- Reviewer/Manager publish ได้เฉพาะเอกสารในแผนกตัวเอง
- Reviewer/Manager publish ได้เฉพาะตอนเอกสารอยู่ในสถานะ `in_review`
- Admin publish ได้ทุกสถานะ
- Published item ถูกออกแบบให้ห้ามแก้ตรง ๆ

### ขั้นตอน

1. เปิด knowledge item
2. ตรวจสอบว่าสถานะเป็น `in_review` (สำหรับ reviewer/manager)
3. กด `Publish`
4. ระบบจะ:
   - เปลี่ยนสถานะเป็น `published`
   - สร้างเวอร์ชันใหม่
   - บันทึกผู้อนุมัติและเวลาที่อนุมัติ
   - พยายามโพสต์ข้อความลง chatter

## 8) การใช้งาน Scan Wizard

### ใช้เมื่อไหร่

เมื่อมีเอกสารกระดาษหรือไฟล์สแกนและต้องการสร้าง knowledge item จากเอกสารนั้น

### ข้อจำกัดด้าน UI ที่ต้องทราบก่อน

ในเวอร์ชันปัจจุบัน โมดูลนี้ **ยังไม่มีเมนูมาตรฐานสำหรับ scan wizard ใน UI หลัก**

ดังนั้นคำว่า “ใช้ scan wizard” ในคู่มือนี้หมายถึงกรณีต่อไปนี้:

- ทีมพัฒนาเพิ่ม menu/action เอง
- ใช้งานผ่าน technical access / developer mode
- เรียกใช้งานผ่าน custom flow ภายในองค์กร

ถ้าเข้าระบบแล้วไม่พบเมนู scan wizard ให้ถือว่าเป็นพฤติกรรมปกติของเวอร์ชันนี้

### ขั้นตอน

1. เปิดเมนูหรือ action ของ scan wizard ตามสิทธิ์ที่ได้รับ
2. กรอกข้อมูล:
   - `Title`
   - `Summary`
   - `Department`
   - `Knowledge Type`
   - `Classification`
   - `Scan File`
3. กด `Create`

### สิ่งที่ระบบจะทำ

- สร้าง knowledge item ใหม่
- สร้าง attachment relation
- สร้าง extraction record สถานะ `pending`

### ข้อจำกัดปัจจุบัน

- OCR engine ยังไม่อยู่ในโมดูล
- ถ้าต้องการให้ search/AI ใช้ OCR text ได้ ต้องมีการเติม `extracted_text` ใน extraction record
- Contributor ถูกจำกัดให้สร้างได้เฉพาะในแผนกตัวเอง

## 8.1) การใช้ Template

โมดูลนี้มี seed templates อยู่แล้ว เช่น:

- Default SOP Template
- Default FAQ Template
- Default Policy Template

แต่ในเวอร์ชันปัจจุบัน **ยังไม่มี standard end-user flow จากเมนูหลัก** สำหรับเลือก template แล้วสร้างเอกสารแบบครบวงจร

ดังนั้น template ในตอนนี้ให้มองเป็น:

- backend data ที่พร้อมสำหรับการต่อยอด
- technical seed data สำหรับใช้ใน future UI/custom flow
- ข้อมูลมาตรฐานที่ทีมพัฒนาหรือผู้ดูแลระบบสามารถอ้างอิงได้

## 9) การค้นหา (Search)

### พฤติกรรมหลัก

search ของโมดูลนี้เป็นแบบ permission-first:

- ดึงเฉพาะเอกสารที่ผู้ใช้มีสิทธิ์เห็น
- รวมข้อความจาก:
  - `title`
  - `summary`
  - `body`
  - `knowledge.extraction.extracted_text`
- ถ้าคำค้นว่างหรือมีแต่ช่องว่าง ระบบจะไม่คืนผลลัพธ์ทั้งหมด

### การใช้งาน

1. ไปที่เมนู `Knowledge > Search`
2. พิมพ์คำค้น
3. เปิดดูรายการผลลัพธ์ที่ `published`
4. เปิดเอกสารที่ต้องการอ่านต่อ

## 10) การใช้ AI Answer

### แนวคิด

AI Answer จะตอบจากเอกสารที่ผู้ใช้มีสิทธิ์เข้าถึงจริงเท่านั้น

### สิ่งที่ระบบคืนกลับ

- คำตอบย่อ
- รายการ citation
- confidence แบบพื้นฐาน

### ข้อควรทราบ

- ถ้าไม่พบข้อมูล ระบบจะตอบ fallback message
- ถ้า OCR text มีข้อมูลแต่ `body/summary` ว่าง AI สามารถใช้ OCR text เป็นแหล่งตอบได้

## 11) การอ่าน version history

ในฟอร์มของ knowledge item จะมีแท็บ `Versions` ซึ่งใช้ดู:

- หมายเลขเวอร์ชัน
- สถานะของเวอร์ชัน
- ผู้อนุมัติ
- เวลาอนุมัติ

## 12) สิ่งที่ผู้ใช้ควรระวัง

- Contributor ไม่ควรคาดหวังว่าจะกลับไปแก้ published item ตรง ๆ ได้
- Reviewer/Manager ต้องให้เอกสารอยู่ `in_review` ก่อนจึง publish ได้
- ถ้า search หาเอกสารสแกนไม่เจอ ให้ตรวจว่า `extracted_text` ถูกเติมแล้วหรือยัง
- ถ้าเอกสารไม่ปรากฏใน search อาจเกิดจาก:
  - ยังไม่ `published`
  - ไม่มีสิทธิ์เห็น
  - คำค้นว่าง

## 13) ตัวอย่างการใช้งานจริง

### ตัวอย่างที่ 1: สร้าง SOP ใหม่

1. Contributor สร้างเอกสาร `Customer Return SOP`
2. บันทึกเป็น `draft`
3. กด `Submit Review`
4. Reviewer ตรวจสอบ
5. Reviewer กด `Publish`
6. เอกสารถูกใช้งานใน search และ AI answer ได้

### ตัวอย่างที่ 2: นำเข้าจากไฟล์สแกน

1. Contributor ใช้ scan wizard
2. สร้าง knowledge item พร้อม attachment และ extraction
3. ฝ่ายเทคนิคหรือ process OCR เติม `extracted_text`
4. ผู้ใช้ค้นหาเอกสารจากคำที่อยู่ใน OCR text ได้

## 14) สรุป

ถ้าจะใช้โมดูลนี้ให้มีประสิทธิภาพ:

- กำหนดแผนกและสิทธิ์ผู้ใช้ให้ชัด
- ใช้ workflow ก่อน publish ทุกครั้ง
- เติม OCR text ให้ extraction ถ้าต้องการใช้ search/AI กับเอกสารสแกน
- ทดสอบสิทธิ์ข้ามแผนกก่อนใช้งานจริง

## Credits

Development Team: The Auto-Info Co., Ltd. : Dev Team / Mr. Nattanon Vinyangkoon – Project conception, implementation, and thorough review of all deliverables.

AI Coding Assistant: TRAE SOLO / MICROSOFT 365 COPILOT - Utilized to support code generation and productivity improvements under human oversight.
