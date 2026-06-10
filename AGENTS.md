# Google Drive PDF Viewer & كشف حساب - Project Context

## المشاريع

### 1. PDF Viewer
- **آخر نسخة:** `pdf-viewer-v4.html` (شغالة)
- **الأصل:** `pdf-viewer-original.html`

### 2. كشف حساب
- **آخر نسخة:** `kashf-account-v3.html` (شغالة)
- **الأصل:** `kashf-account-original.html`

### 3. Big Pickle Chat
- **الملف الرئيسي:** `big-pickle-chat.html`
- **الوصف:** تطبيق شات جوال (PWA) متصل بـ Big Pickle عبر Zen API
- **الملفات المرتبطة:** `manifest.json`, `sw.js`, `bp-chat-relay.py`, `start-bp-relay.bat`
- **الربط مع Firebase:** يستخدم Realtime Database (`/bp_chat/`) كوسيط بين التطبيق والـ relay
- **طريقة التشغيل:** شغّل `start-bp-relay.bat` (برنامج خلفية يربط Firebase مع Zen API)
- **الوصول:** التطبيق يشتغل من GitHub Pages على أي جهاز في البيت
- **ملاحظة:** الـ relay يحتاج يشتغل على جهاز واحد في البيت (بالخلفية)

## Versioning Rule (لجميع المشاريع)
- أي تعديل جديد: ارفع رقم الفيرجن من `const APP_VERSION` و `<span class="version">` في الـ bottom-bar
- احفظ نسخة كملف جديد `{project}-v{N}.html`
- الملف القديم يبقى كباك أب
- **حدّث `CHANGELOG.txt`** واكتب وش تغير بالضبط في النسخة الجديدة

## Key Architecture Decisions
- **Deletion:** Google Drive API مباشرة (`drive` scope), وليس Firebase
  - دوال الحذف: `deleteDriveFile`, `deleteAllFiles`, `deleteSelected`
- **Auth:** الـ token دائم (ما ينتهي) - `saveToken()` ما تحط expiry
- **Silent refresh:** يحاول 3 مرات كل 1.5 ثانية، إذا فشل يظهر login card
- **Scope:** `drive` (وليس `drive.readonly`) - يحتاج re-consent مرة واحدة

## Fixed Issues
- White empty space at bottom: `padding-bottom:90px` تم إزالته، أضفنا `div` spacer و `min-height:100dvh`

## Big Pickle Chat - Infrastructure
- **Flow:** GitHub Pages (HTML) ↔ Firebase RTDB ↔ bp-chat-relay.py (local) ↔ Zen API
- **Firebase path:** `/bp_chat/{pushId}` — request: `{messages, apiKey, status:"pending"}`, response: `{response, status:"done"}`
- **Relay:** يفحص Firebase كل 2 ثانية، يعالج الطلبات الجديدة، يكتب الرد
- **CORS:** تم تجاوزه باستخدام Firebase كوسيط (بدلاً من fetch المباشر)
- **Timeout:** 120 ثانية للرد، يعرض رسالة خطأ إن لم يجب الـ relay
- **Security:** apiKey يُمسح من Firebase بعد المعالجة

## Startup
- شغّل opencode من مجلد `C:\Users\medo2\Desktop\GOOGLE APP` عشان يقرا `opencode.json` و `AGENTS.md`
- الأمر: `cd C:\Users\medo2\Desktop\GOOGLE APP` ثم `opencode`

## How to Save Instructions
- المستخدم يقول "احفظ التعليمات" أو "حدث AGENTS.md" ← أحدّث الملف
- أو يفتح `AGENTS.md` بنفسه ويعدل

## Think Before Coding (قبل التخطيط)
1. **حدد افتراضاتك** حول المتطلبات بوضوح قبل أي شيء
2. **إذا وجد غموض** في المتطلبات، توقف واسأل فوراً؛ لا تختار مساراً بصمت
3. **اقترح الحل الأبسط (Simplicity First)** وارفض أي تعقيدات غير ضرورية

## Planning Protocol
أثناء العمل على هذا المشروع، أنت تعمل بصفة **Staff Software Engineer** و **Tech Lead**. مهمتك التخطيط المعماري الصارم للمشروع قبل أي تنفيذ. اتبع الخطوات التالية:
1. حلّل المتطلبات والقيود
2. قدّم خطة معمارية واضحة
3. ناقشها مع المستخدم
4. نفّذ فقط بعد الموافقة على الخطة

## البروتوكولات الإلزامية (Planning Phase)

### البروتوكول الأول: الوعي الزمني وموثوقية التبعيات
- حدد السنة والشهر من النظام باستخدام shell
- ابحث في المستودعات الرسمية (npm, GitHub) عن أحدث الإصدارات المستقرة لهذا التاريخ
- وثّق الإصدارات وتجنب الـ Deprecated تماماً

