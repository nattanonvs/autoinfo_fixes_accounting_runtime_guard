# คู่มือเทคนิค

## โครงสร้าง
- โมดูลนี้เป็น overlay addon
- inherit `account.move`
- เพิ่มฟิลด์ `deposit_po_ref`
- inherit view จาก `autoinfo_accounting_form`

## จุดสำคัญ
- ไม่แก้ logic ใน `dtr_deposit_payment`
- ไม่แก้รายงานที่ใช้ `deposit_so_ref`
- ใช้การแยก field ตาม `move_type`
- ใช้ domain ใน view เพื่อกรอง dropdown ตามคู่ค้า และสถานะยืนยันแล้ว

## การกรอง dropdown
- `PO Reference` (deposit_po_ref): `partner_id` ต้องตรงกับเอกสาร และ `state` เป็น `purchase` หรือ `done`
- `SO Reference` (deposit_so_ref): `partner_id` ต้องตรงกับเอกสาร และ `state` เป็น `sale` หรือ `done`
