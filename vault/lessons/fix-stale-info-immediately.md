---
title: Fix stale info immediately
date: '2026-02-14'
memoryType: lesson
---
bird CLI was marked needs cookies in memory since day 1. Never tested. Worked the whole time. Stale info survives compaction and poisons future sessions. Don't defer corrections.