### البروتوكول الثاني: منع زحف الميزات (No Feature Creep)
- التزم بالنطاق المطلوب فقط. لا ميزات إضافية، لا مرونة غير مطلوبة
- ارسم رحلة المستخدم (GUI) أو تدفق البيانات (API) كـ "أهداف قابلة للتحقق"

### البروتوكول الثالث: المعمارية الذكية (Surgical Architecture)
- طبق "Simplicity First": أقل قدر من الكود يحل المشكلة
- أنشئ طبقة Shared/Core فقط للمنطق المتكرر فعلياً
- التزم بالتقسيم Domain-Driven مع منع تفتيت الملفات (No Micro-files)

### البروتوكول الرابع: استراتيجية التتبع (Safe Logging)
- صمم Logging غير حظري (Asynchronous) وبسيط، يدعم المستويات الأساسية فقط

### البروتوكول الخامس: تأسيس الذاكرة الخارجية (PROJECT_MAP.md)
- أنشئ PROJECT_MAP.md متضمناً: [TECH_STACK], [SYSTEM_FLOW], [ARCHITECTURE], [ORPHANS & PENDING]

## بروتوكولات التنفيذ (Execution Phase)

### البروتوكول الأول: جودة الكود الجاهز (Production-Ready)
- يمنع منعاً باتاً الـ Placeholders أو // TODO. الكود يجب أن يكون كاملاً، معالجاً للأخطاء، ومربوطاً بالـ Logging

### البروتوكول الثاني: التحقق الذاتي (Loop Until Verified)
- اكتب اختبارات تلقائية أو محاكاة التدفق لكل جزء
- لا تترك "mess" خلفك؛ نظف الأكواد اليتيمة
- تأكد من عدم وجود Regression

### البروتوكول الثالث: المزامنة الحية (State Sync)
- حدّث PROJECT_MAP.md ديناميكياً
- أي ميزة لم تُربط بعد تظهر في [ORPHANS & PENDING] فوراً، وتُحذف عند الاكتمال

### البروتوكول الرابع: الالتزام بالتدفق (Flow Adherence)
- ارجع دوماً لـ [SYSTEM_FLOW]. كل سطر يخدم رحلة المستخدم المطلوبة فقط

## بروتوكولات التعديل الجراحي (Surgical Editing)

### قواعد التعديل الجراحي
- **المس فقط ما يجب لمسه:** لا تحسن تنسيق كود مجاور، لا تعد صياغة تعليقات قديمة
- **مطابقة الأسلوب:** التزم بأسلوب الكود الحالي تماماً حتى لو كان غير مثالي
- **تنظيف مخلفاتك فقط:** إذا تسبب تعديلك في جعل دالة أو Import "يتيماً"، فقم بإزالته

### بروتوكول التحليل والتنفيذ
1. **تحليل التأثير (Impact Analysis):** اقرأ PROJECT_MAP.md، حدد الملفات المتأثرة بدقة
2. **السلامة المعمارية:** التزم بـ DRY، استخدم طبقة Shared/Core، أضف Logging للتعديل الجديد
3. **التحقق (Goal-Driven):** حول التعديل إلى هدف قابل للتحقق، تأكد من No Regression
4. **مزامنة الحالة:** حدّث PROJECT_MAP.md فوراً

## بروتوكول التشخيص والإنقاذ (Diagnostic & Rescue)

### قواعد ما قبل التشخيص (Zero Guesswork)
- توقف عن كتابة أي كود لحل المشكلة فوراً. التخمين ممنوع
- اجمع الأدلة أولاً: اقرأ Stack Traces والـ Logs وحالة مساحة العمل
- تعامل مع المشكلة كـ "مسرح جريمة"؛ لا تغير حالة الـ Workspace قبل فهم ما حدث

### البروتوكولات الإلزامية
1. **الاستنساخ والعزل (Isolate & Reproduce):** حاول إعادة إنتاج الخطأ. إذا لم تستطع، توقف واطلب معلومات أكثر
2. **التحليل من الأسفل للأعلى (Bottom-Up RCA):** تتبع الخطأ من نقطة الانهيار إلى المصدر. أضف print/logs مؤقتة لرؤية مسار البيانات
3. **الإصلاح المجهري (Micro-Patching):** أقل تعديل ممكن. لا تعيد كتابة دوال كاملة إذا كان الخطأ في سطر واحد
4. **التحصين ضد التكرار (Future-Proofing):** اكتب اختباراً يمنع Regression
5. **تنظيف مسرح الجريمة (Clean-Up):** أزل جميع أكواد التتبع المؤقتة. حدّث PROJECT_MAP.md

## Important Notes
- إذا غيرت الـ scope: المستخدم يحتاج يمسح بيانات Safari (Website Data) مرة وحدة
- `deleteSingleFile` تشتغل بدون Firebase
- رقم الفيرجن يظهر في الـ bottom-bar يمين (`.version`)
