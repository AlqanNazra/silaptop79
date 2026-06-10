import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "silaptop79.settings")
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from inventori.views import manajemen_laptop_page, detail_laptop_page, editdatalaptop_hc_view
from inventori.models import LaptopInventori

factory = RequestFactory()
request = factory.get('/hc/manajemen-laptop/')
user = User.objects.first()
if not user:
    user = AnonymousUser()
request.user = user
# We need to add session and messages middleware to the request
from django.contrib.messages.storage.fallback import FallbackStorage
setattr(request, 'session', 'session')
messages = FallbackStorage(request)
setattr(request, '_messages', messages)

try:
    response = manajemen_laptop_page(request)
    print("manajemen_laptop_page OK")
except Exception as e:
    import traceback
    traceback.print_exc()

request = factory.get('/hc/pengajuan-laptop/')
request.user = user
setattr(request, 'session', 'session')
setattr(request, '_messages', messages)
try:
    from inventori.views import pengajuan_page_view
    response = pengajuan_page_view(request)
    print("pengajuan_page_view OK")
except Exception as e:
    import traceback
    traceback.print_exc()

from inventori.models import Pengajuan
pengajuan = Pengajuan.objects.first()
if pengajuan:
    request = factory.get(f'/hc/detail-pengajuan/?id={pengajuan.id_pengajuan}')
    request.user = user
    setattr(request, 'session', 'session')
    setattr(request, '_messages', messages)
    try:
        from inventori.views import detailpengajuan_hc_view
        response = detailpengajuan_hc_view(request)
        print("detailpengajuan_hc_view OK")
    except Exception as e:
        import traceback
        traceback.print_exc()

# Let's also test detail_laptop_page
laptop = LaptopInventori.objects.first()
if laptop:
    request = factory.get(f'/hc/detail-laptop/{laptop.id_laptop_inventori}/')
    request.user = user
    setattr(request, 'session', 'session')
    setattr(request, '_messages', messages)
    try:
        response = detail_laptop_page(request, laptop.id_laptop_inventori)
        print("detail_laptop_page OK")
    except Exception as e:
        import traceback
        traceback.print_exc()

    request = factory.get(f'/hc/edit-laptop/{laptop.id_laptop_inventori}/')
    request.user = user
    setattr(request, 'session', 'session')
    setattr(request, '_messages', messages)
    try:
        response = editdatalaptop_hc_view(request, laptop.id_laptop_inventori)
        print("editdatalaptop_hc_view OK")
    except Exception as e:
        import traceback
        traceback.print_exc()

request = factory.get('/hc/riwayat-peminjaman/')
request.user = user
setattr(request, 'session', 'session')
setattr(request, '_messages', messages)
try:
    from inventori.views import riwayatpeminjamanlaptop_hc_view
    response = riwayatpeminjamanlaptop_hc_view(request)
    print("riwayatpeminjamanlaptop_hc_view OK")
except Exception as e:
    import traceback
    traceback.print_exc()
