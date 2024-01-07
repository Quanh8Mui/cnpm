from flask_login import logout_user, current_user
from flask_admin import BaseView, expose, Admin
from flask import redirect, flash, url_for, render_template, request
from app import app, db, dao
from app.models import (KhachHang, LoaiKhachHang, Phong, LoaiPhong, PhieuThuePhong, LoaiPhong_DonVitinhTien,
                        DonViTinhTien, UserRoleEnum, NguoiQuanTri, PhieuDanhGia, ThongSoQuyDinh, NhuCau,
                        DsPhieuDatPhong, PhieuDatPhong, DsPhongDaDat)
from flask_admin.contrib.sqla import ModelView
from datetime import datetime

admin = Admin(app=app, name='QUẢN TRỊ DANH SÁCH KHÁCH SẠN', template_mode='bootstrap4')


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedAdminNguoiQuanTri(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN

    def create_model(self, form):
        import hashlib
        model = self.model()
        form.populate_obj(model)
        nguoiquantri = NguoiQuanTri(name=model.name
                                    , username=model.username
                                    , password=str(hashlib.md5(model.password.encode('utf-8')).hexdigest())
                                    , cccd=model.cccd, sdt=model.sdt,
                                    ngaysinh=model.ngaysinh
                                    , diachi=model.diachi, user_role=model.user_role)

        self.session.add(nguoiquantri)
        self._on_model_change(form, nguoiquantri, True)
        self.session.commit()
        return True


class NguoiQuanTriView(AuthenticatedAdminNguoiQuanTri):
    can_create = True
    can_edit = True


class AuthenticatedNhanVienPhieuDatPhong(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.NHAN_VIEN

    column_list = [ 'khachhang.tenkhachhang', 'ngaybatdau', 'ngayketthuc', 'khachhang.cccd',
                   'dscacphongdadat.phong_id']

    def phongid_formatter(self, context, model, name):
        rooms = []
        dspdd = dao.get_dspdd_by_phieu_dat_phong_id(model.id)

        for d in dspdd:
            phong = dao.get_phong_by_id(d.phong_id)
            rooms.append(phong.tenphong)

        return rooms

    column_formatters = {
        'dscacphongdadat.phong_id': phongid_formatter,
    }


class PhieuDatPhongView(AuthenticatedNhanVienPhieuDatPhong):
    can_create = False
    can_edit = False
    can_delete = False


class MyLogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(NguoiQuanTriView(NguoiQuanTri, db.session, name="Quản lí nhân sự"))
admin.add_view(PhieuDatPhongView(PhieuDatPhong, db.session, name="Tra cứu lịch đặt phòng"))
admin.add_view(MyLogoutView(name='Đăng xuất'))
