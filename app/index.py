from flask import Flask, render_template, request, redirect, url_for
from app import app, login, db, dao
from twilio.rest import Client
import json, hmac, hashlib, requests
import uuid
from app.models import (KhachHang, LoaiKhachHang, Phong, LoaiPhong, PhieuThuePhong, LoaiPhong_DonVitinhTien,
                        DonViTinhTien, UserRoleEnum, NguoiQuanTri, PhieuDanhGia, ThongSoQuyDinh, NhuCau,
                        DsPhieuDatPhong, PhieuDatPhong, DsPhongDaDat, DsPhieuThuePhong, DsPhongDaThue)
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import cloudinary
import cloudinary.uploader
from admin import *

import cloudinary
today = datetime.now().strftime('%Y-%m-%d')


cloudinary.config(
    cloud_name="ds7ikpaeh",
    api_key="752858474657471",
    api_secret="s2bK7XOjXnjhKrsI8Grwl2dv4gI"
)


@login.user_loader
def load_nguoiquantri(id):
    return dao.get_NguoiQuanTri_by_id(id)


@app.route("/")
def home():
    rooms = []
    room1 = dao.get_phong_by_id(1)
    room2 = dao.get_phong_by_id(21)
    room3 = dao.get_phong_by_id(31)
    rooms.append(room1)
    rooms.append(room2)
    rooms.append(room3)
    return render_template("index.html", rooms=rooms)


@app.route('/admin/login', methods=['POST'])
def login_admin_process():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_nguoiquantri(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route("/dat-phong", methods=['POST'])
def booking_room():
    name = request.form.get('name_customer')
    phone = request.form.get('phone')
    cccd = request.form.get('cccd')
    country = request.form.get('country')
    gender = request.form.get('gender')
    room_type = request.form.get('room_type')
    address = request.form.get('address')
    start = request.form.get('start_booking')
    end = request.form.get('end_booking')
    favor = request.form.get('favor')

    loaikhachhang = dao.get_LoaiKhachHang_by_tenLoaiKhachHang(country)

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
                           start=start, end=end, customers_id_arr=customers_id_arr, favor=favor
                           )


@app.route("/dat-phong/lap-phieu-dat-phong/", methods=['POST'])
def lapphieudatphong():
    start = request.form.get('start')
    end = request.form.get('end')
    favor = request.form.get('favor')
    customer_order = dao.get_KhachHang_by_id(request.form.get('customer_order_id'))
    dvtt = dao.get_donvitinhtien_by_ten(request.form.get('dvtt'))
    lp = dao.get_loaiphong_by_tenloaiphong(request.form.get('lp'))
    available_room = dao.get_phong_by_id(request.form.get('available_room_id'))
    customers_id_arr = eval(request.form.get('customers_id_arr'))
    lp_arr = eval(request.form.get('lp_arr'))
    dv_arr = eval(request.form.get('dv_arr'))
    price_arr = eval(request.form.get('price_arr'))
    phieudatphong_id = request.form.get('phieudatphong_id')

    if not phieudatphong_id:
        phieudatphong = PhieuDatPhong(ngaybatdau=start, ngayketthuc=end, khachhang_id=customer_order.id)
        db.session.add(phieudatphong)
        db.session.commit()
    else:
        phieudatphong = dao.get_phieudatphong_by_id(phieudatphong_id)

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
    if favor:
        favor_dao = dao.get_nhucau_by_phieudatphong_id(phieudatphong.id)
        if not favor_dao:
            favor_dao = NhuCau(nhucau=favor, phieudatphong_id=phieudatphong.id)
            db.session.add(favor_dao)
            db.session.commit()

    customers_id_arr = []

    return render_template("available_room.html", phong_available=phong_available,
                           loaiphong_donvitinhtien=loaiphong_donvitinhtien, customer_order=customer_order
                           , flag='success', lp_arr=lp_arr, dv_arr=dv_arr, length=3, price_arr=price_arr,
                           start=start, end=end, customers_id_arr=customers_id_arr, phieudatphong=phieudatphong)


@app.route("/admin/lapphieuthuephong", methods=['GET'])
@login_required
def formlapphieuthuephong():
    return render_template("admin/lapphieuthuephong.html")


