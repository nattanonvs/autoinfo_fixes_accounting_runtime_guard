# คู่มือผู้ใช้งาน Task Sequence ตามแผนก

## 1. คู่มือนี้ใช้เมื่อไร

คู่มือนี้ใช้สำหรับตั้งค่าเลขรัน `Task Code` ตามแผนกในโมดูล `autoinfo_project` เช่น `BA`, `TA`, `IA`, `FA`, `DES` เพื่อให้เวลา user สร้างงาน ระบบออกรหัสงานอัตโนมัติตามแผนกของผู้สร้าง

ตัวอย่างรูปแบบชื่อที่ระบบแสดง:

- `[BA0126-00001/JOB-BA-0001] วิเคราะห์ Requirement`

ตัวอย่างรูปแบบรหัส:

- `BA0126-00001`

ความหมายของรหัส:

- `BA` = รหัสย่อแผนก
- `0126` = เดือนและปีแบบ `MMyy`
- `00001` = running number 5 หลัก
- running number จะเริ่มนับใหม่เมื่อเปลี่ยนเดือน

## 2. ก่อนเริ่มใช้งาน

ควรตรวจสอบให้ครบก่อน:

1. มีการติดตั้งโมดูล `autoinfo_project` แล้ว
2. ผู้ใช้งานมีข้อมูล `Employee` ผูกกับ user
3. `Employee` ของผู้ใช้งานอยู่ในแผนกที่ถูกต้อง
4. แผนกที่จะใช้งานมีสิทธิ์ให้แก้ไขหน้า `Department`

หมายเหตุ:

- ระบบออกรหัสจากแผนกของผู้สร้างงาน
- ถ้าผู้สร้างไม่มีแผนก หรือแผนกยังไม่ตั้งค่า `Task Sequence` งานจะสร้างไม่ผ่าน

## 3. หน้าใช้งานอยู่ตรงไหน

ให้ไปที่เมนู `Employees > Configuration > Departments` แล้วเปิดแผนกที่ต้องการตั้งค่า

ในหน้า `Department` จะมีส่วน `Department Sequence Setup` สำหรับตั้งค่าเลขงาน

## 4. ฟิลด์ที่ต้องรู้จัก

- `Task Code Prefix` คือรหัสย่อแผนก เช่น `BA`, `TA`, `IA`, `FA`, `DES`
- `Task Sequence` คือ sequence ที่ระบบใช้รันเลขงานของแผนกนั้น
- `Task Sequence Status` คือสถานะความพร้อมของการตั้งค่า
- `Task Sequence Preview` คือตัวอย่างเลขงานถัดไปที่ระบบจะสร้าง

ความหมายของสถานะ:

- `Not Configured` = ยังตั้งค่าไม่ครบ
- `Invalid Setup` = มี sequence แล้ว แต่ค่าภายในไม่ตรงรูปแบบที่ระบบต้องการ
- `Ready` = พร้อมใช้งาน สามารถสร้าง task และออกรหัสได้

## 5. Workflow ตั้งค่าครั้งแรก

ใช้ขั้นตอนนี้เมื่อแผนกยังไม่เคยตั้ง `Task Sequence`

1. ไปที่ `Employees > Configuration > Departments`
2. เปิดแผนกที่ต้องการ เช่น `Business Analyst`
3. ใส่ค่าใน `Task Code Prefix` เช่น `BA`
4. ตรวจว่าฟิลด์ `Task Sequence` ยังว่างอยู่
5. กดปุ่ม `Create Task Sequence`
6. บันทึกหรือรอให้หน้าจอรีเฟรชค่าปัจจุบัน
7. ตรวจ `Task Sequence Status` ต้องเป็น `Ready`
8. ตรวจ `Task Sequence Preview` เช่น `BA0126-00001`

สิ่งที่ควรเห็นหลังตั้งค่าสำเร็จ:

- ระบบสร้าง `Task Sequence` ให้แผนกอัตโนมัติ
- ปุ่ม `Create Task Sequence` จะไม่ใช่ action หลักอีกแล้ว
- ปุ่ม `Refresh Task Sequence` จะใช้สำหรับปรับค่าระบบให้กลับมาตามมาตรฐาน

## 6. Workflow สำหรับ BA, TA, IA, FA, DES

ใช้แนวทางเดียวกันทุกแผนก โดยเปลี่ยนเฉพาะ `Task Code Prefix`

ตัวอย่างที่แนะนำ:

1. แผนก `Business Analyst` ใช้ `BA`
2. แผนก `Technical Analyst` ใช้ `TA`
3. แผนก `Implementation` ใช้ `IA`
4. แผนก `Functional Analyst` ใช้ `FA`
5. แผนก `Design` ใช้ `DES`

ตัวอย่างเลข preview ที่ควรได้:

- `BA0126-00001`
- `TA0126-00001`
- `IA0126-00001`
- `FA0126-00001`
- `DES0126-00001`

คำแนะนำ:

- ใช้ prefix ให้สั้นและสื่อความหมายชัดเจน
- ควรใช้รูปแบบเดียวกันทั้งองค์กร
- ระบบจะ normalize เป็นตัวพิมพ์ใหญ่ในการตั้งค่า

## 7. Workflow เมื่อต้องแก้ไขหรือซ่อมการตั้งค่า

ใช้ขั้นตอนนี้เมื่อ:

- เปลี่ยน `Task Code Prefix`
- เลือก `Task Sequence` เดิมกลับมาใช้
- ต้องการปรับ sequence ให้กลับมาตามมาตรฐาน
- สถานะขึ้น `Invalid Setup`

ขั้นตอน:

