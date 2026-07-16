# Knowledge Platform Release Prep Design

## Goal

เตรียมโมดูล `autoinfo_company_knowledge_platform` ให้พร้อมสำหรับการปล่อยใช้งานและอัปโหลดขึ้น GitHub repository ที่กำหนด โดยใช้โค้ดและเอกสารที่มีอยู่เป็นฐาน และแก้เฉพาะสิ่งที่จำเป็นจริง

เป้าหมายรอบนี้มี 6 ส่วน:

1. ยืนยันและคงโลโก้โมดูลที่เหมาะสม
2. รีวิวโค้ดอีกรอบแบบ pre-release
3. เก็บเอกสารให้ครบทุกชุดและตรงกับพฤติกรรมจริงของระบบ
4. เพิ่มคำเตือนสำคัญมากในต้นคู่มือติดตั้ง
5. zip โมดูลให้พร้อมแจกจ่าย
6. เตรียม Git repository และ push ขึ้น `https://github.com/nattanonvs/autoinfo_company_knowledge_platform.git`

## Scope

งานนี้ครอบคลุมเฉพาะโมดูล:

- `autoinfo_company_knowledge_platform`

จะไม่แตะ Odoo core และจะไม่แก้โมดูลอื่นใน repo เดียวกัน

## Current Context

สถานะปัจจุบันของโมดูล:

- โค้ดหลักและ test suite มีอยู่แล้ว
- เอกสารหลักมีอยู่แล้วหลายไฟล์
- โลโก้มีอยู่แล้ว 2 เวอร์ชัน โดยผู้ใช้เลือกเวอร์ชันเข้มให้เป็นตัวหลัก
- มี commit ของโมดูลอยู่แล้วหลายชุด
- ผู้ใช้ต้องการ push ไป GitHub repo ใหม่ชื่อเดียวกับโมดูล

## Approaches Considered

### Approach A: ใช้โมดูลเดิมเป็นฐานและเก็บงานแบบ minimal-safe

แนวทางนี้จะ:

- ใช้โค้ดเดิมทั้งหมดเป็นฐาน
- รีวิวและแก้เฉพาะ defect จริง
- ปรับเอกสารให้ตรงกับ final module state
- zip และ push โดยไม่รื้อโครงสร้างใหญ่

ข้อดี:

- เสี่ยงต่ำสุด
- ตรงกับความต้องการ “ไม่ rebuild”
- ไม่ทำลาย history หรือ behavior ที่ใช้งานได้แล้ว

ข้อเสีย:

- โครงสร้างบางจุดอาจไม่ “รีเซ็ตใหม่หมด” แบบงาน greenfield

### Approach B: จัดโครงสร้างใหม่บางส่วนก่อนปล่อย

แนวทางนี้จะ:

- คง logic หลักไว้
- ย้าย/จัดไฟล์ให้เนี้ยบขึ้นก่อน release

ข้อดี:

- repo ดูเรียบร้อยขึ้น

ข้อเสีย:

- เพิ่มความเสี่ยงจากการย้าย path
- ไม่จำเป็นหากโค้ดปัจจุบัน stable อยู่แล้ว

### Recommendation

เลือก **Approach A**

เพราะตรงกับข้อกำหนดเรื่อง minimal change, production safety, และการใช้โมดูลเดิมเป็นฐานมากที่สุด

## Implementation Design

### 1. Logo

- ใช้ `static/description/icon.png` เป็นโลโก้หลัก
- เก็บ `static/description/icon_alt.png` เป็นไฟล์สำรอง
- ไม่เปลี่ยนชื่อไฟล์หลักอื่นเพิ่ม

### 2. Code Review

จะรีวิวในมุม:

- manifest/dependencies
- access/security/rules
- views/actions/menus
- uninstall safety
- จุดเสี่ยง runtime ที่อาจทำให้เซิร์ฟเวอร์ล้ม

ถ้าเจอ defect จริง:

- แก้แบบ minimal-safe
- retest เฉพาะ flow ที่กระทบ
- จำกัดรอบแก้ไม่เกิน 3 รอบ

### 3. Documentation

เอกสารเป้าหมาย:

