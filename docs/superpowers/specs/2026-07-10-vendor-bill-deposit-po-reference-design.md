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
- ปรับ dropdown ของทั้ง `PO Reference` และ `SO Reference` ให้แสดงเฉพาะรายการที่เกี่ยวข้องตามคู่ค้า และเป็นเอกสารที่ยืนยันแล้ว
- เมื่อผู้ใช้เลือก `PO Reference` หรือ `SO Reference` ให้ sync ข้อมูลต้นทางระดับหัวเอกสารและระดับ line โดยไม่สร้าง line ใหม่

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
- Dropdown filtering (ข้อ 2)
- `PO Reference` ต้องเห็นเฉพาะ `Purchase Order` ของคู่ค้าเดียวกัน และอยู่ในสถานะ `purchase` หรือ `done`
- `SO Reference` ต้องเห็นเฉพาะ `Sale Order` ของคู่ค้าเดียวกัน และอยู่ในสถานะ `sale` หรือ `done`

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
- แนวทาง domain:
- `deposit_po_ref` ใช้ domain: `[('partner_id', '=', partner_id), ('state', 'in', ['purchase', 'done'])]`
- `deposit_so_ref` ใช้ domain: `[('partner_id', '=', partner_id), ('state', 'in', ['sale', 'done'])]`

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
- เมื่อเลือก `PO Reference`
- ระบบต้องเติมข้อมูลต้นทางระดับหัวเอกสาร เช่น `po_origin` และ/หรือ `invoice_origin` ตาม pattern เดิมของระบบซื้อ
- ระบบต้องพยายาม map `purchase_line_id` และ `vendor_source_doc` ลง `invoice_line_ids` ที่มีอยู่แล้ว
- เมื่อเลือก `SO Reference`
- ระบบต้องเติมข้อมูลต้นทางระดับหัวเอกสาร เช่น `origin_second` และ/หรือ `invoice_origin` ตาม pattern เดิมของระบบขาย
- ระบบต้องพยายาม map `sale_line_ids` ลง `invoice_line_ids` ที่มีอยู่แล้ว
- การ map line ใช้ `product_id` เป็นตัวจับคู่หลัก
- ถ้ามีหลาย line ของ product เดียวกัน ให้จับคู่ตามลำดับที่พบ
- ถ้าไม่เจอ line ที่ match กัน ให้ข้ามโดยไม่สร้าง line ใหม่

## สิ่งที่ไม่เปลี่ยน
- ไม่เปลี่ยนค่า `order_type = deposit_payment`
- ไม่เปลี่ยนปุ่ม `Add Deposit Payment`
- ไม่เปลี่ยนการคำนวณ deposit และ deduct
- ไม่แก้รายงานที่อ้าง `deposit_so_ref`
- ไม่ทำ migration ข้อมูลเก่า
- ไม่แก้ไฟล์ของ `autoinfo_accounting_form` ตรง ๆ
- ไม่สร้าง line ใหม่จาก `PO/SO`
- ไม่ลบ line เดิมของเอกสาร
- ไม่เปลี่ยน wizard เดิมของฝั่งซื้อหรือฝั่งขาย

## ความเสี่ยง
- รายงานหรือโค้ดภายนอกที่อ่าน `deposit_so_ref` เพื่อใช้กับ `Vendor Bill` จะยังไม่เห็น `deposit_po_ref`
- แต่ใน scope นี้ถือว่ายอมรับได้ เพราะผู้ใช้ขอแก้เฉพาะหน้าจอ
- หากลำดับการโหลด view ไม่ถูกต้อง อาจทำให้ฟิลด์ซ้อนหรือแสดงไม่ตามเงื่อนไข
- การจับคู่ line ด้วย `product_id` อาจเชื่อมได้ไม่ครบ หากเอกสารมีหลายบรรทัดสินค้าซ้ำกันและไม่มี key แยกอื่น
- เนื่องจากไม่สร้าง line ใหม่ กรณีเอกสารต้นทางมี line แต่ใบ deposit ไม่มี line ที่ match กัน จะเชื่อมได้เฉพาะหัวเอกสาร

## การทดสอบที่ต้องผ่าน
- `Customer Invoice` แบบ `deposit_payment` ยังแสดง `SO Reference`
- `Vendor Bill` แบบ `deposit_payment` แสดง `PO Reference`
- `Vendor Bill` แบบอื่นไม่แสดง `PO Reference`
- ปุ่มและ wizard ของ deposit เดิมยังเปิดได้ตามปกติ
- ไม่มี error จากการโหลด view หรือ model
- การติดตั้งและถอนติดตั้งโมดูลเสริมไม่ทำให้โมดูลเดิมเสีย
- dropdown ของ `PO Reference` ต้องไม่แสดง PO ของคู่ค้าคนละราย
- dropdown ของ `PO Reference` ต้องไม่แสดง PO ที่สถานะไม่ใช่ `purchase/done`
- dropdown ของ `SO Reference` ต้องไม่แสดง SO ของคู่ค้าคนละราย
- dropdown ของ `SO Reference` ต้องไม่แสดง SO ที่สถานะไม่ใช่ `sale/done`
- เลือก `PO Reference` แล้วหัวเอกสารต้องได้ค่า source document ตาม pattern ของฝั่งซื้อ
- line ที่ `product_id` ตรงกันต้องได้ `purchase_line_id` และ/หรือ `vendor_source_doc` ตามที่ระบบรองรับ
- เลือก `SO Reference` แล้วหัวเอกสารต้องได้ค่า source document ตาม pattern ของฝั่งขาย
- line ที่ `product_id` ตรงกันต้องได้ `sale_line_ids`
- line ที่ match ไม่ได้ต้องไม่ถูกลบ และต้องไม่ถูกสร้างใหม่

## เกณฑ์สำเร็จ
- ผู้ใช้เห็น `PO Reference` บน `Vendor Bill` เมื่อเลือก `Type = Deposit Payment`
- ฝั่ง `Customer Invoice` และ flow deposit เดิมยังทำงานได้เหมือนเดิม
- การแก้ไขอยู่ในขอบเขตเล็ก, rollback ได้ง่าย, และทำงานผ่านโมดูลเสริม

## Credits
- The Auto-Info Co., Ltd. : Dev Team / Mr. Nattanon Vinyangkoon
- AI Coding Assistant: TRAE SOLO / MICROSOFT 365 COPILOT
