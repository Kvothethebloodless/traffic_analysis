from flask import Flask, request, redirect, url_for, render_template, make_response, Response
#import flask
import os
import json
import glob
from uuid import uuid4

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index2.html")

@app.route("/zip/<foldername>")
def getFile(foldername):
    folder_path = "uploadr/static/uploads/"+foldername+"/"
    zip_name = "uploadr/static/uploads/"+foldername+'.zip'
    file_names = folder_path+'*'
    command = 'zip '+zip_name+' '+file_names+' --junk-names'
    print(command)
    os.system(command)
    print(os.getcwd())
    print("Requested to compress "+foldername)
    # headers = {"Content-Disposition": "attachment; filename=%s" % file_name}
    # with open(file_name, 'r') as f:
        # body = f.read()
    # resp = Response(body)
    resp = make_response("OK")
    resp.headers['Content-Disposition']='attachment'
    resp.headers['filename']=zip_name
    resp.headers["Content-type"] = "zip"
    return resp

@app.route("/download_helper/static/uploads/<foldername>/<filename>")
def downloadhelper(foldername,filename):
    return redirect("/download/static/uploads/"+foldername+'/'+filename)


@app.route("/upload", methods=["POST"])
def upload():
    """Handle the upload of a file."""
    form = request.form

    # Create a unique "session ID" for this particular batch of uploads.

    # Is the upload using Ajax, or a direct POST by the form?
    is_ajax = False
    if form.get("__ajax", None) == "true":
        is_ajax = True

    # Target folder for these uploads.
        #except:
   #     if is_ajax:
    #        return ajax_response(False, "Couldn't create upload directory: {}".format(target))
    #    else:
    #        return "Couldn't create upload directory: {}".format(target)

    print "=== Form Data ==="
    for key, value in form.items():
        print key, "=>", value
    its = form.items()
    filename = its[1][1]
    upload_key = str(filename)
    print(upload_key)
    upload_key = upload_key.replace(' ','')
    upload_key = upload_key.replace('.','')
    target = "uploadr/static/uploads/{}".format(upload_key)
    if(not (os.path.isdir(target))):
        os.mkdir(target)

    for upload in request.files.getlist("file"):
        #filename = upload.filename.rsplit("/")[0]
        print upload
        #destination = "/".join([target, filename])
        print "Accept incoming file:", "filegame"
        #print "Save it to:", destination
        #upload.save(destination)

    if is_ajax:
        return ajax_response(True, upload_key)
    else:
        return redirect(url_for("upload_complete", uuid=upload_key))


@app.route("/files/<uuid>")
def upload_complete(uuid):
    """The location we send them to at the end of the upload."""

    # Get their files.
    root = "uploadr/static/uploads/{}".format(uuid)
    if not os.path.isdir(root):
        return "Error: UUID not found!"

    files = []
    for file in glob.glob("{}/*.*".format(root)):
        fname = file.split(os.sep)[-1]
        files.append(fname)

    return render_template("files2.html",
        uuid=uuid,
        files=files,
    )


def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return json.dumps(dict(
        status=status_code,
        msg=msg,
    ))
