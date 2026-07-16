# Department Task Sequence Setup Design

## เป้าหมาย

ทำให้การตั้งค่าเลข `Task Code` อยู่ที่หน้า `Department` เพียงจุดเดียว โดยผู้ใช้ไม่ต้องเข้าเมนู `Technical > Sequences` แต่ระบบยังใช้ `ir.sequence` ของ Odoo เป็นกลไกเบื้องหลังเหมือนเดิม

รูปแบบเลขที่ต้องรองรับคือ:

- `BA0126-00001`
- `TA0126-00001`
- `IA0126-00001`
- `FA0126-00001`
- `DES0126-00001`

กติกา:

- `BA`, `TA`, `IA`, `FA`, `DES` มาจากตัวย่อแผนก
- `01` คือเดือนแบบ 2 หลัก
- `26` คือปีแบบ 2 หลัก
- `00001` คือ running 5 หลัก
- running reset ใหม่ทุกเดือน
- ตอนสร้าง task ให้ใช้ sequence ของแผนกของผู้สร้าง task

## ขอบเขต

งานนี้ครอบคลุมเฉพาะ:

- การตั้งค่า sequence ที่หน้า `hr.department`
- การสร้างหรือเลือก sequence จากหน้า `Department`
- การใช้ sequence ของแผนกผู้สร้างตอน generate `project.task.code`
- การแสดงชื่อ task เป็น `[CODE/JOB NO] ชื่องาน`

งานนี้ไม่ครอบคลุม:

- การย้ายข้อมูลย้อนหลังของ task เก่า
- การ merge running number ข้ามแผนก
- การให้ project เป็นตัวกำหนด code หลักแทนแผนกของผู้สร้าง

## สิ่งที่มีอยู่แล้ว

ปัจจุบันระบบมีแล้ว:

- `hr.department.project_task_sequence_id` สำหรับผูก sequence ให้แผนก
- `hr.department.task_code_prefix` สำหรับเก็บตัวย่อแผนก
- logic การ generate `project.task.code` จากแผนกของผู้สร้าง
- logic การตั้ง prefix แบบ `%(range_month)s%(range_y)s`
- ชื่อ task แสดงเป็น `[CODE/JOB NO] ชื่องาน`

จุดที่ยังไม่ลงตัวคือ:

- ผู้ใช้ยังอาจต้องเตรียม `ir.sequence` เองจากเมนู Technical
- หน้า Department ยังเป็นเพียงหน้าผูกค่า ไม่ใช่หน้าจัดการ sequence แบบครบวงจร

## แนวทางที่เลือก

เลือกแนวทาง `C`

- หน้า `Department` เป็นหน้าตั้งค่า sequence สำหรับ task
- ผู้ใช้สามารถ “เลือก sequence ที่ใช้” ได้จากหน้า Department
- ผู้ใช้สามารถ “สร้าง sequence ใหม่” ได้จากหน้า Department เช่นกัน
- ไม่ต้องเข้าเมนู `Technical > Sequences`

ดังนั้นหน้า Department จะเป็นจุดใช้งานจริงเพียงหน้าเดียว แม้เบื้องหลังยังเก็บข้อมูลอยู่ใน `ir.sequence`

## ทางเลือกที่พิจารณา

### ทางเลือก A: สร้างอัตโนมัติทั้งหมด

ผู้ใช้กรอกแค่ prefix แล้วระบบสร้าง sequence ให้เองเสมอ

ข้อดี:

- ใช้ง่ายที่สุด
- ลดโอกาสเลือก sequence ผิด

ข้อเสีย:

- ยืดหยุ่นน้อย
- ถ้าต้องใช้ sequence เดิมหรือแก้เชิง admin จะควบคุมยาก

### ทางเลือก B: เลือกหรือสร้างได้จาก Department

ผู้ใช้เลือก sequence เดิมได้ หรือกดสร้างใหม่จากหน้า Department

ข้อดี:

- ยืดหยุ่น
- ไม่ต้องเข้า Technical

ข้อเสีย:

- UI ต้องชัดเจนเพื่อกันความสับสน

### ทางเลือก C: Department เป็นหน้า setup หลัก และมีทั้งเลือกกับสร้าง

