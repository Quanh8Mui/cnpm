from app.models import (KhachHang, LoaiKhachHang, Phong, LoaiPhong, PhieuThuePhong, LoaiPhong_DonVitinhTien,
                        DonViTinhTien, UserRoleEnum, NguoiQuanTri, PhieuDanhGia, ThongSoQuyDinh, NhuCau)
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


def get_phong_available_by_loaiphong_id(id):
    phong = Phong.query
    if id:
        phong = phong.filter_by(tinhtrang=False, loaiphong_id=id).all()

    return phong


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


def auth_nguoiquantri(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return NguoiQuanTri.query.filter(NguoiQuanTri.username.__eq__(username.strip()),
                                     NguoiQuanTri.password.__eq__(password)).first()
