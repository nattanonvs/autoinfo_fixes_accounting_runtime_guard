# การแก้ปัญหาเบื้องต้น

## ไม่เห็นช่อง `PO Reference`
- ตรวจสอบว่าเอกสารเป็น `Vendor Bill`
- ตรวจสอบว่าเลือก `Type = Deposit Payment`
- อัปเกรดโมดูล `autoinfo_fixes_vendor_bill_deposit_po_reference`

## ใน dropdown ไม่มีรายการให้เลือก
- ตรวจสอบว่าเลือกคู่ค้าแล้ว
- ตรวจสอบว่า `PO` หรือ `SO` อยู่สถานะยืนยันแล้ว
- ถ้าเอกสารยังไม่ยืนยัน ระบบจะไม่แสดงใน dropdown

## ยังเห็น `SO Reference` ในฝั่งขาย
- เป็นพฤติกรรมปกติสำหรับ `Customer Invoice`
- โมดูลนี้ไม่ได้เปลี่ยน flow ฝั่งขาย
