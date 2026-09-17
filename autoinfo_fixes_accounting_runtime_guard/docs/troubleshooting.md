# Troubleshooting

## อาการ: เจอ `PyPDF2` หรือ `passlib` หาย

สาเหตุ:
- package อยู่คนละ interpreter
- package ยังไม่ได้ติดตั้งใน Python ที่ Odoo ใช้จริง

วิธีเช็ก:
1. รัน `python3 -c "import sys; print(sys.executable)"`
2. รัน `python3 -c "import PyPDF2"` หรือ package ที่สงสัย

## อาการ: เจอ `actual_due_date` ไม่มี

สาเหตุ:
- dependency chain ไม่ครบ
- โมดูลเจ้าของ field ยังไม่ถูก upgrade

วิธีเช็ก:
1. เปิด Runtime Guard
2. ดู check หมวด `Dependency Chain` และ `Schema Risk`
3. ใช้คำสั่ง `grep` หรือ `sed` ที่ wizard แนะนำ

## อาการ: มีโมดูลค้าง `to upgrade`

วิธีเช็ก:
1. เปิด Runtime Guard
2. ดู check หมวด `Module State`
3. รัน SQL ที่ระบบแนะนำเพื่อตรวจรายการทั้งหมด
