# Department Task Sequence UX And Guides Design

## เป้าหมาย

ปรับประสบการณ์ใช้งานของหน้า `Department` สำหรับ `Task Sequence Setup` ให้ชัดเจนขึ้น และเพิ่มเอกสารใช้งานสำหรับทั้งผู้ใช้ทั่วไปและผู้ดูแลระบบ โดยไม่เปลี่ยนหลักการออกเลข task code ที่ทำเสร็จแล้ว

งานนี้มี 2 ส่วน:

- ปรับ UX บนหน้า `Department`
- เพิ่มคู่มือใช้งานและคู่มือทดสอบ

## สิ่งที่มีอยู่แล้ว

ปัจจุบันระบบรองรับแล้ว:

- ตั้ง `Task Code Prefix` บน `Department`
- เลือกหรือสร้าง `Task Sequence` จากหน้า `Department`
- กด `Refresh Task Sequence` เพื่อ normalize ค่า sequence
- ใช้ sequence ของแผนกผู้สร้างตอนออก `project.task.code`
- แสดงชื่อ task เป็น `[CODE/JOB NO] ชื่องาน`
- ป้องกันการกด `Create Task Sequence` ซ้ำด้วย validation ฝั่ง backend

ดังนั้นงานรอบนี้ไม่แตะ logic หลักของการ generate code แต่จะทำให้หน้าใช้งานเข้าใจง่ายขึ้นและมีคู่มือรองรับ

## ปัญหาที่ต้องแก้

แม้ backend จะกันการสร้างซ้ำแล้ว แต่หน้า `Department` ยังมีจุดที่ทำให้ผู้ใช้สับสนได้:

- เมื่อมี sequence แล้ว ปุ่ม `Create Task Sequence` ยังแสดงอยู่
- ผู้ใช้ต้อง “ลองกด” จึงจะรู้ว่าควรใช้ `Refresh` แทน
- ยังไม่มีคู่มือสั้นสำหรับทีมที่ต้องตั้ง BA / TA / IA / FA / DES
- ยังไม่มีชุดคำสั่งมาตรฐานสำหรับ admin/test ที่เอาไปใช้ซ้ำได้ง่าย

## แนวทางที่เลือก

เลือกให้หน้า `Department` ทำตัวตามสถานะจริงของแผนก:

- ถ้ายังไม่มี `Task Sequence` ให้เห็นปุ่ม `Create Task Sequence`
- ถ้ามี `Task Sequence` แล้ว ให้ซ่อนปุ่ม `Create Task Sequence`
- ถ้ามี `Task Sequence` แล้ว ให้เห็นปุ่ม `Refresh Task Sequence`

เหตุผล:

- ลดความสับสน
- ตรงกับ mental model ของผู้ใช้
- สอดคล้องกับ validation ที่มีอยู่แล้วใน backend

## ทางเลือกที่พิจารณา

### ทางเลือก A: ซ่อนปุ่ม Create เมื่อมี sequence แล้ว

ข้อดี:

- หน้าใช้งานชัดที่สุด
- ลดโอกาสกดผิด
- ทำให้ flow เป็นธรรมชาติ: สร้างครั้งแรก -> refresh เมื่อมีของแล้ว

ข้อเสีย:

- ถ้าผู้ใช้ต้องการ “เปลี่ยนไปใช้ sequence เดิมอีกตัว” ต้องทำผ่าน field `Task Sequence` แล้วใช้ `Refresh`

### ทางเลือก B: แสดงปุ่ม Create แต่ disable

ข้อดี:

- ผู้ใช้เห็นทุก action ที่ระบบมี

ข้อเสีย:

- หน้าจอดูรกกว่า
- ผู้ใช้ยังสงสัยว่าทำไมปุ่มนี้อยู่แต่กดไม่ได้

### ทางเลือก C: แสดงปุ่ม Create ตลอด แล้วปล่อยให้ backend กัน

ข้อดี:

- เปลี่ยน UI น้อยที่สุด

ข้อเสีย:

- UX แย่
- ผู้ใช้ต้องเรียนรู้จาก error message

คำแนะนำ: ใช้ทางเลือก A

## การออกแบบ UX บนหน้า Department

ในส่วน `Department Sequence Setup`:

### กรณียังไม่มี Task Sequence

ให้แสดง:

- `Task Code Prefix`
- `Task Sequence`
- `Task Sequence Status`
- `Task Sequence Preview`
- ปุ่ม `Create Task Sequence`

ให้ซ่อน:

- ปุ่ม `Refresh Task Sequence`

### กรณีมี Task Sequence แล้ว

ให้แสดง:

- `Task Code Prefix`
- `Task Sequence`
- `Task Sequence Status`
- `Task Sequence Preview`
- ปุ่ม `Refresh Task Sequence`

