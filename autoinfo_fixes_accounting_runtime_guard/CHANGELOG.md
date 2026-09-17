# CHANGELOG

## 15.0.1.0.1 - 2026-09-17

### Type
- Documentation update

### Summary
- เพิ่มคู่มือแก้ปัญหา `pyOpenSSL / cryptography / cffi` ชนกันใน system Python
- เพิ่มขั้นตอน recovery แบบทีละ step ตั้งแต่ตรวจ path, backup package ฝั่ง `/usr/local`, reinstall package ฝั่ง `apt`, verify Python SSL stack, จนถึงทดสอบ Odoo
- เพิ่มคำเตือนในคู่มือติดตั้งว่าไม่ควรใช้ `pip install --upgrade cryptography pyOpenSSL cffi` ทับ system Python โดยตรง

### Impact
- ช่วยลดความเสี่ยงที่ Odoo และ `pip` จะพังพร้อมกันจาก package SSL stack ชนกัน
- ทำให้ทีมสามารถกู้ environment ที่พังกลับมาได้ด้วยคำสั่ง copy-paste

### Related Commit
- `741e61a` `docs(runtime-guard): add pyopenssl recovery guide`

## 15.0.1.0.0 - 2026-09-17

### Type
- Initial release

### Summary
- สร้างโมดูล `autoinfo_fixes_accounting_runtime_guard`
- เพิ่ม model `autoinfo.runtime.guard.run`
- เพิ่ม model `autoinfo.runtime.guard.check`
- เพิ่ม wizard `autoinfo.runtime.guard.fix.help`
- เพิ่มเมนู `Runtime Guard`
- เพิ่มชุดตรวจ Version 1 สำหรับ runtime path, Python package, dependency chain, schema risk, module state, และ external DB warning
- เพิ่มเอกสาร `README.md`, `installation_guide.md`, `technical_guide.md`, `troubleshooting.md`, `user_guide.md`
- เพิ่ม UI, ACL, cron scaffold, และ regression tests

### Impact
- รวมปัญหา runtime ที่เจอจริงไว้ในโมดูลเดียว
- ทำให้ผู้ดูแลระบบมีจุดศูนย์กลางสำหรับตรวจปัญหาและเปิดคำสั่งแก้แบบ copy-paste

### Related Commits
- `1352cf3` `test: add runtime guard service red tests`
- `752fd58` `feat: add runtime guard audit service`
- `7fa7582` `feat: add runtime guard ui and fix help wizard`
- `326ccda` `docs: add runtime guard admin guidance`
- `195a978` `docs(runtime-guard): add full thai installation guides`

## Commit History Summary

### `1352cf3`
- เพิ่ม red tests สำหรับ service layer เพื่อยืนยันพฤติกรรมก่อนลง implementation

### `752fd58`
- เพิ่ม model หลักและ service layer ของ Runtime Guard

### `7fa7582`
- เพิ่ม wizard, UI, ACL และ flow การเปิด `Fix Help` กับ `Mark Reviewed`

### `326ccda`
- เพิ่มเอกสาร admin guidance ชุดแรกของโมดูล

### `195a978`
- เพิ่มคู่มือภาษาไทยแบบเต็มสำหรับติดตั้ง ใช้งาน เทคนิค และ troubleshooting

### `741e61a`
- เพิ่มคู่มือ recovery สำหรับปัญหา `pyOpenSSL` ชนกับ `cryptography/cffi`
