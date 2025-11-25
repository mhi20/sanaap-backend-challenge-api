<div dir="rtl">

#  راه‌اندازی پروژه Django با Docker Compose

سرویس های استفاده شده در این پروژه: 
 - Redis
 - PostgresSql
 - Minio
 - Nginx

 این راهنما مخصوص محیط **Development** نوشته شده است

---

##  پیش‌نیازها

  مواردی که باید روی سیستم نصب باشند:

- Docker  
- Docker Compose

---

##  ساختار پوشه‌های Docker

پروژه در محیط توسعه از مسیر زیر استفاده می‌کند:
```
deployments/development/
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── init-db.sh
└── nginx/
└── nginx.conf
```

---
## ساخت فایل محیطی `.env`

در مسیر زیر یک فایل `.env` بسازید یا نام .env.sample را به .env تغییر دهید:

و مقادیر داخل فایل را براساس تنظیمات خودتان مقداردهی کنید

``
deployments/development/.env
``

##  اجرای پروژه 
``
docker compose -f deployments/development/docker-compose.yml up -d
``

##  توضیح اسکریپت هایی که در آپ شدن پروژه دخیل هستند 

### deployments/development/init-db.sh :

توضیحات اسکریپت:

-	بررسی می‌کند دیتابیس وجود دارد یا نه

-	اگر دیتابیس رو پیدا نکرد ، دیتابیس موردنظر را میسازد

-	براساس کاربر مشخص شده دسترسی میدهد

این مرحله قبل از اجرای Django اجرا می‌شود.


### deployments/development/entrypoint.sh :

این اسکریپت وظایف زیر را انجام می‌دهد:
1.	اجرای init-db.sh
2.	اجرای migrations
3.	اجرای collectstatic
4.	اجرای Gunicorn با workerهای Uvicorn


## تنظیم Minio برای ذخیره‌سازی فایل‌ها

برای اینکه فایل‌های مدل Document به‌صورت public باشند، لازم است در Minio یک باکت با نام **documents** ساخته شود و سطح دسترسی آن روی حالت عمومی public تنظیم بشود.

### مراحل انجام کار

ابتدا وارد کانتینر Minio شوید:

```
docker exec -it minio sh
```

سپس یک alias برای Minio CLI داخل کانتینر تنظیم کنید:

```
mc alias set localminio http://localhost:9000 minioadmin minioadmin
```

### ایجاد باکت documents

```
mc mb --ignore-existing localminio/documents
```

### تنظیم سطح دسترسی باکت روی Public

```
mc anonymous set download localminio/documents
```


## مستندات API

در این پروژه از **drf-spectacular** برای تولید OpenAPI Schema و نمایش مستندات API استفاده شده است.

### مسیرهای مستندات

| مسیر | توضیح |
|------|--------|
| `/api/schema/` | خروجی JSON از OpenAPI Schema (مناسب برای ابزارها و کلاینت‌ها) |
| `/api/docs/swagger/` | رابط کاربری Swagger UI برای مشاهده و تست API |
| `/api/docs/redoc/` | رابط کاربری ReDoc برای مشاهده مستندات API |

### نحوه دسترسی

بعد از اجرای پروژه، مستندات از طریق لینک‌های زیر در دسترس خواهد بود:

- **Swagger UI:**  
```
http://localhost:8000/api/docs/swagger/
```

- **ReDoc:**

```
http://localhost/api/docs/redoc/
```

</div>