ให้ซ่อน:

- ปุ่ม `Create Task Sequence`

## หลักการแสดงผล

- การซ่อน/แสดงปุ่มใช้เงื่อนไขจาก `project_task_sequence_id`
- ฝั่ง backend ยังต้องกัน duplicate creation เหมือนเดิม
- ถ้ามีการเรียก action โดยตรงนอกหน้า UI ระบบยังต้องปลอดภัย

## ขอบเขตของคู่มือผู้ใช้

สร้างคู่มือสำหรับผู้ใช้ธุรกิจที่ต้องตั้งค่าแผนก เช่น BA / TA / IA / FA / DES

หัวข้อที่ต้องมี:

- หน้า Department อยู่ตรงไหน
- ต้องกรอก `Task Code Prefix` อย่างไร
- วิธีสร้าง sequence ครั้งแรก
- วิธี refresh sequence
- ตัวอย่างรหัสที่ระบบจะออก เช่น `BA0126-00001`
- ความหมายของ `Status` และ `Preview`
- กรณีเจอข้อความ error ต้องทำอย่างไร

รูปแบบเอกสาร:

- กระชับ
- เป็นขั้นตอนใช้งานจริง
- ใช้ภาษาไทย

## ขอบเขตของคู่มือ admin/test

สร้างคู่มือสำหรับผู้ดูแลระบบหรือทีม dev/test

หัวข้อที่ต้องมี:

- ไฟล์ config ที่ใช้รันทดสอบ
- คำสั่ง upgrade มาตรฐาน
- คำสั่ง test มาตรฐาน
- ตัวอย่างฐานข้อมูลทดสอบที่ใช้
- จุดที่ต้องเช็กเมื่อ task code ไม่ออก
- warning ที่พบได้และสิ่งที่ถือว่าไม่ใช่ blocker

รูปแบบเอกสาร:

- ใช้คำสั่ง copy/paste ได้
- ระบุ path ชัดเจน
- ใช้ภาษาไทยเป็นหลัก แทรก command ภาษาอังกฤษตามความจำเป็น

## File Strategy

แนะนำให้แยกเป็น 3 ส่วน:

- ปรับ `hr_department_view.xml` เฉพาะเรื่อง visibility ของปุ่ม
- เพิ่ม `README` หรือ `docs/user_guide.md` สำหรับผู้ใช้
- เพิ่ม `docs/admin_test_guide.md` สำหรับทีม admin/test

การแยกแบบนี้ช่วยให้:

- UI logic อยู่ในไฟล์ view ตามหน้าที่
- คู่มือใช้งานไม่ปนกับโค้ด
- เอกสารสำหรับผู้ใช้และ admin ไม่ปนกัน

## Error Handling

กรณีที่ต้องคงไว้:

- ถ้าผู้ใช้เรียก `Create Task Sequence` ทั้งที่มี sequence แล้ว ระบบยังต้อง error และบอกให้ใช้ `Refresh`
- ถ้า setup ผิด ระบบยังต้องชี้กลับมาที่หน้า Department

กรณีที่ UX ต้องช่วยลด:

- ผู้ใช้ไม่ควรเห็น action ที่ไม่ควรใช้ในสถานะปัจจุบัน

## การทดสอบ

ต้องทดสอบเพิ่มอย่างน้อย:

- เมื่อ Department ยังไม่มี `project_task_sequence_id` ปุ่ม `Create` แสดง และ `Refresh` ซ่อน
- เมื่อ Department มี `project_task_sequence_id` ปุ่ม `Refresh` แสดง และ `Create` ซ่อน
- backend ยังคงกัน duplicate creation ได้ แม้ UI จะซ่อนปุ่มแล้ว
- เอกสารใหม่ถูกสร้างใน path ที่กำหนด
- คำสั่งในคู่มือ admin/test ใช้งานได้จริงกับ `odoo.conf` ปัจจุบัน

## ผลลัพธ์ที่ต้องได้

- หน้า Department เข้าใจง่ายขึ้น
- ผู้ใช้ BA / TA / IA / FA / DES ตั้งค่าได้จากหน้าเดียวโดยไม่สับสน
- ทีม admin/test มีคำสั่งรันซ้ำได้จากคู่มือ
- logic หลักของ task code ไม่เปลี่ยนจากที่ผ่าน test แล้ว

## สรุป

งานนี้เป็นการต่อยอดจาก logic ที่พร้อมใช้งานแล้ว โดยโฟกัสที่:

- ทำให้หน้า `Department` แสดง action ตามสถานะจริง
- ลดความสับสนของผู้ใช้
- เพิ่มเอกสารใช้งานและเอกสารทดสอบให้พร้อมส่งต่อทีม