@app.route("/admin/lapphieuthuephong", methods=['POST'])
@login_required
def lapphieuthuephong():
    start = request.form.get('start_booking')
    end = request.form.get('end_booking')
    dvtt = request.form.get('dvtt')
    rooms_ordered = request.form.getlist('rooms_ordered')
    customers_name = request.form.getlist('customer_name')
    customers_type = request.form.getlist('customer_type')
    customers_cccd = request.form.getlist('customer_cccd')
    customers_address = request.form.getlist('customer_address')
    phieudatphong_id = request.form.get('phieudatphong_id')
    unit = dao.get_unit_by_unit_name(dvtt)

    if phieudatphong_id:
        phieudatphong_id = int(phieudatphong_id)
        phieudatphong = dao.get_phieudatphong_by_id(phieudatphong_id)
        phieuthuephong = PhieuThuePhong(ngaybatdau=start, ngayketthuc=end, khachhang_id=phieudatphong.khachhang_id)
        db.session.add(phieuthuephong)
        db.session.commit()

        for i in range(len(rooms_ordered)):
            room = dao.get_phong_by_tenphong(rooms_ordered[i])
            loaiphong_donvitinhtien = dao.get_phong_donvitinhtien_by_2id(room.loaiphong_id, unit.id)

            dsphongdathue = DsPhongDaThue(phong_id=room.id, loaiphong_donvitinhtien_id=loaiphong_donvitinhtien.id,
                                          phieuthuephong_id=phieuthuephong.id)
            db.session.add(dsphongdathue)
            db.session.commit()

        for i in range(1, len(customers_name)):
            if customers_name[i] != '':
                khachhang = dao.get_KhachHang_by_tenkhachhang(customers_name[i])
                loaikhachhang = dao.get_LoaiKhachHang_by_tenLoaiKhachHang(customers_type[i])
                if khachhang:
                    dsphieuthuephong = DsPhieuThuePhong(phieuthuephong_id=phieuthuephong.id, khachhang_id=khachhang.id)
                    db.session.add(dsphieuthuephong)
                    db.session.commit()
                    if customers_cccd[i]:
                        khachhang.cccd = customers_cccd[i]
                    if customers_address[i]:
                        khachhang.diachi = customers_address[i]
                    khachhang.loaikhachhang_id = loaikhachhang.id
                    db.session.add(khachhang)
                    db.session.commit()
    else:
        phieuthuephong = None
        for i in range(len(customers_name)):
            if i == 0 and customers_name[i]:
                if customers_cccd[i]:
                    khachhang = dao.get_KhachHang_by_cccd(customers_cccd[i])
                    if not khachhang:
                        loaikhachhang = dao.get_LoaiKhachHang_by_tenLoaiKhachHang(customers_type[i])
                        khachhang = KhachHang(tenkhachhang=customers_name[i], cccd=customers_cccd[i],
                                              loaikhachhang_id=loaikhachhang.id)
                        db.session.add(khachhang)
                        db.session.commit()
                    phieuthuephong = PhieuThuePhong(ngaybatdau=start, ngayketthuc=end,
                                                    khachhang_id=khachhang.id)
                    db.session.add(phieuthuephong)
                    db.session.commit()
            elif i != 0 and customers_name[i]:
                khachhang = None
                if customers_cccd[i]:
                    khachhang = dao.get_KhachHang_by_cccd(customers_cccd[i])
                if not khachhang:
                    loaikhachhang = dao.get_LoaiKhachHang_by_tenLoaiKhachHang(customers_type[i])
                    khachhang = KhachHang(tenkhachhang=customers_name[i], loaikhachhang_id=loaikhachhang.id)
                    db.session.add(khachhang)
                    db.session.commit()
                dsphieuthuephong = DsPhieuThuePhong(phieuthuephong_id=phieuthuephong.id, khachhang_id=khachhang.id)
                db.session.add(dsphieuthuephong)
                db.session.commit()

        for i in range(len(rooms_ordered)):
            room = dao.get_phong_by_tenphong(rooms_ordered[i])
            loaiphong_donvitinhtien = dao.get_phong_donvitinhtien_by_2id(room.loaiphong_id, unit.id)

            dsphongdathue = DsPhongDaThue(phong_id=room.id,
                                          loaiphong_donvitinhtien_id=loaiphong_donvitinhtien.id,
                                          phieuthuephong_id=phieuthuephong.id)
            db.session.add(dsphongdathue)
            db.session.commit()


    phong_available = dao.get_phong_available_by_tinhtrang()
    phong_unavailable = dao.get_phong_unavailable_by_tinhtrang()
    length1 = len(phong_available)
    length2 = len(phong_unavailable)
    flag = 'success'
    return render_template('admin/lapphieuthuephong.html', phong_available=phong_available, length1=length1,
                           length2=length2, phong_unavailable=phong_unavailable, flag=flag)


@app.route('/logout_manager')
@login_required
def logout_manager():
    logout_user()
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