- `README.md`
- `docs/installation_guide.md`
- `docs/uninstallation_guide.md`
- `docs/user_guide.md`
- `docs/technical_guide.md`
- `docs/troubleshooting.md`
- `docs/timeline_and_changelog.md`

หลักการเขียน:

- ภาษาไทย
- อิงจาก final code เท่านั้น
- ไม่อ้างฟีเจอร์ที่ไม่มีจริง
- แยกชัดว่าอะไรมี UI entry point และอะไรเป็น backend capability

### 4. Critical Warning In Install Guide

ในต้น `installation_guide.md` จะเพิ่มส่วนเตือนพิเศษที่เด่นชัดมากเกี่ยวกับเรื่องที่อาจทำให้ระบบล้ม เช่น:

- อัปเกรดโมดูลก่อนใช้งานทุกครั้งเมื่อ schema เปลี่ยน
- หากไม่ upgrade อาจเกิด `UndefinedColumn`
- ต้อง backup ก่อนติดตั้ง/อัปเกรดบน production
- ต้อง restart Odoo หลังเปลี่ยน `addons_path` หรือ deploy โค้ดใหม่

รูปแบบการเน้น:

- เป็นส่วนต้นเอกสาร
- ใช้ข้อความเตือนชัดเจน
- ถ้าระบบ markdown/renderer รองรับ จะจัดเป็นบล็อกเตือนเด่น

### 5. Packaging

- zip โมดูลจากโฟลเดอร์จริง
- ปลายทาง:
  - `C:\odoo\APPreadytouse\backup`
- ชื่อไฟล์ zip จะอิงชื่อโมดูลและวันที่

### 6. Git Preparation And Push

เป้าหมาย Git:

- repository เป้าหมาย:
  - `https://github.com/nattanonvs/autoinfo_company_knowledge_platform.git`

การทำงาน:

1. ตรวจสถานะ repo ปัจจุบัน
2. หลีกเลี่ยงการปนกับไฟล์อื่นใน monorepo เดิม
3. หากจำเป็น จะ clone/init repo เป้าหมายแยกสำหรับโมดูลนี้
4. ใส่ description ที่เหมาะสมใน `README.md` และ metadata ที่เกี่ยวข้อง
5. commit เฉพาะงานที่เกี่ยวกับ release prep รอบนี้
6. push ขึ้น GitHub repo เป้าหมาย ถ้า auth พร้อม

## Testing Plan

ลำดับ validation:

1. อ่านโค้ดและสรุป defect ที่แท้จริง
2. ถ้ามีการแก้โค้ด:
   - run targeted test ที่เกี่ยวข้อง
3. run smoke checks ที่จำเป็น:
   - install/upgrade
   - main menu/view/action
   - uninstall หากมีการแตะส่วนที่เสี่ยง
4. ตรวจเอกสารให้ตรงกับ final state
5. ตรวจว่า zip เปิดใช้ได้

## Risks

### Risk 1: Production schema mismatch

ถ้า deploy โค้ดใหม่แต่ไม่ `-u autoinfo_company_knowledge_platform` อาจเกิด error แบบ:

- `psycopg2.errors.UndefinedColumn`

### Risk 2: Push ปนกับ monorepo เดิม

ถ้าทำ Git จาก repo ปัจจุบันตรง ๆ อาจเผลอรวมโมดูลอื่นที่ไม่เกี่ยว

### Risk 3: เอกสารพูดเกินของจริง

หากไม่ตรวจเทียบกับ code อีกครั้ง อาจมีคู่มือที่พา user ไปหาเมนูที่ยังไม่มีจริง

## Acceptance Criteria

งานนี้ถือว่าเสร็จเมื่อ:

- โลโก้หลักถูกเลือกและอยู่ในตำแหน่งมาตรฐาน
- โค้ดได้รับการ review รอบ release
- เอกสารครบและตรงกับระบบจริง
- คู่มือติดตั้งมีคำเตือนสำคัญตั้งแต่ต้น
- zip ถูกสร้างสำเร็จ
- repository เป้าหมายพร้อมและ push สำเร็จ หรือถ้าติดข้อจำกัดจริงจะถูกรายงานอย่างชัดเจน
