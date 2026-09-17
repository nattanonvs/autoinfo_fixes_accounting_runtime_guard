# Technical Guide

## Main Models

- `autoinfo.runtime.guard.run`
- `autoinfo.runtime.guard.check`
- `autoinfo.runtime.guard.fix.help`

## Check Set V1

- runtime path
- python package
- dependency chain
- schema risk
- module state
- external DB warning

## Design Notes

- ใช้ service layer แยกจาก UI
- ใช้ wizard สำหรับแสดงคำสั่งแก้
- `Mark Reviewed` ใช้เก็บ audit trail
- safe auto-fix จำกัดเฉพาะงานในโมดูลนี้
