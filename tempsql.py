#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 16:04:34 2024

@author: russ
"""
SELECT         photo.name,         photo.photo_fn,         photo.id,         photoshow.name,         photoshow.id,         photoshow_photo.seq_no,         photoshow_photo.photoshow_id       FROM   photo       JOIN   photoshow_photo       ON   photoshow_photo.photo_id = photo.id       JOIN   photoshow       ON   photoshow.id = photoshow_photo.photoshow_id       WHERE  photoshow.id = :id;     '







SELECT         photo.name,
photo.photo_fn,
photo.id,
photoshow.name,
photoshow.id,
photoshow_photo.seq_no,
photoshow_photo.photoshow_id
FROM   photo
JOIN   photoshow_photo       ON   photoshow_photo.photo_id = photo.id
JOIN   photoshow       ON   photoshow.id = photoshow_photo.photoshow_id
WHERE  photoshow.id = 29;


bad:


SELECT
  photo.name,
  photo.photo_fn,
  photo.id,
  photoshow.name,
  photoshow.id
FROM   photo
JOIN   photoshow_photo
ON     photoshow_photo.photo_id = photo.id
JOIN   photoshow
ON     photoshow.id = photoshow_photo.photoshow_id

WHERE  photoshow.id = 29;


returned 3 rows


SELECT "id", "photoshow_id", "photo_id", "seq_no", "no_comma"

FROM "photoshow_photo"

WHERE photoshow.id = 29
ORDER BY "photoshow_photo.id" ASC

===================== 0k 3 rows ====================
SELECT
  photo.name,
  photo.photo_fn,
  photo.id,
  photoshow.name,
  photoshow.id,
  photoshow_photo.seq_no,
  photoshow_photo.photoshow_id
FROM   photo
JOIN   photoshow_photo
ON     photoshow_photo.photo_id = photo.id
JOIN   photoshow
ON     photoshow.id = photoshow_photo.photoshow_id
WHERE  photoshow.id = 29;