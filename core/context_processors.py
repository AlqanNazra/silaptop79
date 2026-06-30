import datetime
from inventori.models import Pengajuan, Peminjaman

def notification_counts(request):
    try:
        today = datetime.date.today()
        
        # HC notifications count: Pengajuan masuk/menunggu + Pengembalian + Jatuh tempo
        p_menunggu_hc = Pengajuan.objects.filter(status__in=['menunggu', 'pending']).count()
        p_kembali_hc = Peminjaman.objects.filter(status='dikembalikan').count()
        p_aktif_hc = Peminjaman.objects.filter(status__in=['dipinjam', 'aktif'])
        p_jt_hc = sum(1 for p in p_aktif_hc if p.tanggal_jatuh_tempo and (p.tanggal_jatuh_tempo - today).days <= 7)
        total_hc = p_menunggu_hc + p_kembali_hc + p_jt_hc

        # IT notifications count: Pengajuan masuk/menunggu + Pengembalian
        p_menunggu_it = Pengajuan.objects.filter(status__in=['menunggu', 'pending']).count()
        p_kembali_it = Peminjaman.objects.filter(status='dikembalikan').count()
        total_it = p_menunggu_it + p_kembali_it

        has_active_borrow = False
        if request.user.is_authenticated:
            id_user = getattr(request.user, 'id_user', None)
            if not id_user:
                id_user = getattr(request.user, 'username', None)
            if id_user:
                has_active_borrow = Peminjaman.objects.filter(
                    id_user=id_user,
                    status__in=['dipinjam', 'aktif']
                ).exists()

        return {
            'total_notifikasi_hc': total_hc,
            'total_notifikasi_it': total_it,
            'has_active_borrow': has_active_borrow,
        }
    except Exception:
        return {
            'total_notifikasi_hc': 0,
            'total_notifikasi_it': 0,
            'has_active_borrow': False,
        }
