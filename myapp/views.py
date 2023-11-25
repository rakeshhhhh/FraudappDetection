from django.shortcuts import render
from .models import user_login,category_master,company_details,data_set,product_master,product_pic,product_review,sub_category_master,user_details
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from django.db.models import Max
from .app_classification import AppClassification
from project.settings import BASE_DIR
# Create your views here.
def index(request):
    return render(request,'./myapp/index.html')

def about(request):
    return render(request,'./myapp/about.html')

def home(request):
    return render(request,'./myapp/home.html')

def contactus(request):
    return render(request,'./myapp/contactus.html')

def admin_login(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        passwd = request.POST.get('passwd')

        ul = user_login.objects.filter(uname=uname, password=passwd,utype='admin')

        if len(ul) == 1:
            request.session['user_id'] = ul[0].uname
            context = {'uname': request.session['user_id']}
            return render(request, 'myapp/admin_home.html',
                          context)
        else:
            context = {'msg': 'Invalid username or password'}
            return render(request, 'myapp/admin_login.html',context)
    else:
        return render(request, 'myapp/admin_login.html')

def admin_home(request):

    context = {'uname':request.session['user_id']}
    return render(request,'./myapp/admin_home.html',context)

def admin_settings(request):

    context = {'uname':request.session['user_id']}
    return render(request,'./myapp/admin_settings.html',context)

def admin_settings_404(request):

    context = {'uname':request.session['user_id']}
    return render(request,'./myapp/admin_settings_404.html',context)

def admin_changepassword(request):
    if request.method == 'POST':
        uname = request.session['user_id']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print("username:::" + uname)
        print("current_password" + str(current_password))

        try:

            ul = user_login.objects.get(uname=uname, password=current_password)

            if ul is not None:
                ul.password = new_password  # change field
                ul.save()
                context={'msg':'Password Changed'}
                return render(request, './myapp/admin_changepassword.html',context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/admin_changepassword.html',context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Not Changed'}
            return render(request, './myapp/admin_changepassword.html',context)
    else:
        return render(request, './myapp/admin_changepassword.html')

def admin_category_master_add(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        cm = category_master(category_name=category_name)
        cm.save()
        return render(request, 'myapp/admin_category_master_add.html')

    else:
        return render(request, 'myapp/admin_category_master_add.html')

def admin_category_master_delete(request):
    id = request.GET.get('id')
    print("id="+id)

    nm = category_master.objects.get(id=int(id))
    nm.delete()

    nm_l = category_master.objects.all()
    context ={'category_list':nm_l}
    return render(request,'myapp/admin_category_master_view.html',context)

def admin_category_master_view(request):
    nm_l = category_master.objects.all()
    context ={'category_list':nm_l}
    return render(request,'myapp/admin_category_master_view.html',context)

def admin_subcategory_master_add(request):
    if request.method == 'POST':
        category_master_id = int(request.POST.get('category_master_id'))
        sub_category_name = request.POST.get('sub_category_name')

        sm = sub_category_master(sub_category_name=sub_category_name,category_master_id=category_master_id)
        sm.save()
        cm_l = category_master.objects.all()
        context = {'category_list': cm_l}
        return render(request, 'myapp/admin_subcategory_master_add.html',context)

    else:
        cm_l = category_master.objects.all()
        context = {'category_list': cm_l}
        return render(request, 'myapp/admin_subcategory_master_add.html',context)

def admin_subcategory_master_delete(request):
    id = request.GET.get('id')
    print("id="+id)

    nm = sub_category_master.objects.get(id=int(id))
    nm.delete()

    cm_l = category_master.objects.all()
    cmd = {}
    for cm in cm_l:
        cmd[cm.id] = cm.category_name

    st_l = sub_category_master.objects.all()
    context ={'subcategory_list':st_l,'category_list':cmd}
    return render(request,'myapp/admin_subcategory_master_view.html',context)

def admin_subcategory_master_view(request):
    cm_l = category_master.objects.all()
    cmd = {}
    for cm in cm_l:
        cmd[cm.id] = cm.category_name

    st_l = sub_category_master.objects.all()
    context = {'subcategory_list': st_l, 'category_list': cmd}
    return render(request, 'myapp/admin_subcategory_master_view.html', context)

def admin_data_set_add(request):
    if request.method == 'POST':
        sentiment_type = request.POST.get('sentiment_type')
        data_path = request.POST.get('data_path')
        ds = data_set(sentiment_type=sentiment_type,data_path=data_path)
        ds.save()

        ##########training model############
        data_file_path = os.path.join(BASE_DIR, 'data/data_set.csv')
        # os.remove(data_file_path)

        obj_list = data_set.objects.all()
        f = open(data_file_path, "w")
        f.write('text,label')
        f.write("\n")
        for obj in obj_list:

            f.write(f'{obj.data_path},{obj.sentiment_type}')
            f.write("\n")
        f.close()
        data_file_path = os.path.join(BASE_DIR, 'data/data_set.csv')
        data_file_label_path = os.path.join(BASE_DIR, 'data/data_set_label.dat')
        tfid_file_path = os.path.join(BASE_DIR, 'data/data_set_tfid.dat')
        model_file_path = os.path.join(BASE_DIR, 'data/data_set_svm.model')

        obj = AppClassification()
        txt_result = obj.text_processing(data_file_path, data_file_label_path)
        obj.train_model(txt_result, tfid_file_path, model_file_path, 'svm')
        ################

        context = {'msg':'Record added'}
        return render(request, 'myapp/admin_data_set_add.html',context)

    else:
        context = {'msg': ''}
        return render(request, 'myapp/admin_data_set_add.html',context)

def admin_data_set_delete(request):
    id = request.GET.get('id')
    print("id="+id)

    ds = data_set.objects.get(id=int(id))
    ds.delete()

    ds_l = data_set.objects.all()
    context ={'data_list':ds_l,'msg':'Record deleted'}
    return render(request,'myapp/admin_data_set_view.html',context)

def admin_data_set_view(request):
    ds_l = data_set.objects.all()
    context = {'data_list': ds_l, 'msg': ''}
    return render(request, 'myapp/admin_data_set_view.html', context)

def admin_company_details_view(request):
    cd_l = company_details.objects.all()
    context = {'company_list': cd_l, 'msg': ''}
    return render(request, 'myapp/admin_company_details_view.html', context)


def admin_company_product_master_view(request):
    c_email =  request.GET.get('c_email')#request.session['user_name']
    cd = company_details.objects.get(c_email=c_email)
    company_details_id = cd.id

    pm_l = product_master.objects.filter(company_details_id=company_details_id)

    scm_l = sub_category_master.objects.all()
    scmd = {}
    for scm in scm_l:
        scmd[scm.id] = scm.sub_category_name

    context = {'product_list': pm_l, 'subcategory_list': scmd, 'msg': ''}
    return render(request, 'myapp/admin_company_product_master_view.html', context)

def admin_company_product_pic_view(request):
    product_master_id = request.GET.get('product_master_id')
    pp_l = product_pic.objects.filter(product_master_id=product_master_id)
    context = {'pic_list': pp_l, 'product_master_id': product_master_id, 'msg': ''}
    return render(request, 'myapp/admin_company_product_pic_view.html', context)

########Company#############
def company_login_check(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        passwd = request.POST.get('passwd')

        ul = user_login.objects.filter(uname=uname, password=passwd,utype='company')
        print(len(ul))
        if len(ul) == 1:
            request.session['user_id'] = ul[0].uname
            request.session['user_name'] = ul[0].uname
            context = {'uname': request.session['user_name']}
            return render(request, 'myapp/company_home.html',context)
        else:
            context={'msg':'Invalid username or password'}
            return render(request, 'myapp/company_login.html',context)
    else:
        context = {'msg': ''}
        return render(request, 'myapp/company_login.html',context)

def company_home(request):

    context = {'uname':request.session['user_name']}
    return render(request,'./myapp/company_home.html',context)

def company_details_add(request):
    if request.method == 'POST':

        c_name =  request.POST.get('c_name')
        c_descp =  request.POST.get('c_descp')
        c_addr1 =  request.POST.get('c_addr1')
        c_addr2 =  request.POST.get('c_addr2')
        c_addr3 = request.POST.get('c_addr3')
        c_pincode =  request.POST.get('c_pincode')
        c_email =  request.POST.get('c_email')
        c_contact1 = request.POST.get('c_contact1')
        c_url =  request.POST.get('c_url')
        c_dt = datetime.today().strftime('%Y-%m-%d')
        c_tm = datetime.today().strftime('%H:%M:%S')
        c_status = 'active'
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        pic_path = fs.save(uploaded_file.name, uploaded_file)

        c_logo = pic_path

        password = request.POST.get('password')
        uname=c_email

        ul = user_login(uname=uname, password=password, utype='company')
        ul.save()

        cm = company_details(c_name=c_name,c_descp=c_descp, c_addr1=c_addr1, c_addr2=c_addr2, c_addr3=c_addr3, c_pincode=c_pincode, c_contact1=c_contact1,
                             c_logo=c_logo,c_tm=c_tm,c_dt=c_dt,c_url=c_url,c_status=c_status,c_email=c_email )
        cm.save()

        context={'msg':'Record added'}
        return render(request, 'myapp/company_login.html',context)

    else:
        return render(request, 'myapp/company_details_add.html')

def company_changepassword(request):
    if request.method == 'POST':
        uname = request.session['user_name']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print("username:::" + uname)
        print("current_password" + str(current_password))

        try:

            ul = user_login.objects.get(uname=uname, password=current_password)

            if ul is not None:
                ul.password = new_password  # change field
                ul.save()
                context = {'msg':'Password changed'}
                return render(request, './myapp/company_changepassword.html',context)
            else:
                context = {'msg': 'Password change error'}
                return render(request, './myapp/company_changepassword.html',context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password change error'}
            return render(request, './myapp/company_changepassword.html',context)
    else:
        return render(request, './myapp/company_changepassword.html')

def company_settings(request):

    context = {'uname':request.session['user_name']}
    return render(request,'./myapp/company_settings.html',context)

def company_product_master_add(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        c_email=request.session['user_name']
        cd = company_details.objects.get(c_email=c_email)
        company_details_id = cd.id
        sub_category_master_id = int(request.POST.get('sub_category_master_id'))
        product_descp = request.POST.get('product_descp')
        product_price = float(request.POST.get('product_price'))
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        pic_path = fs.save(uploaded_file.name, uploaded_file)
        status = pic_path


        pm = product_master(product_name=product_name,company_details_id=company_details_id,sub_category_master_id=sub_category_master_id,
                            product_descp=product_descp,product_price=product_price,dt=dt,tm=tm,status=status)
        pm.save()

        scm_l = sub_category_master.objects.all()
        context = {'subcategory_list':scm_l,'msg':'Record added'}
        return render(request, 'myapp/company_product_master_add.html',context)

    else:
        scm_l = sub_category_master.objects.all()
        context = {'subcategory_list':scm_l,'msg':''}
        return render(request, 'myapp/company_product_master_add.html',context)

def company_product_master_delete(request):
    id = request.GET.get('id')
    print("id="+id)

    pm = product_master.objects.get(id=int(id))
    pm.delete()

    c_email = request.session['user_name']
    cd = company_details.objects.get(c_email=c_email)
    company_details_id = cd.id

    pm_l = product_master.objects.filter(company_details_id=company_details_id)

    scm_l = sub_category_master.objects.all()
    scmd = {}
    for scm in scm_l:
        scmd[scm.id] = scm.sub_category_name

    context ={'product_list':pm_l,'subcategory_list': scmd,'msg':'Record deleted'}
    return render(request,'myapp/company_product_master_view.html',context)

def company_product_master_view(request):
    c_email = request.session['user_name']
    cd = company_details.objects.get(c_email=c_email)
    company_details_id = cd.id

    pm_l = product_master.objects.filter(company_details_id=company_details_id)

    scm_l = sub_category_master.objects.all()
    scmd = {}
    for scm in scm_l:
        scmd[scm.id] = scm.sub_category_name

    context = {'product_list': pm_l, 'subcategory_list': scmd, 'msg': ''}
    return render(request, 'myapp/company_product_master_view.html', context)

def company_product_pic_add(request):
    if request.method == 'POST':
        product_master_id = request.POST.get('product_master_id')
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        pic_path = fs.save(uploaded_file.name, uploaded_file)

        pp = product_pic(product_master_id=int(product_master_id),pic_path=pic_path)
        pp.save()

        context = {'msg':'Picture added','product_master_id':product_master_id}
        return render(request, 'myapp/company_product_pic_add.html',context)

    else:
        product_master_id = request.GET.get('product_master_id')
        context = {'msg':'','product_master_id':product_master_id}
        return render(request, 'myapp/company_product_pic_add.html',context)

def company_product_pic_delete(request):
    id = request.GET.get('id')
    product_master_id = request.GET.get('product_master_id')
    print("id="+id)
    pp = product_pic.objects.get(id=int(id))
    pp.delete()

    pp_l = product_pic.objects.filter(product_master_id=int(product_master_id))
    context ={'pic_list':pp_l,'product_master_id': product_master_id,'msg':'Picture deleted'}
    return render(request,'myapp/company_product_pic_view.html',context)

def company_product_pic_view(request):
    product_master_id = request.GET.get('product_master_id')
    pp_l = product_pic.objects.filter(product_master_id=product_master_id)
    context = {'pic_list': pp_l, 'product_master_id': product_master_id, 'msg': ''}
    return render(request, 'myapp/company_product_pic_view.html', context)
import os
def company_product_review_view(request):
    product_master_id = request.GET.get('product_master_id')
    pr_l = product_review.objects.filter(product_master_id=product_master_id)
    cmd={}
    umd = {}

    for pr in pr_l:
        ########################
        obj = AppClassification()
        result = obj.input_text_processing(pr.review)
        data_file_path = os.path.join(BASE_DIR, 'data/data_set.csv')
        data_file_label_path = os.path.join(BASE_DIR, 'data/data_set_label.dat')
        tfid_file_path = os.path.join(BASE_DIR, 'data/data_set_tfid.dat')
        model_file_path = os.path.join(BASE_DIR, 'data/data_set_svm.model')

        model = obj.load_data(model_file_path)
        Tfidf_vect = obj.load_data(tfid_file_path)
        p = obj.get_prediction(model, result, Tfidf_vect)
        label = obj.load_data(data_file_label_path)
        label = sorted(label)
        print(f'result = {label[p[0]]}')
        final_label = label[p[0]]
        ########################
        cmd[pr.id] = final_label
        uobj = user_login.objects.get(id=pr.user_id)
        udobj = user_details.objects.get(email=uobj.uname)
        umd[pr.user_id] = f'{udobj.f_name} {udobj.l_name}'

    context = {'review_list': pr_l,'user_list': umd,'sentiment_list': cmd, 'product_master_id': product_master_id, 'msg': ''}
    return render(request, 'myapp/company_product_review_view.html', context)

########USER#############
def user_login_check(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        passwd = request.POST.get('passwd')

        ul = user_login.objects.filter(uname=uname, password=passwd,utype='user')
        print(len(ul))
        if len(ul) == 1:
            request.session['user_id'] = ul[0].id
            request.session['user_name'] = ul[0].uname
            user_id = request.session['user_id']
            ud=user_details.objects.get(user_id=int(user_id))
            context = {'fname': ud.f_name, 'lname': ud.l_name}
            #context = {'uname': request.session['user_name']}
            return render(request, 'myapp/user_home.html',context)
        else:
            context = {'msg': 'Invalid username or password'}
            return render(request, 'myapp/user_login.html',context)
    else:
        return render(request, 'myapp/user_login.html')

def user_home(request):
    user_id = request.session['user_id']
    ud = user_details.objects.get(user_id=int(user_id))
    context = {'fname': ud.f_name, 'lname': ud.l_name}
    return render(request,'./myapp/user_home.html',context)

def user_details_add(request):
    if request.method == 'POST':

        f_name = request.POST.get('fname')
        l_name = request.POST.get('lname')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        addr = request.POST.get('addr')
        pincode = request.POST.get('pincode')
        email = request.POST.get('email')
        contact = request.POST.get('contact')

        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        status = 'ok'

        password = request.POST.get('password')

        uname=email


        ul = user_login(uname=uname, password=password, utype='user')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        ud = user_details(user_id=user_id, dob=dob,f_name=f_name, l_name=l_name, gender=gender, addr=addr, pincode=pincode, contact=contact,
                               status=status,email=email,dt=dt,tm=tm )
        ud.save()

        print(user_id)
        context={'msg':'User Registered'}
        return render(request, 'myapp/user_login.html',context)

    else:
        return render(request, 'myapp/user_details_add.html')

def user_details_edit(request):
    if request.method == 'POST':

        f_name = request.POST.get('fname')
        l_name = request.POST.get('lname')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        addr = request.POST.get('addr')
        pincode = request.POST.get('pincode')
        email = request.POST.get('email')
        contact = request.POST.get('contact')

        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        status = 'ok'
        user_id = request.session['user_id']
        ud = user_details.objects.get(user_id=int(user_id))
        ud.f_name = f_name
        ud.l_name = l_name
        ud.dob = dob
        ud.gender = gender
        ud.addr = addr
        ud.pincode = pincode
        ud.email = email
        ud.contact= contact

        ud.save()

        return user_profile(request)

    else:
        user_id = request.session['user_id']
        ud1 = user_details.objects.get(user_id=int(user_id))
        context = {'ud': ud1}
        return render(request, 'myapp/user_details_edit.html',context)


def user_profile(request):
    user_id = request.session['user_id']
    ud1 = user_details.objects.filter(user_id=int(user_id))
    context = {'user_details': ud1}
    return render(request, './myapp/user_profile.html', context)


def user_changepassword(request):
    if request.method == 'POST':
        uname = request.session['user_name']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print("username:::" + uname)
        print("current_password" + str(current_password))

        try:

            ul = user_login.objects.get(uname=uname, password=current_password)

            if ul is not None:
                ul.password = new_password  # change field
                ul.save()
                context = {'msg':'Password changed'}
                return render(request, './myapp/user_changepassword.html',context)
            else:
                context = {'msg': 'Password change error'}
                return render(request, './myapp/user_changepassword.html',context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password change error'}
            return render(request, './myapp/user_changepassword.html',context)
    else:
        return render(request, './myapp/user_changepassword.html')

def user_settings(request):

    context = {'uname':request.session['user_name']}
    return render(request,'./myapp/user_settings.html',context)

def user_product_master_view(request):

    pm_l = product_master.objects.all()

    scm_l = sub_category_master.objects.all()
    scmd = {}
    for scm in scm_l:
        scmd[scm.id] = scm.sub_category_name

    context = {'product_list': pm_l, 'subcategory_list': scmd, 'msg': ''}
    return render(request, 'myapp/user_product_master_view.html', context)

def user_product_search(request):
    if request.method == 'POST':
        app_name = request.POST.get('app_name')

        pm_l = product_master.objects.filter(product_name__contains=app_name)

        scm_l = sub_category_master.objects.all()
        scmd = {}
        for scm in scm_l:
            scmd[scm.id] = scm.sub_category_name

        context = {'product_list': pm_l, 'subcategory_list': scmd, 'msg': ''}
        return render(request, 'myapp/user_product_master_view.html', context)
    else:
        return render(request, 'myapp/user_product_search.html')


def user_product_pic_view(request):
    product_master_id = request.GET.get('product_master_id')
    pp_l = product_pic.objects.filter(product_master_id=product_master_id)
    context = {'pic_list': pp_l, 'product_master_id': product_master_id, 'msg': ''}
    return render(request, 'myapp/user_product_pic_view.html', context)

def user_product_review_add(request):
    if request.method == 'POST':
        product_master_id = request.POST.get('product_master_id')
        user_id = request.session['user_id']
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        status = 'ok'
        pr = product_review(product_master_id=int(product_master_id),user_id=int(user_id),rating=int(rating),review=review,
                            dt=dt,tm=tm,status=status)
        pr.save()

        context = {'msg':'Review added','product_master_id':product_master_id}
        return render(request, 'myapp/user_product_review_add.html',context)

    else:
        product_master_id = request.GET.get('product_master_id')
        context = {'msg':'','product_master_id':product_master_id}
        return render(request, 'myapp/user_product_review_add.html',context)

def user_product_review_delete(request):
    id = request.GET.get('id')
    product_master_id = request.GET.get('product_master_id')
    print("id="+id)
    pp = product_review.objects.get(id=int(id))
    pp.delete()

    user_id = request.session['user_id']
    product_master_id = request.GET.get('product_master_id')
    pr_l = product_review.objects.filter(product_master_id=product_master_id, user_id=int(user_id))
    context = {'review_list': pr_l, 'product_master_id': product_master_id, 'msg': 'Review deleted'}
    return render(request, 'myapp/user_product_review_view.html', context)

def user_product_review_view(request):
    user_id=request.session['user_id']
    product_master_id = request.GET.get('product_master_id')
    pr_l = product_review.objects.filter(product_master_id=product_master_id,user_id=int(user_id))
    context = {'review_list': pr_l, 'product_master_id': product_master_id, 'msg': ''}
    return render(request, 'myapp/user_product_review_view.html', context)

def user_product_allreview_view(request):
    product_master_id = request.GET.get('product_master_id')
    pr_l = product_review.objects.filter(product_master_id=product_master_id)
    cmd={}
    umd = {}
    sentiment_rank_dict = dict()
    sel_id = 0
    sel_val = 0
    for pr in pr_l:
        ########################
        obj = AppClassification()
        result = obj.input_text_processing(pr.review)
        data_file_path = os.path.join(BASE_DIR, 'data/data_set.csv')
        data_file_label_path = os.path.join(BASE_DIR, 'data/data_set_label.dat')
        tfid_file_path = os.path.join(BASE_DIR, 'data/data_set_tfid.dat')
        model_file_path = os.path.join(BASE_DIR, 'data/data_set_svm.model')

        model = obj.load_data(model_file_path)
        Tfidf_vect = obj.load_data(tfid_file_path)
        p = obj.get_prediction(model, result, Tfidf_vect)
        label = obj.load_data(data_file_label_path)
        label = sorted(label)
        print(f'result = {label[p[0]]}')
        final_label = label[p[0]]
        if final_label in sentiment_rank_dict:
            val = sentiment_rank_dict[final_label]
            val +=1# pr.rating
            sentiment_rank_dict[final_label] = val
            if sel_val < val:
                sel_val = val
                sel_id = final_label
        else:
            val =1# pr.rating
            sentiment_rank_dict[final_label] = val
            if sel_val < val:
                sel_val = val
                sel_id = final_label
        ########################
        cmd[pr.id] = final_label
        uobj = user_login.objects.get(id=pr.user_id)
        udobj = user_details.objects.get(email=uobj.uname)
        umd[pr.user_id] = f'{udobj.f_name} {udobj.l_name}'
    print(sel_id)
    dd = {'positive':'Safe','negative':'Fake'}
    context = {'review_list': pr_l,'user_list': umd,'sentiment_list': cmd, 'product_master_id': product_master_id, 'msg': f'Based on analysis the app is {dd[sel_id]}'}
    return render(request, 'myapp/user_product_allreview_view.html', context)

def user_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return user_login_check(request)
    else:
        return user_login_check(request)

def company_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return company_login_check(request)
    else:
        return company_login_check(request)

def admin_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return admin_login(request)
    else:
        return admin_login(request)
