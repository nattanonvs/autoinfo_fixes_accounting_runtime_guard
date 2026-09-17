# User Guide

## สำหรับใคร

เอกสารนี้สำหรับ

- แอดมินระบบ
- โปรแกรมเมอร์
- ผู้ที่มีสิทธิ์ดูเมนู Technical ใน Odoo

## เมนูที่ใช้

เมนูหลักของโมดูลคือ `Runtime Guard`

เมนูนี้ใช้สำหรับ

- รันชุดตรวจ
- เปิดดูผลตรวจ
- เปิดคำแนะนำแก้ปัญหา
- บันทึกการ review

## วิธีใช้งานแบบสั้น

1. เปิดเมนู `Runtime Guard`
2. กด `Run Checks`
3. อ่านรายการที่ขึ้น `warning`, `error`, หรือ `review`
4. เปิดรายการที่ต้องการ
5. กด `Open Fix Help`
6. คัดลอกคำสั่งไปใช้ใน Linux server
7. กลับมากด `Mark Reviewed`

## วิธีใช้งานทีละขั้น

### 1. รันการตรวจ

เมื่อเข้าเมนู `Runtime Guard` ให้กด `Run Checks`

ระบบจะสร้างรายการตรวจ เช่น

- Runtime Path
- Python Package
- Dependency Chain
- Schema Risk
- Module State
- External DB Warning

### 2. ดูระดับผลตรวจ

ผลตรวจแต่ละรายการจะมีระดับ เช่น

- `ok` : ปกติ
- `warning` : ควรตรวจเพิ่ม
- `error` : มีปัญหาที่ต้องแก้
- `review` : ควรเปิดดูรายละเอียดก่อนตัดสินใจ

### 3. เปิด Fix Help

กด `Open Fix Help` เพื่อดู

- สาเหตุของปัญหา
- คำสั่งเช็ก
- คำสั่งแก้
- คำสั่งตรวจซ้ำ
- หมายเหตุความเสี่ยง

## ตัวอย่างการใช้งานจริง

### กรณี package หาย

1. รัน `Run Checks`
2. พบรายการ `Python Package`
3. กด `Open Fix Help`
4. คัดลอกคำสั่ง `pip install`
5. ไปติดตั้งบน server
6. กลับมากด `Mark Reviewed`

### กรณี dependency chain มีปัญหา

1. รัน `Run Checks`
2. พบรายการ `Dependency Chain`
3. เปิดดูว่าปัญหาผูกกับโมดูลไหน
4. ใช้คำสั่ง `grep`, `sed`, หรือ Python script ตามที่ระบบแนะนำ
5. อัปเดตโมดูลที่เกี่ยวข้อง
6. กลับมากด `Mark Reviewed`

### กรณีหน้าเว็บยัง error หลัง update

1. รัน `Run Checks`
2. เปิดรายการที่เกี่ยวกับ schema หรือ runtime
3. ถ้า shell เห็น field แล้ว แต่หน้าเว็บยัง error ให้ restart service
4. กลับมาตรวจซ้ำ

## หมายเหตุสำคัญ

- โมดูลนี้ช่วยตรวจและสรุปปัญหา
- โมดูลนี้ไม่แก้ environment ภายนอกให้อัตโนมัติ
- ถ้าปัญหาเกิดจาก source module ต้นทาง ต้องแก้ที่โมดูลต้นทางจริง
- หลัง update โมดูลที่แตะ model หรือ view สำคัญ ควร restart Odoo service
