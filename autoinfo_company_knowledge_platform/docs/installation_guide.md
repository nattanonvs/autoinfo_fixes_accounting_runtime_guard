# คู่มือติดตั้ง (Installation Guide)

<div style="border:2px solid #d00; padding:12px; border-radius:8px;">
<div style="color:#d00; font-weight:800; font-size:18px;">
คำเตือนสำคัญมาก (อ่านก่อนติดตั้ง)
</div>
<div style="color:#d00;">
1) ก่อนติดตั้งหรืออัปเกรด ต้องสำรองฐานข้อมูลก่อนทุกครั้ง<br/>
2) หลังวางโค้ดใหม่ ต้องสั่งอัปเกรดโมดูลด้วย ไม่งั้นอาจขึ้น error และทำให้ระบบล้ม เช่น <code>UndefinedColumn</code><br/>
3) ตัวอย่างคำสั่งอัปเกรด: <code>/var/odoo/odoo15/odoo-bin -c /etc/odoo/odoo.conf -d FROMGOLIVE_9MAY2026 -u autoinfo_company_knowledge_platform --stop-after-init</code><br/>
4) ถ้าแก้ <code>addons_path</code> หรือเพิ่มโค้ดใหม่ ต้องรีสตาร์ท Odoo service<br/>
</div>
</div>

## 1) ภาพรวม

โมดูล `autoinfo_company_knowledge_platform` ใช้สำหรับสร้างระบบคลังความรู้กลางขององค์กรบน Odoo 15 โดยรองรับ:

- knowledge item แยกตามแผนก
- workflow การเผยแพร่เนื้อหา
- สิทธิ์ตามบทบาท + ระดับความลับ
- การนำเข้าจากเอกสารสแกน
- search และ AI answer ที่เคารพสิทธิ์ผู้ใช้

## 2) ข้อกำหนดก่อนติดตั้ง

ก่อนติดตั้ง ต้องตรวจสอบสิ่งต่อไปนี้:

1. ใช้ Odoo 15
2. มีสิทธิ์ระดับ Administrator สำหรับติดตั้งโมดูล
3. ระบบโหลด custom addons path ได้ปกติ
4. มีโมดูลพื้นฐานต่อไปนี้พร้อมใช้งาน:
   - `mail`
   - `web`
5. ไฟล์ config ของ Odoo สามารถอ้างถึง custom addons path ได้ครบ

## 3) ตำแหน่งวางโมดูล

- โฟลเดอร์รวม custom addons:
  - `/var/odoo/custom15_autoinfo`
- โฟลเดอร์ของโมดูล:
  - `/var/odoo/custom15_autoinfo/autoinfo_company_knowledge_platform`

## 4) ตรวจสอบ `addons_path`

แก้ไขไฟล์ config:

- `/etc/odoo/odoo.conf`

ตรวจสอบให้ `addons_path` มี path ของ custom addons ตัวอย่างเช่น:

```ini
addons_path = /var/odoo/odoo15/addons,/var/odoo/custom15_autoinfo
```

ถ้าระบบของคุณมีหลาย path อยู่แล้ว ให้เพียงเพิ่ม `/var/odoo/custom15_autoinfo` เข้าไป ไม่จำเป็นต้องแทนค่าทั้งหมด

## 5) ขั้นตอนติดตั้ง

### วิธีที่ 0: ติดตั้งจาก GitHub (แนะนำ)

1. เข้าเครื่องเซิร์ฟเวอร์
2. ไปที่โฟลเดอร์ addons:

```bash
cd /var/odoo/custom15_autoinfo
```

3. ดึงโค้ดจาก GitHub:

```bash
git clone https://github.com/nattanonvs/autoinfo_company_knowledge_platform.git
```

4. ตรวจว่ามีโฟลเดอร์นี้จริง:

- `/var/odoo/custom15_autoinfo/autoinfo_company_knowledge_platform`

5. รีสตาร์ท Odoo service 1 ครั้ง

6. ติดตั้งหรืออัปเกรดโมดูลด้วยคำสั่ง:

```bash
/var/odoo/odoo15/odoo-bin -c /etc/odoo/odoo.conf -d <db_name> -i autoinfo_company_knowledge_platform --stop-after-init
```

### วิธีที่ 1: ติดตั้งผ่านคำสั่ง

```bash
/var/odoo/odoo15/odoo-bin -c /etc/odoo/odoo.conf -d <db_name> -i autoinfo_company_knowledge_platform --stop-after-init
```

ตัวอย่าง:

```bash
/var/odoo/odoo15/odoo-bin -c /etc/odoo/odoo.conf -d FROMGOLIVE_9MAY2026 -i autoinfo_company_knowledge_platform --stop-after-init
```

### วิธีที่ 2: ติดตั้งผ่าน Apps

1. รีสตาร์ท Odoo service
2. เข้าเมนู Apps
3. กด `Update Apps List`
4. ค้นหา `Autoinfo Company Knowledge Platform`
5. กด `Install`

## 6) ข้อมูลที่โมดูลจะติดตั้งให้

หลังติดตั้ง โมดูลจะสร้างข้อมูลหลักดังนี้:

- Security groups:
  - `Knowledge Viewer`
  - `Knowledge Contributor`
  - `Knowledge Reviewer`
  - `Knowledge Department Manager`
  - `Knowledge Admin`
