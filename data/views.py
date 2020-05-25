from django.shortcuts import render,redirect
from lib.xmlutils.xmlutils import xml2csv
import pandas as pd
from .models import Files,Contact
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    if request.method == 'POST':
        try:
            id=request.POST['id']
            tag_name = request.POST['tag_name']

            f=Files.objects.get(id=id)
            print(f.file)
            if tag_name != "":
                print("XML")

                converter = xml2csv.xml2csv(f.file, "static/xml2csv.csv")
                converter.convert(tag=tag_name)
                return render(request, "base.html", {"file": "xml2csv.csv","step1":True})
            else:
                print("JSON")

                try:
                    df = pd.read_json(f.file, typ='series', encoding='utf-8')
                    df.to_csv("static/json2csv.csv")
                except Exception as e:
                    f = Files.objects.get(id=id)
                    print(e,)
                    df = pd.read_json(f.file, encoding='utf-8')
                    df.to_csv("static/json2csv.csv")

                return render(request, "base.html", {"file": "json2csv.csv","step1":True})
        except Exception as e:
            print(e)
            messages = "Something wrong with your file"
            return render(request, "base.html", {"messages": messages,"step1":True})

    else:
        return render(request, "base.html",{"step1":True})


def contact(request):
    try:
        if request.method == "POST":
            name = request.POST['name']
            email = request.POST['email']
            subject = request.POST['subject']
            query_message = request.POST['message']
            print(name, email, subject, query_message)
            messages = "Thank You! our representative will contact you soon ..."

            Contact.objects.create(name=name,email=email,subject=subject,text=query_message)
            # For User Acknowlegement
            send_mail("Contact Us",messages,settings.EMAIL_HOST_USER,[email])

            # For Admin
            send_mail("Contact Us", query_message, settings.EMAIL_HOST_USER, [settings.ADMIN_EMAIL])

            return render(request, "base.html", {"messages": messages})
        else:
            return redirect("/")

    except Exception as e:
        return redirect("/")


def tag_name(request):
    try:
        file_extension = ["json", "xml"]
        if request.method == "POST":
            file = request.FILES['file']

            temp = file.name
            temp = temp[::-1].split(".")
            uploaded_file_extension = temp[0][::-1]

            if uploaded_file_extension in file_extension:
                f=Files()
                f.file = file
                f.save()
                if uploaded_file_extension == 'xml':
                    tree = xml2csv.et.parse(f.file)
                    tag_name = tree.getiterator()[1].tag
                    return render(request,'base.html',{"tag_name":tag_name,"id":f.id ,"step2" :True })

                else:
                    return render(request, 'base.html', {"tag_name": "", "id": f.id,"step2" :True })

    except Exception as e:
        messages = "Please enter json or xml file"
        return render(request, "base.html", {"messages": messages,"step1":True})