แนวทางนี้เหมือน B ในเชิงพฤติกรรม แต่ย้ำชัดว่า Department คือศูนย์กลางของการตั้งค่า

ข้อดี:

- ตรงกับ flow ธุรกิจที่สุด
- คนใช้งานจำได้ง่ายว่า “ถ้าจะตั้ง BA/TA/IA/FA/DES ให้ไปที่ Department”
- ยังรองรับ sequence เดิมได้ ถ้ามีกรณีพิเศษ

ข้อเสีย:

- ต้องออกแบบ validation และปุ่มให้ชัดเพื่อกันเลือก sequence ผิด

คำแนะนำ: ใช้ทางเลือก C

## การออกแบบหน้าจอ Department

เพิ่มส่วน `Department Sequence Setup` ในหน้า `hr.department`

ฟิลด์หลัก:

- `Task Code Prefix`
  - ตัวอย่าง: `BA`, `TA`, `IA`, `FA`, `DES`
  - บังคับเป็นตัวพิมพ์ใหญ่
  - ไม่ควรมีช่องว่าง
- `Task Sequence`
  - ผูกกับ `ir.sequence`
  - จำกัดรายการให้เห็นเฉพาะ sequence ที่ใช้กับ task
- `Task Sequence Preview`
  - แสดงตัวอย่างเลข เช่น `BA0726-00001`
  - ใช้ช่วยให้ผู้ใช้เห็นผลก่อนใช้งานจริง
- `Task Sequence Status`
  - เช่น `Not Configured`, `Ready`, `Invalid Setup`

ปุ่มหลัก:

- `Create Task Sequence`
  - สร้าง sequence ใหม่ให้แผนกนี้จากค่าที่กรอกบนหน้า Department
- `Refresh Task Sequence`
  - อัปเดต sequence ที่ผูกอยู่ให้กลับสู่รูปแบบมาตรฐาน

## กติกาการสร้าง Sequence จากหน้า Department

เมื่อกด `Create Task Sequence`:

- ระบบตรวจว่า `Task Code Prefix` ถูกกรอกแล้ว
- ระบบสร้าง `ir.sequence` ใหม่ 1 รายการ
- ตั้งค่ามาตรฐานดังนี้:
  - `name` = ชื่อที่สื่อว่าเป็น Task Sequence ของแผนกนั้น
  - `code` = ค่าเฉพาะสำหรับ sequence task ของแผนกนั้น
  - `prefix` = `<PREFIX>%(range_month)s%(range_y)s-`
  - `padding` = `5`
  - `number_increment` = `1`
  - `use_date_range` = `True`
  - `implementation` = ใช้มาตรฐานเดียวกับระบบปัจจุบัน
- ระบบนำ sequence ที่สร้างใหม่ไปผูกกับ `project_task_sequence_id` ของ Department ทันที

ตัวอย่าง:

- BA -> `BA%(range_month)s%(range_y)s-`
- DES -> `DES%(range_month)s%(range_y)s-`

## กติกาการเลือก Sequence จากหน้า Department

ถ้าผู้ใช้ต้องการใช้ sequence เดิม:

- เลือกได้จากฟิลด์ `Task Sequence`
- ระบบต้อง validate ว่า sequence ที่เลือก “เหมาะกับ task”

validation ขั้นต่ำ:

- ต้องเป็น sequence ที่ active
- ต้องมี `padding = 5`
- ต้องเปิด `use_date_range = True`
- ควรมี prefix ที่สอดคล้องกับ `Task Code Prefix`

ถ้าไม่ตรงมาตรฐาน:

- ปุ่ม `Refresh Task Sequence` จะช่วยอัปเดตให้ตรงมาตรฐาน
- หรือระบบแจ้งสถานะ `Invalid Setup`

## กติกาการออกเลขตอนสร้าง Task

ตอนสร้าง `project.task`:

- หา Department ของผู้สร้าง task จาก employee ของ user
- อ่าน `project_task_sequence_id` ของ Department นั้น
- ถ้าไม่พบ sequence ให้ error พร้อมบอกให้ไปตั้งค่าที่หน้า Department
- ถ้าพบ sequence ให้ใช้ sequence นั้น generate `code`
- ถ้ายังไม่มี date range ของเดือนปัจจุบัน ให้ระบบสร้างรายเดือนอัตโนมัติ
- ถ้า running เกิน `99999` ในเดือนนั้น ให้ error

