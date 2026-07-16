# คู่มือ Admin/Test สำหรับ Department Task Sequence

## Config ที่ใช้งาน
- ใช้ไฟล์ config: `c:\odoo\odoo-15.0\odoo.conf`
- Database สำหรับ upgrade/test มาตรฐาน: `test_autoinfo_project_department_sequence_setup`
- ให้ตรวจ `addons_path` ในไฟล์ config ว่ามี path ที่จำเป็นสำหรับโมดูลชุดนี้ครบก่อนรันคำสั่ง
- ต้องไม่มี path `c:\odoo\addons_oca\apps-store` ปะปนอยู่ใน `addons_path`

## คำสั่ง Upgrade มาตรฐาน

```powershell
python c:\odoo\odoo-15.0\odoo-bin -c c:\odoo\odoo-15.0\odoo.conf -d test_autoinfo_project_department_sequence_setup -u autoinfo_project,dtr_project --stop-after-init --log-level=info
```

## คำสั่ง Test มาตรฐาน

```powershell
python c:\odoo\odoo-15.0\odoo-bin -c c:\odoo\odoo-15.0\odoo.conf -d test_autoinfo_project_department_sequence_setup -u autoinfo_project,dtr_project --test-enable --test-tags /autoinfo_project --stop-after-init --log-level=test
```

## จุดตรวจสอบเมื่อใช้งานหรือทดสอบ
1. ตรวจว่า user ผู้สร้างรายการมี Employee และ Department ผูกครบ
2. ตรวจว่า Department มีค่า `Task Code Prefix`
3. ตรวจว่า Department มีค่า `Task Sequence`
4. ตรวจว่า `Task Sequence Status` เป็น `Ready`
5. กด `Refresh Task Sequence` แล้วลองสร้างเลขงานใหม่อีกครั้ง
6. หลังรัน test ให้ตรวจ log ว่าจบด้วยสถานะลักษณะ `0 failed, 0 error(s)`

## คำเตือนที่พบได้และไม่บล็อกการทดสอบ
- `selection overrides existing selection`
- `unable to set NOT NULL on project_task.task_category_id/project_site_id`
- warning กลุ่มนี้ให้บันทึกไว้ประกอบผลทดสอบได้ แต่ไม่ถือว่าเป็น blocker หากคำสั่ง upgrade/test จบสมบูรณ์
