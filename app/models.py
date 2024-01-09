from sqlalchemy.orm import relationship
from app import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime, Boolean, SmallInteger
import enum
from datetime import datetime
from flask_login import UserMixin


class UserRoleEnum(enum.Enum):
    KHACH_HANG = 1
    ADMIN = 2
    NHAN_VIEN = 3


class LoaiKhachHang(db.Model):
    __tablename__ = 'loaikhachhang'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenloaikhachhang = Column(String(50), nullable=False)


class KhachHang(db.Model):
    __tablename__ = 'khachhang'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenkhachhang = Column(String(100), nullable=False)
    gioitinh = Column(String(12), default=None)
    cccd = Column(String(12), nullable=True, default=None)
    sdt = Column(String(12), default=None, nullable=True)
    diachi = Column(String(255), nullable=True, default=None)
    loaikhachhang_id = db.Column(Integer, ForeignKey(LoaiKhachHang.id), nullable=False)
    loaikhachhang = db.relationship('LoaiKhachHang', backref='loaikhachhangBackrefkhachhang')
    phieudanhgia = db.relationship('PhieuDanhGia', backref='phieudanhgiaBackrefkhachhang')
    # phieuthuephong = db.relationship('PhieuThuePhong',
    #                                  backref=' phieuthuephongBackrefKhachHang')
    # phieudatphong = db.relationship('PhieuDatPhong',
    #                                 backref=' phieudatphongBackrefKhachHang')
    dsphieudatphong = db.relationship('DsPhieuDatPhong', backref='DsPhieuDatPhongBackrefKhachHang')
    dsphieuthuephong = db.relationship('DsPhieuThuePhong', backref='DsPhieuThuePhongBackrefKhachHang')


class NguoiQuanTri(db.Model, UserMixin):
    __tablename__ = 'manager'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    name = Column(String(50), nullable=False)
    sdt = Column(String(12), nullable=False, unique=True)
    cccd = Column(String(50), nullable=False, unique=True)
    ngaysinh = Column(DateTime, nullable=False)
    diachi = Column(String(50), nullable=False)
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.ADMIN)


