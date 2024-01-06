from sqlalchemy.orm import relationship
from app import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime, Boolean, SmallInteger
import enum
from datetime import datetime
from flask_login import UserMixin


class UserRoleEnum(enum.Enum):
    KHACH_HANG = 1
    ADMIN = 2
    THU_NGAN = 3


class LoaiKhachHang(db.Model):
    __tablename__ = 'loaikhachhang'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenloaikhachhang = Column(String(50), nullable=False)


class KhachHang(db.Model):
    __tablename__ = 'khachhang'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenkhachhang = Column(String(100), nullable=False)
    cccd = Column(String(12), nullable=False, unique=True)
    sdt = Column(String(12), nullable=False, unique=True)
    diachi = Column(String(255), nullable=True)
    ngaysinh = Column(DateTime, nullable=True)
    loaikhachhang_id = db.Column(Integer, ForeignKey(LoaiKhachHang.id), unique=True, nullable=False)
    loaikhachhang = db.relationship('LoaiKhachHang', backref='loaikhachhangBackrefkhachhang')
    phieudanhgia = db.relationship('PhieuDanhGia', backref='phieudanhgiaBackrefkhachhang')
    phieuthuephong = db.relationship('PhieuThuePhong',
                                     backref=' phieuthuephongBackrefKhachHang')


class NguoiQuanTri(db.Model):
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
    tenloaiphong = Column(String(255), nullable=False)
    loaiphong_donvitinhtien = db.relationship('LoaiPhong_DonVitinhTien',
                                              backref=' loaiphong_donvitinhtienBackrefLoaiPhong')
    phieudanhgia = db.relationship('PhieuDanhGia',
                                   backref=' phieudanhgiaBackrefLoaiPhong')


class Phong(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ghichu = Column(String(255), nullable=False)
    tinhtrang = Column(Boolean, nullable=False, default=0)
    hinhanh = Column(String(255), nullable=False)
    loaiphong_id = db.Column(Integer, ForeignKey(LoaiPhong.id), nullable=False)
    phieuthuephong = db.relationship('PhieuThuePhong',
                                     backref=' phieuthuephongBackrefPhong')


class PhieuThuePhong(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngaybatdau = Column(DateTime, nullable=False)
    ngayketthuc = Column(DateTime, nullable=False)
    loaiphong_id = db.Column(Integer, ForeignKey(LoaiPhong.id), nullable=False)
    khachhang_id = db.Column(Integer, ForeignKey(KhachHang.id), nullable=False)


class DonViTinhTien(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(255), nullable=False)
    loaiphong_donvitinhtien = db.relationship('LoaiPhong_DonVitinhTien',
                                              backref=' loaiphong_donvitinhtienBackrefDonViTinhTien')


class LoaiPhong_DonVitinhTien(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    loaiphong_id = db.Column(Integer, ForeignKey(LoaiPhong.id), nullable=False)
    donvitinhtien_id = db.Column(Integer, ForeignKey(DonViTinhTien.id), nullable=False)
    giatien = db.Column(Float, nullable=False)


class PhieuDanhGia(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngaydanhgia = Column(DateTime, nullable=False)
    soSao = Column(Integer, nullable=False)
    khachhang_id = db.Column(Integer, ForeignKey(KhachHang.id), nullable=False)
    loaiphong_id = db.Column(Integer, ForeignKey(LoaiPhong.id), nullable=False)


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
                                     backref=' phieuthuekhamBackrefhoadon')


if __name__ == "__main__":
    from app import app

    with app.app_context():
        db.create_all()
        db.session.commit()
