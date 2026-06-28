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

        return {
            'total_notifikasi_hc': total_hc,
            'total_notifikasi_it': total_it,
        }
    except Exception:
        return {
            'total_notifikasi_hc': 0,
            'total_notifikasi_it': 0,
        }
