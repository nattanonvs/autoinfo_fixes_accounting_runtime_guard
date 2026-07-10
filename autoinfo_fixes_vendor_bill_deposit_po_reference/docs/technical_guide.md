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