class LoaiPhong(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenloaiphong = Column(String(255), nullable=False, unique=True)
    loaiphong_donvitinhtien = db.relationship('LoaiPhong_DonVitinhTien',
                                              backref='Loaiphong_donvitinhtienBackrefPhong')


class Phong(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenphong = Column(String(255), nullable=False)
    ghichu = Column(String(255), nullable=False)
    tinhtrang = Column(Boolean, nullable=False, default=False)
    hinhanh = Column(String(255), default='https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704610281/khach-san'
                                          '-gan-day-9-min_kswi8g.png')
    loaiphong_id = db.Column(Integer, ForeignKey(LoaiPhong.id), nullable=False)

    phieudanhgia = db.relationship('PhieuDanhGia',
                                   backref=' phieudanhgiaBackrefLoaiPhong')
    dscacphongdadat = db.relationship('DsPhongDaDat', backref='dscacphongdadatBackrefPhong')
    dsphieuthuephong = db.relationship('DsPhongDaThue', backref='dsphieuthuephongBackrefPhong')


class DonViTinhTien(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(255), nullable=False)
    loaiphong_donvitinhtien = db.relationship('LoaiPhong_DonVitinhTien',
                                              backref='phong_donvitinhtienBackrefDonViTinhTien')


class LoaiPhong_DonVitinhTien(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    loaiphong_id = db.Column(Integer, ForeignKey(LoaiPhong.id), nullable=False)
    donvitinhtien_id = db.Column(Integer, ForeignKey(DonViTinhTien.id), nullable=False)
    giatien = db.Column(Float, nullable=False)
    dsphongdadat = db.relationship('DsPhongDaDat', backref='dsphongdadatBackrefLoaiPhong_DonVitinhTien')
    dsphongdathue = db.relationship('DsPhongDaThue', backref='dscacphongdathueBackrefLoaiPhong_DonVitinhTien')


class PhieuDatPhong(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    khachhang_id = db.Column(Integer, ForeignKey(KhachHang.id), nullable=False)
    ngaybatdau = Column(DateTime, nullable=False)
    ngayketthuc = Column(DateTime, nullable=False)
    dsphieudatphong = db.relationship('DsPhieuDatPhong', backref='DsPhieuDatPhongBackrefPhieuDatPhong')
    dsphongdathue = db.relationship('DsPhongDaDat', backref='dscacphongdadatBackrefPhieuDatPhong')
    khachhang = db.relationship('KhachHang', backref='khachhangBackrefPhieuDatPhong')


class DsPhieuDatPhong(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    khachhang_id = db.Column(Integer, ForeignKey(KhachHang.id), nullable=False)
    phieudatphong_id = db.Column(Integer, ForeignKey(PhieuDatPhong.id), nullable=False)


class DsPhongDaDat(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    phong_id = db.Column(Integer, ForeignKey(Phong.id), nullable=False)
    loaiphong_donvitinhtien_id = db.Column(Integer, ForeignKey(LoaiPhong_DonVitinhTien.id), nullable=False)
    phieudatphong_id = db.Column(Integer, ForeignKey(PhieuDatPhong.id), nullable=False)


class PhieuThuePhong(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngaybatdau = Column(DateTime, nullable=False)
    ngayketthuc = Column(DateTime, nullable=False)
    dsphieuthuephong = db.relationship('DsPhieuThuePhong', backref='DsPhieuThuePhongBackrefPhieuThuePhong')
    dscacphongthue = db.relationship('DsPhongDaThue', backref='dsphongdathueBackrefPhieuThuePhong')
    khachhang = db.relationship('KhachHang', backref='khachhangBackrefPhieuThuePhong')
    khachhang_id = db.Column(Integer, ForeignKey(KhachHang.id), nullable=False)


class DsPhieuThuePhong(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    khachhang_id = db.Column(Integer, ForeignKey(KhachHang.id), nullable=False)
    phieuthuephong_id = db.Column(Integer, ForeignKey(PhieuThuePhong.id), nullable=False)


class DsPhongDaThue(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    phong_id = db.Column(Integer, ForeignKey(Phong.id), nullable=False)
    loaiphong_donvitinhtien_id = db.Column(Integer, ForeignKey(LoaiPhong_DonVitinhTien.id), nullable=False)
    phieuthuephong_id = db.Column(Integer, ForeignKey(PhieuThuePhong.id), nullable=False)


class PhieuDanhGia(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngaydanhgia = Column(DateTime, nullable=False)
    soSao = Column(Integer, nullable=False)
    khachhang_id = db.Column(Integer, ForeignKey(KhachHang.id), nullable=False)
    phong_id = db.Column(Integer, ForeignKey(Phong.id), nullable=False)


class ThongSoQuyDinh(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(20), nullable=False, unique=True)
    value = Column(String(100), nullable=False)


class HoaDon(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngaytaohoadon = Column(DateTime, nullable=False)
    thanhtien = Column(Float, nullable=False)
    phieuthuephong_id = db.Column(Integer, ForeignKey(PhieuThuePhong.id), nullable=False)
    phieuthuephong = db.relationship('PhieuThuePhong',
                                     backref=' phieuthuephongBackrefhoadon')


class NhuCau(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nhucau = Column(String(255), nullable=False)
    phieudatphong_id = db.Column(Integer, ForeignKey(PhieuDatPhong.id), nullable=False)
    phieudatphong = db.relationship('PhieuDatPhong', backref='phieudatphongBackrefnhucau')


if __name__ == "__main__":
    from app import app

    with app.app_context():
        db.create_all()
        import hashlib

        loaikhachhang1 = LoaiKhachHang(tenloaikhachhang='Viet Nam')
        loaikhachhang2 = LoaiKhachHang(tenloaikhachhang='Others')
        db.session.add_all([loaikhachhang1, loaikhachhang2])
        db.session.commit()

        donvi1 = DonViTinhTien(ten='Giờ')
        donvi2 = DonViTinhTien(ten='Ngày')
        donvi3 = DonViTinhTien(ten='Tuần')
        db.session.add_all([donvi1, donvi2, donvi3])
        db.session.commit()

        loaiphong1 = LoaiPhong(tenloaiphong='Phổ thông')
        loaiphong2 = LoaiPhong(tenloaiphong='Thương gia')
        loaiphong3 = LoaiPhong(tenloaiphong='Phòng V.I.P')
        db.session.add_all([loaiphong1, loaiphong2, loaiphong3])
        db.session.commit()

        phong1 = Phong(tenphong='Phong 1', ghichu='Phòng có 1 máy lạnh , 1 giường , 1 TV', tinhtrang=False,
                       loaiphong_id=loaiphong1.id,
                       hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706902/tnfbho3bhagtndjbggyi.jpg")
        phong2 = Phong(tenphong='Phong 2', ghichu='Phòng có 1 máy lạnh , 1 giường , 1 TV', tinhtrang=False,
                       loaiphong_id=loaiphong1.id,
                       hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706902/tnfbho3bhagtndjbggyi.jpg")
        phong3 = Phong(tenphong='Phong 3', ghichu='Phòng có 1 máy lạnh , 1 giường , 1 TV', tinhtrang=False,
                       loaiphong_id=loaiphong1.id,
                       hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706902/tnfbho3bhagtndjbggyi.jpg")
        phong4 = Phong(tenphong='Phong 4', ghichu='Phòng có 1 máy lạnh , 1 giường , 1 TV', tinhtrang=False,
                       loaiphong_id=loaiphong1.id,
                       hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706902/tnfbho3bhagtndjbggyi.jpg")
        phong5 = Phong(tenphong='Phong 5', ghichu='Phòng có 1 máy lạnh , 1 giường , 1 TV', tinhtrang=False,
                       loaiphong_id=loaiphong1.id,
                       hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706902/tnfbho3bhagtndjbggyi.jpg")
        phong6 = Phong(tenphong='Phong 6', ghichu='Phòng có 1 máy lạnh , 1 giường , 1 TV', tinhtrang=False,
                       loaiphong_id=loaiphong1.id,
                       hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706902/tnfbho3bhagtndjbggyi.jpg")
        phong7 = Phong(tenphong='Phong 7', ghichu='Phòng có 1 máy lạnh , 1 giường , 1 TV', tinhtrang=False,
                       loaiphong_id=loaiphong1.id,
                       hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706902/tnfbho3bhagtndjbggyi.jpg")
        phong8 = Phong(tenphong='Phong 8', ghichu='Phòng có 1 máy lạnh , 1 giường , 1 TV', tinhtrang=False,
                       loaiphong_id=loaiphong1.id,
                       hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706902/tnfbho3bhagtndjbggyi.jpg")
        phong9 = Phong(tenphong='Phong 9', ghichu='Phòng có 1 máy lạnh , 1 giường , 1 TV', tinhtrang=False,
                       loaiphong_id=loaiphong1.id,
                       hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706902/tnfbho3bhagtndjbggyi.jpg")
        phong10 = Phong(tenphong='Phong 10', ghichu='Phòng có 1 máy lạnh , 1 giường , 1 TV', tinhtrang=False,
                        loaiphong_id=loaiphong1.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706902/tnfbho3bhagtndjbggyi.jpg")
        phong11 = Phong(tenphong='Phong 11', ghichu='Phòng có 1 máy lạnh , 1 giường , 1 TV', tinhtrang=False,
                        loaiphong_id=loaiphong1.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706902/tnfbho3bhagtndjbggyi.jpg")
        phong12 = Phong(tenphong='Phong 12', ghichu='Phòng có 1 máy lạnh , 1 giường , 1 TV', tinhtrang=False,
                        loaiphong_id=loaiphong1.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706902/tnfbho3bhagtndjbggyi.jpg")
        phong13 = Phong(tenphong='Phong 13', ghichu='Phòng có 1 máy lạnh , 1 giường , 1 TV', tinhtrang=False,
                        loaiphong_id=loaiphong1.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706902/tnfbho3bhagtndjbggyi.jpg")
        phong14 = Phong(tenphong='Phong 14', ghichu='Phòng có 1 máy lạnh , 1 giường , 1 TV', tinhtrang=False,
                        loaiphong_id=loaiphong1.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706902/tnfbho3bhagtndjbggyi.jpg")
        phong15 = Phong(tenphong='Phong 15', ghichu='Phòng có 1 máy lạnh , 1 giường , 1 TV', tinhtrang=False,
                        loaiphong_id=loaiphong1.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706902/tnfbho3bhagtndjbggyi.jpg")
        phong16 = Phong(tenphong='Phong 16', ghichu='Phòng có 1 máy lạnh , 1 giường , 1 TV', tinhtrang=False,
                        loaiphong_id=loaiphong1.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706902/tnfbho3bhagtndjbggyi.jpg")
        phong17 = Phong(tenphong='Phong 17', ghichu='Phòng có 1 máy lạnh , 1 giường , 1 TV', tinhtrang=False,
                        loaiphong_id=loaiphong1.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706902/tnfbho3bhagtndjbggyi.jpg")
        phong18 = Phong(tenphong='Phong 18', ghichu='Phòng có 1 máy lạnh , 1 giường , 1 TV', tinhtrang=False,
                        loaiphong_id=loaiphong1.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706902/tnfbho3bhagtndjbggyi.jpg")
        phong19 = Phong(tenphong='Phong 19', ghichu='Phòng có 1 máy lạnh , 1 giường , 1 TV', tinhtrang=False,
                        loaiphong_id=loaiphong1.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706902/tnfbho3bhagtndjbggyi.jpg")
        phong20 = Phong(tenphong='Phong 20', ghichu='Phòng có 1 máy lạnh , 1 giường , 1 TV', tinhtrang=False,
                        loaiphong_id=loaiphong1.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706902/tnfbho3bhagtndjbggyi.jpg")
        phong21 = Phong(tenphong='Phong 21', ghichu='2 phòng có 2 máy lạnh , 2 giường , 2 TV', tinhtrang=False,
                        loaiphong_id=loaiphong2.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704610281/khach-san-gan-day-9-min_kswi8g.png")
        phong22 = Phong(tenphong='Phong 22', ghichu='2 phòng có 2 máy lạnh , 2 giường , 2 TV', tinhtrang=False,
                        loaiphong_id=loaiphong2.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704610281/khach-san-gan-day-9-min_kswi8g.png")
        phong23 = Phong(tenphong='Phong 23', ghichu='2 phòng có 2 máy lạnh , 2 giường , 2 TV', tinhtrang=False,
                        loaiphong_id=loaiphong2.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704610281/khach-san-gan-day-9-min_kswi8g.png")
        phong24 = Phong(tenphong='Phong 24', ghichu='2 phòng có 2 máy lạnh , 2 giường , 2 TV', tinhtrang=False,
                        loaiphong_id=loaiphong2.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704610281/khach-san-gan-day-9-min_kswi8g.png")
        phong25 = Phong(tenphong='Phong 25', ghichu='2 phòng có 2 máy lạnh , 2 giường , 2 TV', tinhtrang=False,
                        loaiphong_id=loaiphong2.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704610281/khach-san-gan-day-9-min_kswi8g.png")
        phong26 = Phong(tenphong='Phong 26', ghichu='2 phòng có 2 máy lạnh , 2 giường , 2 TV', tinhtrang=False,
                        loaiphong_id=loaiphong2.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704610281/khach-san-gan-day-9-min_kswi8g.png")
        phong27 = Phong(tenphong='Phong 27', ghichu='2 phòng có 2 máy lạnh , 2 giường , 2 TV', tinhtrang=False,
                        loaiphong_id=loaiphong2.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704610281/khach-san-gan-day-9-min_kswi8g.png")
        phong28 = Phong(tenphong='Phong 28', ghichu='2 phòng có 2 máy lạnh , 2 giường , 2 TV', tinhtrang=False,
                        loaiphong_id=loaiphong2.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704610281/khach-san-gan-day-9-min_kswi8g.png")
        phong29 = Phong(tenphong='Phong 29', ghichu='2 phòng có 2 máy lạnh , 2 giường , 2 TV', tinhtrang=False,
                        loaiphong_id=loaiphong2.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704610281/khach-san-gan-day-9-min_kswi8g.png")
        phong30 = Phong(tenphong='Phong 30', ghichu='2 phòng có 2 máy lạnh , 2 giường , 2 TV', tinhtrang=False,
                        loaiphong_id=loaiphong2.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704610281/khach-san-gan-day-9-min_kswi8g.png")
        phong31 = Phong(tenphong='Phong 31', ghichu='3 phòng có 3 máy lạnh , 3 giường , 3 TV', tinhtrang=False,
                        loaiphong_id=loaiphong3.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706913/gbctc3plgysydtquxvzl.jpg")
        phong32 = Phong(tenphong='Phong 32', ghichu='3 phòng có 3 máy lạnh , 3 giường , 3 TV', tinhtrang=False,
                        loaiphong_id=loaiphong3.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706913/gbctc3plgysydtquxvzl.jpg")
        phong33 = Phong(tenphong='Phong 33', ghichu='3 phòng có 3 máy lạnh , 3 giường , 3 TV', tinhtrang=False,
                        loaiphong_id=loaiphong3.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706913/gbctc3plgysydtquxvzl.jpg")
        phong34 = Phong(tenphong='Phong 34', ghichu='3 phòng có 3 máy lạnh , 3 giường , 3 TV', tinhtrang=False,
                        loaiphong_id=loaiphong3.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706913/gbctc3plgysydtquxvzl.jpg")
        phong35 = Phong(tenphong='Phong 35', ghichu='3 phòng có 3 máy lạnh , 3 giường , 3 TV', tinhtrang=False,
                        loaiphong_id=loaiphong3.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706913/gbctc3plgysydtquxvzl.jpg")
        phong36 = Phong(tenphong='Phong 36', ghichu='3 phòng có 3 máy lạnh , 3 giường , 3 TV', tinhtrang=False,
                        loaiphong_id=loaiphong3.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706913/gbctc3plgysydtquxvzl.jpg")
        phong37 = Phong(tenphong='Phong 37', ghichu='3 phòng có 3 máy lạnh , 3 giường , 3 TV', tinhtrang=False,
                        loaiphong_id=loaiphong3.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706913/gbctc3plgysydtquxvzl.jpg")
        phong38 = Phong(tenphong='Phong 38', ghichu='3 phòng có 3 máy lạnh , 3 giường , 3 TV', tinhtrang=False,
                        loaiphong_id=loaiphong3.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706913/gbctc3plgysydtquxvzl.jpg")
        phong39 = Phong(tenphong='Phong 39', ghichu='3 phòng có 3 máy lạnh , 3 giường , 3 TV', tinhtrang=False,
                        loaiphong_id=loaiphong3.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706913/gbctc3plgysydtquxvzl.jpg")
        phong40 = Phong(tenphong='Phong 40', ghichu='3 phòng có 3 máy lạnh , 3 giường , 3 TV', tinhtrang=False,
                        loaiphong_id=loaiphong3.id,
                        hinhanh="https://res.cloudinary.com/ds7ikpaeh/image/upload/v1704706913/gbctc3plgysydtquxvzl.jpg")

        admin = NguoiQuanTri(name='admin'
                             , username='admin'
                             , password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
                             , cccd="322323232", sdt='323232323',
                             ngaysinh=datetime.strptime('2023-12-07 00:00:00', "%Y-%m-%d %H:%M:%S")
                             , diachi='ABCXYZ', user_role=UserRoleEnum.ADMIN)

        db.session.add_all([phong1, phong2, phong3, phong4, phong5, phong6, phong7, phong8, phong9, phong10,
                            phong11, phong12, phong13, phong14, phong15, phong16, phong17, phong18, phong19, phong20,
                            phong21, phong22, phong23, phong24, phong25, phong26, phong27, phong28, phong29, phong30,
                            phong31, phong32, phong33, phong34, phong35, phong36, phong37, phong38, phong39, phong40,
                            admin])
        db.session.commit()

        quydinh1 = ThongSoQuyDinh(key='songuoi1phong', value='3')
        quydinh2 = ThongSoQuyDinh(key='heso', value='1.5')
        db.session.add_all([quydinh1, quydinh2])
        db.session.commit()
