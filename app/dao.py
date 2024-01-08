from app.models import (KhachHang, LoaiKhachHang, Phong, LoaiPhong, PhieuThuePhong, LoaiPhong_DonVitinhTien,
                        DonViTinhTien, UserRoleEnum, NguoiQuanTri, PhieuDanhGia, ThongSoQuyDinh, NhuCau, DsPhongDaDat,
                        PhieuDatPhong, DsPhieuDatPhong, DsPhongDaThue, DsPhieuThuePhong)
import hashlib


def get_KhachHang_by_id(id):
    return KhachHang.query.get(id)


def get_loaiphong_by_id(id):
    return LoaiPhong.query.get(id)


def get_phong_by_id(id):
    return Phong.query.get(id)


def get_donvitinhtien_by_id(id):
    return DonViTinhTien.query.get(id)


def get_NguoiQuanTri_by_id(id):
    return NguoiQuanTri.query.get(id)


def get_phieudatphong_by_id(id):
    return PhieuDatPhong.query.get(id)


def get_loaiphong_donvitinhtien_by_id(id):
    return LoaiPhong_DonVitinhTien.query.get(id)


def get_KhachHang_by_tenkhachhang(tenkhachhang):
    khachhang = KhachHang.query

    if tenkhachhang:
        khachhang = khachhang.filter_by(tenkhachhang=tenkhachhang).first()

    return khachhang


def get_KhachHang_by_cccd(cccd):
    khachhang = KhachHang.query

    if cccd:
        khachhang = khachhang.filter_by(cccd=cccd).first()

    return khachhang


def get_LoaiKhachHang_by_tenLoaiKhachHang(ten):
    loaikhachhang = LoaiKhachHang.query

    if ten:
        loaikhachhang = loaikhachhang.filter_by(tenloaikhachhang=ten).first()

    return loaikhachhang


def get_loaiphong_by_tenloaiphong(ten):
    loaiphong = LoaiPhong.query

    if ten:
        loaiphong = loaiphong.filter_by(tenloaiphong=ten).first()

    return loaiphong


def get_phong_by_loaiphong_id(id):
    phong = Phong.query
    if id:
        phong = phong.filter_by(loaiphong_id=id).all()

    return phong


def get_phong_by_tenphong(ten):
    phong = Phong.query
    if ten:
        phong = phong.filter_by(tenphong=ten).first()

    return phong


def get_phong_available_by_loaiphong_id(id):
    phong = Phong.query
    if id:
        phong = phong.filter_by(tinhtrang=False, loaiphong_id=id).all()

    return phong


def get_phong_available_by_tinhtrang():
    return Phong.query.filter_by(tinhtrang=False).all()


def get_phong_unavailable_by_tinhtrang():
    return Phong.query.filter_by(tinhtrang=True).all()


def get_donvitinhtien_by_ten(ten):
    dvtt = DonViTinhTien.query
    if ten:
        dvtt = dvtt.filter_by(ten=ten).first()

    return dvtt


def get_loaiphong_donvitinhtien_by_2id(id1, id2):
    loaiphong_dvtt = LoaiPhong_DonVitinhTien.query
    if id1 and id2:
        loaiphong_dvtt = loaiphong_dvtt.filter_by(loaiphong_id=id1, donvitinhtien_id=id2).first()

    return loaiphong_dvtt


def get_all_phong_donvitinhtien():
    return LoaiPhong_DonVitinhTien.query.all()


def get_phong_donvitinhtien_by_loaiphong_id(id):
    phong_dvtt = LoaiPhong_DonVitinhTien.query
    if id:
        phong_dvtt = phong_dvtt.filter_by(loaiphong_id=id).all()

    return phong_dvtt


def get_phong_donvitinhtien_by_2id(id1, id2):
    phong_dvtt = LoaiPhong_DonVitinhTien.query
    if id1 and id2:
        phong_dvtt = phong_dvtt.filter_by(loaiphong_id=id1, donvitinhtien_id=id2).first()

    return phong_dvtt


def get_unit_by_unit_name(name):
    dvtt = DonViTinhTien.query
    if name:
        dvtt = dvtt.filter_by(ten=name).first()

    return dvtt


def get_value_by_key(key):
    value = ThongSoQuyDinh.query
    if key:
        value = value.filter_by(key=key).first()

    return value


def get_dspdd_by_phieu_dat_phong_id(id):
    dspdd = DsPhongDaDat.query
    if id:
        dspdd = dspdd.filter_by(phieudatphong_id=id).all()

    return dspdd


def get_dspdt_by_phieu_thue_phong_id(id):
    dspdt = DsPhongDaThue.query
    if id:
        dspdt = dspdt.filter_by(phieuthuephong_id=id).all()

    return dspdt


def get_dsptp_by_phieu_thue_phong_id(id):
    dsptp = DsPhieuThuePhong.query
    if id:
        dsptp = dsptp.filter_by(phieuthuephong_id=id).all()

    return dsptp


def get_dspdp_by_phieu_dat_phong_id(id):
    dspdp = DsPhieuDatPhong.query
    if id:
        dspdp = dspdp.filter_by(phieudatphong_id=id).all()

    return dspdp


def get_dspdp_by_2id(id1, id2):
    dspdp = DsPhieuDatPhong.query
    if id1 and id2:
        dspdp = dspdp.filter_by(phieudatphong_id=id1, khachhang_id=id2).all()

    return dspdp


def get_nhucau_by_phieudatphong_id(id):
    nhucau = NhuCau.query
    if id:
        nhucau = nhucau.filter_by(phieudatphong_id=id).first()

    return nhucau


def auth_nguoiquantri(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return NguoiQuanTri.query.filter(NguoiQuanTri.username.__eq__(username.strip()),
                                     NguoiQuanTri.password.__eq__(password)).first()