ผลลัพธ์สุดท้าย:

- `code` = `BA0726-00001` เป็นต้น

## Data Flow

### Flow การตั้งค่า

1. ผู้ใช้เปิดหน้า Department
2. กรอก `Task Code Prefix`
3. เลือก sequence เดิม หรือกด `Create Task Sequence`
4. ระบบ validate setup
5. หน้า Department แสดงสถานะและ preview

### Flow การสร้าง Task

1. ผู้ใช้สร้าง task
2. ระบบหา department ของผู้สร้าง
3. ระบบอ่าน sequence ของ department
4. ระบบสร้างหรือใช้ monthly date range
5. ระบบ generate `code`
6. ระบบแสดงชื่อ task เป็น `[CODE/JOB NO] ชื่องาน`

## Error Handling

กรณีที่ต้องแจ้ง error ชัดเจน:

- ผู้สร้าง task ไม่มี employee
- employee ไม่มี department
- department ไม่มี `Task Code Prefix`
- department ไม่มี `Task Sequence`
- sequence ถูกตั้งค่าผิดรูปแบบ
- monthly date range ชนกันหรือไม่เป็นรายเดือน
- running number เกิน `99999`

ข้อความควรบอกผู้ใช้ให้กลับไปแก้ที่หน้า `Department` ไม่ใช่ชี้ไปที่เมนู Technical

## ผลกระทบต่อข้อมูลเดิม

- task ใหม่จะใช้กติกาใหม่
- task เดิมไม่ต้องเปลี่ยน `code` ย้อนหลัง
- department ที่มี `project_task_sequence_id` อยู่แล้ว ยังใช้งานต่อได้
- ถ้า sequence เดิมตั้งค่าไม่ตรงมาตรฐาน สามารถใช้ `Refresh Task Sequence` ปรับให้ถูกต้อง

## ข้อกำหนดด้าน UI/UX

- หน้า Department ต้องสื่อชัดว่าเป็นจุดตั้งค่า task code ของแผนก
- ผู้ใช้ควรเห็นตัวอย่างเลขก่อนใช้งานจริง
- ถ้าตั้งค่าไม่ครบ ต้องเห็นสถานะผิดพลาดชัดเจน
- ถ้าพร้อมใช้งาน ต้องเห็นสถานะ `Ready`

## การทดสอบ

ต้องทดสอบอย่างน้อย:

- สร้าง sequence ใหม่จาก Department ของ BA
- เลือก sequence เดิมจาก Department ของ TA
- สร้าง task โดย user แผนก BA ได้ `BAMMYY-00001`
- สร้าง task ถัดไปในเดือนเดียวกัน ได้ `...-00002`
- เปลี่ยนเดือนแล้วเลข reset เป็น `...-00001`
- user ที่ไม่มี department สร้าง task แล้ว error ถูกต้อง
- department ที่ไม่มี sequence สร้าง task แล้ว error ถูกต้อง
- ชื่อ task แสดงเป็น `[CODE/JOB NO] ชื่องาน`

## แผนการลงมือทำ

1. ปรับโมเดล `hr.department` ให้รองรับสถานะ/preview/action ที่ต้องใช้บนหน้า Department
2. ปรับ view ของ Department ให้มีส่วน `Department Sequence Setup`
3. เพิ่มปุ่ม `Create Task Sequence` และ `Refresh Task Sequence`
4. จำกัด domain และ validation ของ `Task Sequence`
5. ปรับ `project.task` ให้ error message ชี้กลับมาที่ Department setup
6. ทดสอบ flow หลักของ BA/TA/IA/FA/DES

## สรุป

แนวทางนี้ทำให้:

- ผู้ใช้ตั้งค่า task sequence ได้จากหน้า Department เพียงจุดเดียว
- ไม่ต้องเข้าเมนู Technical
- ยังใช้ `ir.sequence` มาตรฐานของ Odoo
- รองรับทั้งการเลือก sequence เดิมและการสร้าง sequence ใหม่
- คงรูปแบบ `CODE` เป็น `<PREFIX><MM><YY>-<00001>`
- คงรูปแบบชื่อ task เป็น `[CODE/JOB NO] ชื่องาน`