- Seed knowledge types:
  - `SOP`
  - `FAQ`
  - `Policy`
- Seed templates:
  - `Default SOP Template`
  - `Default FAQ Template`
  - `Default Policy Template`

## 7) ตรวจสอบหลังติดตั้ง

ตรวจสอบอย่างน้อยตามรายการนี้:

1. เมนู `Knowledge` ปรากฏในระบบ
2. เปิดเมนูค้นหาแล้วไม่เกิด error
3. เข้าไปที่กลุ่มสิทธิ์แล้วเห็นกลุ่มของโมดูลครบ
4. เปิด `Knowledge Item` แล้วเห็นฟิลด์หลักครบ เช่น:
   - `title`
   - `summary`
   - `department`
   - `knowledge type`
   - `classification`
   - `state`
5. ตรวจสอบว่า seed knowledge types และ templates ถูกสร้างแล้ว

## 7.1) สิ่งที่ติดตั้งแล้วแต่ยังไม่มีเมนูมาตรฐาน

หลังติดตั้ง โมดูลจะมีทั้งส่วนที่เปิดใช้ผ่าน UI ได้ทันที และส่วนที่มีอยู่ใน backend/data layer แล้วแต่ยังไม่มี menu entry มาตรฐาน

### ใช้งานผ่าน UI ได้ทันที

- เมนู `Knowledge`
- เมนู `Knowledge > Search`
- ฟอร์มและรายการ `knowledge.item`

### มีอยู่แล้วแต่ยังไม่เปิดเป็น standard menu

- `knowledge.template`
- `knowledge.type`
- `knowledge.department`
- `knowledge.create.from.scan`

ดังนั้นถ้าติดตั้งแล้ว “หาเมนู template หรือ scan wizard ไม่เจอ” ไม่ได้แปลว่าติดตั้งผิด แต่เป็นพฤติกรรมปัจจุบันของโมดูลเวอร์ชันนี้

## 8) การตั้งค่าหลังติดตั้งที่แนะนำ

### 8.1 สร้างแผนกที่ใช้จริง

ถ้ายังไม่มีข้อมูลแผนกในโมดูล knowledge ให้สร้างแผนกตามหน่วยงานจริงของบริษัท เช่น:

- Sales
- HR
- Finance
- Operations
- Projects

### 8.2 กำหนดกลุ่มสิทธิ์ให้ผู้ใช้

กำหนดสิทธิ์ตามบทบาทงานจริง เช่น:

- พนักงานทั่วไป: `Knowledge Viewer`
- ผู้สร้างเนื้อหา: `Knowledge Contributor`
- ผู้ตรวจทาน: `Knowledge Reviewer`
- หัวหน้าแผนก: `Knowledge Department Manager`
- ผู้ดูแลระบบ: `Knowledge Admin`

### 8.3 ตั้งค่าแผนกและ clearance ให้ผู้ใช้

โมดูลนี้อ้างอิงฟิลด์ต่อไปนี้บนผู้ใช้:

- `knowledge_department_id`
- `knowledge_clearance_level`

ควรกรอกค่าให้ครบก่อนเปิดใช้งานจริง โดยเฉพาะผู้ที่จะใช้ search, publish และ scan wizard

## 9) การทดสอบ smoke test หลังติดตั้ง

แนะนำให้ทดสอบอย่างน้อยดังนี้:

1. สร้าง knowledge item แบบ draft
2. ส่งเข้า review
3. publish ด้วย reviewer/manager ในแผนกเดียวกัน
4. ทดสอบ user ต่างแผนกว่าไม่เห็นเอกสาร restricted
5. ทดสอบ scan wizard ด้วย contributor
6. ทดสอบ search ด้วยคำที่อยู่ใน `body`
7. ทดสอบ search/AI ด้วย OCR text ที่ถูกเติมใน `knowledge.extraction`

หมายเหตุ:

- ข้อ 5 อาจต้องทดสอบผ่าน technical access, developer mode, server action หรือ custom menu ที่ทีมของคุณเพิ่มเอง เพราะโมดูลยังไม่ได้เปิด menu มาตรฐานสำหรับ scan wizard

## 10) ข้อควรระวัง

- ถ้าไม่ได้กำหนด `knowledge_department_id` ให้ผู้ใช้ การตัดสินสิทธิ์อาจไม่เป็นไปตามที่คาด
- ถ้าไม่ได้เติม `extracted_text` จริง search/AI จะยังไม่ใช้ OCR content ได้
- ถ้ามีการแก้ `addons_path` ต้องรีสตาร์ท Odoo ก่อน
- ควรติดตั้งบน staging ก่อน deploy production
- อย่าคาดหวังว่า seed templates ที่ถูกสร้างแล้วจะมี end-user flow ใช้งานจากเมนูครบถ้วนในเวอร์ชันนี้ เว้นแต่จะมีการเพิ่ม UI entry points เพิ่มเติม

## Credits

Development Team: The Auto-Info Co., Ltd. : Dev Team / Mr. Nattanon Vinyangkoon – Project conception, implementation, and thorough review of all deliverables.

AI Coding Assistant: TRAE SOLO / MICROSOFT 365 COPILOT - Utilized to support code generation and productivity improvements under human oversight.