1. เปิดหน้า `Department` ของแผนกเดิม
2. ตรวจค่า `Task Code Prefix`
3. ตรวจฟิลด์ `Task Sequence` ว่ายังชี้ sequence ที่ถูกต้อง
4. กดปุ่ม `Refresh Task Sequence`
5. ตรวจว่า `Task Sequence Status` กลับมาเป็น `Ready`
6. ตรวจ `Task Sequence Preview` ว่าขึ้นตัวอย่างรหัสตาม prefix ที่ต้องการ

ตัวอย่าง:

- ถ้าแผนก BA เปลี่ยน prefix จาก `ba` หรือ `B A` ให้แก้เป็น `BA`
- ถ้า sequence ถูกแก้ไขผิดรูปแบบ ให้กด `Refresh Task Sequence`

## 8. ตัวอย่างการใช้งานจริงหลังตั้งค่าเสร็จ

หลังจากแผนกตั้งค่า `Ready` แล้ว เมื่อ user ในแผนกนั้นสร้าง task ใหม่ ระบบจะออกรหัสให้อัตโนมัติ

ตัวอย่าง flow:

1. user `BA User` มี `Employee` อยู่ในแผนก `Business Analyst`
2. แผนก `Business Analyst` ตั้งค่า prefix เป็น `BA` และสถานะเป็น `Ready`
3. user สร้าง task ใหม่ใน project ที่ต้องการ
4. ระบบสร้าง `Task Code` เช่น `BA0126-00001`
5. ระบบแสดงชื่อ task เป็นรูปแบบ `[CODE/JOB NO] ชื่องาน`

ตัวอย่างชื่อ task:

- `[BA0126-00001/JOB-BA-0001] Create BA task`

## 9. ความหมายของ Preview และเลขรัน

`Task Sequence Preview` ใช้สำหรับช่วยตรวจว่าระบบพร้อมออกเลขตามรูปแบบที่ถูกต้องหรือไม่ โดยยังไม่จำเป็นต้องสร้าง task จริงก่อน

สิ่งที่ควรสังเกต:

- prefix ต้องตรงกับแผนก เช่น `BA`
- ส่วนกลางต้องเป็นเดือนและปีแบบ `MMyy` เช่น `0126`
- เลขท้ายต้องเป็น 5 หลัก เช่น `00001`

หมายเหตุ:

- running number จะเดินตาม sequence ของแผนกนั้นและรีเซ็ตใหม่ในแต่ละเดือน
- รูปแบบนี้ออกแบบให้แยกแต่ละแผนกได้ชัดเจน

## 10. ปัญหาที่พบบ่อยและวิธีแก้

### กรณีขึ้น `Please complete Department Sequence Setup first.`

สาเหตุที่พบบ่อย:

- ยังไม่ได้ใส่ `Task Code Prefix`
- ยังไม่ได้สร้าง `Task Sequence`
- user ผู้สร้างงานไม่มีแผนกที่พร้อมใช้งาน

วิธีแก้:

1. ไปที่หน้า `Department`
2. ใส่ `Task Code Prefix`
3. กด `Create Task Sequence`
4. ตรวจให้ `Task Sequence Status` เป็น `Ready`
5. ให้แน่ใจว่า user ผู้สร้างมี `Employee` และอยู่ในแผนกนั้น

### กรณีขึ้น `Department Sequence Setup is invalid.`

สาเหตุที่พบบ่อย:

- มีคนแก้ค่า sequence จนไม่ตรงมาตรฐาน
- prefix ของ sequence ไม่ตรงกับ `Task Code Prefix`
- sequence ไม่อยู่ในรูปแบบที่ระบบต้องการ

วิธีแก้:

1. เปิดหน้า `Department`
2. ตรวจ `Task Code Prefix`
3. กด `Refresh Task Sequence`
4. ตรวจสถานะให้กลับมาเป็น `Ready`

### กรณีกด `Create Task Sequence` แล้วระบบแจ้งให้ใช้ Refresh

สาเหตุ:

- แผนกนี้มี `Task Sequence` อยู่แล้ว

วิธีแก้:

1. ไม่ต้องสร้างซ้ำ
2. ใช้ปุ่ม `Refresh Task Sequence` แทน

### กรณี `Task Sequence Preview` ไม่ขึ้น

สาเหตุที่พบบ่อย:

- ยังไม่ได้กรอก prefix
- ยังไม่ได้เลือกหรือสร้าง sequence
- สถานะยังไม่เป็น `Ready`

วิธีแก้:

1. ตรวจว่า `Task Code Prefix` ไม่ว่าง
2. ตรวจว่า `Task Sequence` ถูกเลือกแล้ว
3. ถ้าสถานะเป็น `Invalid Setup` ให้กด `Refresh Task Sequence`

## 11. Checklist สั้นก่อนเริ่มใช้งานจริง

ก่อนให้ทีม BA, TA, IA, FA, DES ใช้งานจริง ควรตรวจดังนี้:

1. ทุกแผนกมี `Task Code Prefix`
2. ทุกแผนกมี `Task Sequence`
3. ทุกแผนกมีสถานะ `Ready`
4. ทุกแผนกมี `Task Sequence Preview`
5. user ที่จะสร้างงานมี `Employee` และผูกแผนกถูกต้อง

## 12. สรุปสั้น

- ตั้งค่าทั้งหมดที่หน้า `Department`
- ถ้ายังไม่เคยมี sequence ให้กด `Create Task Sequence`
- ถ้ามี sequence แล้วหรือค่าผิด ให้กด `Refresh Task Sequence`
- ตรวจ `Task Sequence Status` ให้เป็น `Ready` ก่อนใช้งาน
- เมื่อ user สร้าง task ระบบจะออกรหัสตามแผนก เช่น `BA0126-00001`
