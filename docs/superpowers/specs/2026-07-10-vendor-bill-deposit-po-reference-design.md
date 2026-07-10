# Design: Vendor Bill Deposit PO Reference

## ข้อมูลสรุป
- วันที่: 2026-07-10
- แนวทางล่าสุด: ทำเป็น `โมดูลเสริม`
- โมดูลเดิมที่เกี่ยวข้อง: `autoinfo_accounting_form`, `dtr_deposit_payment`
- เป้าหมาย: เมื่อ `Vendor Bill` เลือก `Type = Deposit Payment` ให้แสดง `PO Reference`
- ขอบเขต: แก้เฉพาะหน้าจอ `Vendor Bill` ไม่แตะรายงาน และไม่เปลี่ยน logic deposit เดิม

## ปัญหาปัจจุบัน
- ฟิลด์อ้างอิงที่ใช้ตอน `Type = Deposit Payment` คือ `deposit_so_ref`
- ฟิลด์นี้เป็น `sale.order` และใช้ชื่อแสดงผลเป็น `SO Reference`
- สำหรับ `Vendor Bill` ความหมายที่ต้องการคืออ้างอิง `Purchase Order` ไม่ใช่ `Sale Order`

## เป้าหมายงาน
- เพิ่มฟิลด์อ้างอิงสำหรับ `Purchase Order` บน `account.move`
- แสดง `PO Reference` เฉพาะกรณี `move_type = in_invoice` และ `order_type = deposit_payment`
- คง `SO Reference` เดิมไว้สำหรับฝั่ง `Customer Invoice`
- แยกงานออกเป็นโมดูลเสริม เพื่อไม่แก้ไฟล์ของโมดูลเดิมตรง ๆ

## แนวทางที่เลือก
- ใช้แนวทาง `แบบ A`
- เปลี่ยนวิธีติดตั้งเป็น `โมดูลเสริม`
- เพิ่มฟิลด์ใหม่ชื่อ `deposit_po_ref` ชนิด `Many2one('purchase.order')`
- ไม่ลบ ไม่เปลี่ยนชนิด และไม่ย้ายความหมายของฟิลด์เดิม `deposit_so_ref`
- inherit model และ view จากโมดูลเดิม เพื่อแสดงฟิลด์ตามประเภทเอกสาร

## การออกแบบหน้าจอ
- ถ้าเป็น `Customer Invoice` และ `Type = Deposit Payment`
- ให้แสดง `deposit_so_ref` ด้วย label `SO Reference`
- ถ้าเป็น `Vendor Bill` และ `Type = Deposit Payment`
- ให้แสดง `deposit_po_ref` ด้วย label `PO Reference`
- ฟิลด์ทั้งสองต้องไม่แสดงพร้อมกัน
- เอกสารประเภทอื่นต้องไม่เปลี่ยนพฤติกรรมเดิม

## การออกแบบข้อมูล
- โมดูลใหม่ควรใช้ชื่อแนว `autoinfo_fixes_...` ตามแนวทางของโปรเจกต์
- ไฟล์โมเดลในโมดูลเสริมจะ inherit `account.move`
- เพิ่มฟิลด์:

```python
deposit_po_ref = fields.Many2one('purchase.order', string='PO Reference')
```

- ไฟล์ view ในโมดูลเสริมจะ inherit view ของ `dtr_customer_invoices.dtr_view_move_form`
- ปรับเงื่อนไข `attrs` ของฟิลด์อ้างอิงให้แยกตาม `move_type`
- แนวทาง view:
- แสดง `deposit_so_ref` เมื่อ `move_type` เป็นฝั่งขายและ `order_type = deposit_payment`
- แสดง `deposit_po_ref` เมื่อ `move_type = in_invoice` และ `order_type = deposit_payment`

## Dependency
- เนื่องจากมีการอ้างโมเดล `purchase.order`
- โมดูลเสริมต้อง depend อย่างน้อยกับ:
- `account`
- `purchase`
- `dtr_customer_invoices`
- `dtr_deposit_payment`
- `autoinfo_accounting_form`

## Data Flow
- ผู้ใช้สร้างหรือเปิด `Vendor Bill`
- ผู้ใช้เลือก `Type = Deposit Payment`
- ระบบแสดง `PO Reference`
- ผู้ใช้เลือก `Purchase Order` ที่เกี่ยวข้อง
- flow ของ `Add Deposit Payment` และ wizard ใน `dtr_deposit_payment` ทำงานตามเดิม
- ฝั่ง `Customer Invoice` ยังใช้ `SO Reference` จากโมดูลเดิมตามเดิม

## สิ่งที่ไม่เปลี่ยน
- ไม่เปลี่ยนค่า `order_type = deposit_payment`
- ไม่เปลี่ยนปุ่ม `Add Deposit Payment`
- ไม่เปลี่ยนการคำนวณ deposit และ deduct
- ไม่แก้รายงานที่อ้าง `deposit_so_ref`
- ไม่ทำ migration ข้อมูลเก่า
- ไม่แก้ไฟล์ของ `autoinfo_accounting_form` ตรง ๆ

## ความเสี่ยง
- รายงานหรือโค้ดภายนอกที่อ่าน `deposit_so_ref` เพื่อใช้กับ `Vendor Bill` จะยังไม่เห็น `deposit_po_ref`
- แต่ใน scope นี้ถือว่ายอมรับได้ เพราะผู้ใช้ขอแก้เฉพาะหน้าจอ
- หากลำดับการโหลด view ไม่ถูกต้อง อาจทำให้ฟิลด์ซ้อนหรือแสดงไม่ตามเงื่อนไข

## การทดสอบที่ต้องผ่าน
- `Customer Invoice` แบบ `deposit_payment` ยังแสดง `SO Reference`
- `Vendor Bill` แบบ `deposit_payment` แสดง `PO Reference`
- `Vendor Bill` แบบอื่นไม่แสดง `PO Reference`
- ปุ่มและ wizard ของ deposit เดิมยังเปิดได้ตามปกติ
- ไม่มี error จากการโหลด view หรือ model
- การติดตั้งและถอนติดตั้งโมดูลเสริมไม่ทำให้โมดูลเดิมเสีย

## เกณฑ์สำเร็จ
- ผู้ใช้เห็น `PO Reference` บน `Vendor Bill` เมื่อเลือก `Type = Deposit Payment`
- ฝั่ง `Customer Invoice` และ flow deposit เดิมยังทำงานได้เหมือนเดิม
- การแก้ไขอยู่ในขอบเขตเล็ก, rollback ได้ง่าย, และทำงานผ่านโมดูลเสริม

## Credits
- The Auto-Info Co., Ltd. : Dev Team / Mr. Nattanon Vinyangkoon
- AI Coding Assistant: TRAE SOLO / MICROSOFT 365 COPILOT
