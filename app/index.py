from flask import Flask, render_template, request, redirect, url_for
from app import app, login, db, dao
from twilio.rest import Client
import json, hmac, hashlib, requests
import uuid
from app.models import (KhachHang, LoaiKhachHang, Phong, LoaiPhong, PhieuThuePhong, LoaiPhong_DonVitinhTien,
                        DonViTinhTien, UserRoleEnum, NguoiQuanTri, PhieuDanhGia, ThongSoQuyDinh, NhuCau,
                        DsPhieuDatPhong, PhieuDatPhong, DsPhongDaDat)
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import cloudinary
import cloudinary.uploader
from admin import *

import cloudinary

cloudinary.config(
    cloud_name="ds7ikpaeh",
    api_key="752858474657471",
    api_secret="s2bK7XOjXnjhKrsI8Grwl2dv4gI"
)


@login.user_loader
def load_nguoiquantri(id):
    return dao.get_manager_by_id(id)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dat-phong", methods=['POST'])
def booking_room():
    name = request.form.get('name_customer')
    phone = request.form.get('phone')
    cccd = request.form.get('cccd')
    country = request.form.get('country')
    gender = request.form.get('gender')
    room_type = request.form.get('room_type')
    address = request.form.get('address')
    unit = request.form.get('unit')
    start = request.form.get('start_booking')
    end = request.form.get('end_booking')
    favor = request.form.get('favor')

    loaikhachhang = dao.get_LoaiKhachHang_by_tenLoaiKhachHang(country)
    if not loaikhachhang:
        loaikhachhang = LoaiKhachHang(tenloaikhachhang=country)
        db.session.add(loaikhachhang)
        db.session.commit()

    customer_order = KhachHang(tenkhachhang=name, sdt=phone, gioitinh=gender, cccd=cccd, diachi=address,
                               loaikhachhang_id=loaikhachhang.id)
    db.session.add(customer_order)
    db.session.commit()

    customers_name = request.form.getlist('customer_name')
    customers_country = request.form.getlist('customer_country')
    customers_cccd = request.form.getlist('customer_cccd')
    customers_address = request.form.getlist('customer_address')

    customers_id_arr = []

    for i in range(len(customers_name)):
        if customers_name[i] != '':
            loaikhachhang = dao.get_LoaiKhachHang_by_tenLoaiKhachHang(customers_country[i])
            if not loaikhachhang:
                loaikhachhang = LoaiKhachHang(tenloaikhachhang=country)
                db.session.add(loaikhachhang)
                db.session.commit()
            khachhang = KhachHang()
            khachhang.loaikhachhang_id = loaikhachhang.id
            khachhang.tenkhachhang = customers_name[i]
            if customers_cccd[i]:
                khachhang.cccd = customers_cccd[i]
            if customers_address[i]:
                khachhang.diachi = customers_address[i]
            db.session.add(khachhang)
            db.session.commit()
            customers_id_arr.append(khachhang.id)
    print(customers_id_arr)
    loaiphong = dao.get_loaiphong_by_tenloaiphong(room_type)
    phong_available = dao.get_phong_available_by_loaiphong_id(loaiphong.id)

    if not phong_available:
        return render_template("index.html"
                               , flag='out_of_room')

    lp_arr = []
    dv_arr = []
    price_arr = []
    for j in range(len(phong_available)):
        loaiphong_donvitinhtien = dao.get_phong_donvitinhtien_by_loaiphong_id(phong_available[j].loaiphong_id)
        length = len(loaiphong_donvitinhtien)
        for i in range(len(loaiphong_donvitinhtien)):
            lp = dao.get_loaiphong_by_id(loaiphong_donvitinhtien[i].loaiphong_id)
            dv = dao.get_donvitinhtien_by_id(loaiphong_donvitinhtien[i].donvitinhtien_id)
            lp_arr.append(lp.tenloaiphong)
            dv_arr.append(dv.ten)
            price_arr.append(loaiphong_donvitinhtien[i].giatien)

    return render_template("available_room.html", phong_available=phong_available,
                           loaiphong_donvitinhtien=loaiphong_donvitinhtien, customer_order=customer_order
                           , flag='success', lp_arr=lp_arr, dv_arr=dv_arr, length=length, price_arr=price_arr,
                            start=start, end=end, customers_id_arr=customers_id_arr)


@app.route("/dat-phong/lap-phieu-dat-phong", methods=['POST'])
def lapphieudatphong():
    start = request.form.get('start')
    end = request.form.get('end')
    customer_order = dao.get_KhachHang_by_id(request.form.get('customer_order_id'))
    dvtt = dao.get_donvitinhtien_by_ten(request.form.get('dvtt'))
    lp = dao.get_loaiphong_by_tenloaiphong(request.form.get('lp'))
    available_room = dao.get_phong_by_id(request.form.get('available_room_id'))
    customers_id_arr = eval(request.form.get('customers_id_arr'))
    lp_arr = eval(request.form.get('lp_arr'))
    dv_arr = eval(request.form.get('dv_arr'))
    price_arr = eval(request.form.get('price_arr'))


    phieudatphong = PhieuDatPhong(ngaybatdau=start, ngayketthuc=end, khachhang_id=customer_order.id)
    db.session.add(phieudatphong)
    db.session.commit()

    for i in range(len(customers_id_arr)):
        dsphieudatphong = DsPhieuDatPhong(khachhang_id=customers_id_arr[i], phieudatphong_id=phieudatphong.id)
        db.session.add(dsphieudatphong)
        db.session.commit()

    loaiphong_donvitinhtien = dao.get_loaiphong_donvitinhtien_by_2id(lp.id, dvtt.id)
    dsphongdadat = DsPhongDaDat(phong_id=available_room.id, loaiphong_donvitinhtien_id=loaiphong_donvitinhtien.id,
                                phieudatphong_id=phieudatphong.id)
    available_room.tinhtrang = True
    db.session.add_all([available_room, dsphongdadat])
    db.session.commit()

    phong_available = dao.get_phong_available_by_loaiphong_id(lp.id)

    return render_template("available_room.html", phong_available=phong_available,
                    loaiphong_donvitinhtien=loaiphong_donvitinhtien, customer_order=customer_order
                    , flag='success', lp_arr=lp_arr, dv_arr=dv_arr, length=3, price_arr=price_arr,
                     start=start, end=end, customers_id_arr=customers_id_arr)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
