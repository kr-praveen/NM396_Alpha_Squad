# Importing required libraries
from flask import Flask, request, render_template, session, send_file
from db_access import td, fd, users
from werkzeug.utils import secure_filename
import os
import re
from main.main_layer import full_analysis
from main.main_rnn import make_model
from main.hybrid_predict import Hybrid_rate
from main import main_web_api
from main import main_cloud
from ibm_watson_access import tone_analyzer, nlu
# Initializing the Flask
app = Flask(__name__)
app.secret_key = "random1"
 
# Setting global variables
working_dir_path = os.getcwd().replace(os.sep, "/")
UPLOAD_TRAINING_FILES = working_dir_path+"/static/DBAlpha/TrainingDB/Files/"
UPLOAD_TRAINING_IMAGES = working_dir_path+"/static/DBAlpha/TrainingDB/Images/"
UPLOAD_TRAINING_MODELS = working_dir_path+"/static/DBAlpha/TrainingDB/Models/"
app.config['UPLOAD_TRAINING_FILES'] = UPLOAD_TRAINING_FILES
app.config['UPLOAD_TRAINING_IMAGES'] = UPLOAD_TRAINING_IMAGES
app.config['UPLOAD_TRAINING_MODELS'] = UPLOAD_TRAINING_MODELS
UPLOAD_FEEDBACK_FILES = working_dir_path+"/static/DBAlpha/FeedbackDB/Files/"
UPLOAD_FEEDBACK_IMAGES = working_dir_path+"/static/DBAlpha/FeedbackDB/Images/"
app.config['UPLOAD_FEEDBACK_FILES'] = UPLOAD_FEEDBACK_FILES
app.config['UPLOAD_FEEDBACK_IMAGES'] = UPLOAD_FEEDBACK_IMAGES
UPLOAD_CLOUD_FEEDBACK_FILES = working_dir_path+"/static/DBAlpha/FeedbackDB/Files/Cloud/"
UPLOAD_CLOUD_FEEDBACK_IMAGES = working_dir_path+"/static/DBAlpha/FeedbackDB/Images/Cloud/"
app.config['UPLOAD_CLOUD_FEEDBACK_FILES'] = UPLOAD_CLOUD_FEEDBACK_FILES
app.config['UPLOAD_CLOUD_FEEDBACK_IMAGES'] = UPLOAD_CLOUD_FEEDBACK_IMAGES
DOWNLOAD_RESULT_FILE = working_dir_path+"/static/DBAlpha/FeedbackDB/Results/"
app.config['DOWNLOAD_RESULT_FILE'] = DOWNLOAD_RESULT_FILE



# =============================================================================
# ======> Home Page <========
# =============================================================================

@app.route("/")
def homepage():    
    return render_template('index.html')

@app.route("/home", methods=['GET', 'POST'])
def submitContactFormHomepage():
    name = request.form['name']
    email = request.form['email']
    comments = request.form['comments']
    import boto3
    from datetime import datetime
    dynamoDB = boto3.resource('dynamodb')
    dynamoTable = dynamoDB.Table('contact-form')
    time_field = str(datetime.now()).replace(":","").replace(" ","").replace("-","")
    dynamoTable.put_item(
            Item = { "date":str(time_field),
                    "name":name,
                    "email":email,
                    "comments":comments,
                    }
            )
    return render_template('index.html')
            

@app.route("/userDashboardHome")
def userDashboardHome():
    if session.get('u-type') is None:
        return render_template('error_page.html')
    return render_template('userDashboard.html')



# =============================================================================
# =============> Error Page <=============
# =============================================================================

@app.route("/errorPage")
def error_page():    
    return render_template('error_page.html')



# =============================================================================
# ==============> Sentence Based Analysis <================== 
# =============================================================================

@app.route("/singleComment")
def single_comment():
    return render_template('singleComment.html')

@app.route("/singleComment", methods=['GET', 'POST'])
def predict_single_comment():
    feedback_str = request.form['feedback']
    hrate = Hybrid_rate(lang = "multi")
    rating = hrate.get_hybrid_rating(feedback_str) 
    feed_json = {"comment": feedback_str}
    try:
        tone = tone_analyzer.analyze_tone(feedback_str)['document_tone']['tones']
        entity_json = nlu.extract_entities(feedback_str)['entities']
        print("1")
        return render_template('singleComment.html', predicted_result = rating, feed_json = feed_json, tone = tone, entity_json = entity_json)
    
    except:
        print("0")
        return render_template('singleComment.html', predicted_result = rating, feed_json = feed_json)



# =============================================================================
# ========>Training Dataset<==========
# Add and View Training Dataset
# =============================================================================

@app.route("/addTrainingData")
def add_td():
    if session.get('u-type') is None:
        return render_template('error_page.html')
    return render_template('addTrainingDatasets.html')

@app.route("/viewTrainingData")
def view_td():
    if session.get('u-type') is None:
        return render_template('error_page.html')
    td_obj = td.TdDAO()
    td_names = td_obj.fetch_all_td()
    return render_template('viewTrainingDatasets.html',td_names = td_names )



# =============================================================================
# ========>Feedback Dataset<==========
# Add and View Feedback Dataset (Local + Cloud)
# =============================================================================

@app.route("/addFeedbackData")
def add_fd():
    if session.get('u-type') is None:
        return render_template('error_page.html')
    td_obj = td.TdDAO()
    training_data_dict = td_obj.fetch_all_td()
    return render_template('addFeedbackDatasets.html', dict_training_data = training_data_dict)  

@app.route("/viewFeedbackData")
def view_fd():
    if session.get('u-type') is None:
        return render_template('error_page.html')
    # Fetching from Local Server
    fd_obj = fd.FdDAO()
    fd_names = fd_obj.fetch_all_fd()
    #Fetching from Cloud Server
    import boto3
    import botocore
    s3 = boto3.client('s3')
    dynamoDB = boto3.resource('dynamodb')
    dynamoTable = dynamoDB.Table('feedback-form-data')
    response = dynamoTable.scan()
    items = response['Items']
    BUCKET_NAME = 'feedback-data-try'
    s3 = boto3.resource('s3')
    KEY=[]
    fd_cloud_names = items
    for val in items:
        KEY.append('static/DBAlpha/FeedbackDB/Images/'+str(val['fd_img']))
        try:
            s3.Bucket(BUCKET_NAME).download_file('static/DBAlpha/FeedbackDB/Images/'+str(val['fd_img']), 'static/DBAlpha/FeedbackDB/Images/Cloud/'+str(val['fd_img']))
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise
    # Rendering the template with both local and cloud feedback dataset details
    return render_template('viewFeedbackDatasets.html',fd_names = fd_names, fd_cloud_names = fd_cloud_names)



# =============================================================================
# ========>Training Data Upload<=========
# Uploading and Processing the Training Dataset Files along
# with generation of pkl model file
# =============================================================================

@app.route("/addTDConfirm", methods = ['GET', 'POST'])
def add_td_confirm():
    if session.get('u-type') is None:
        return render_template('error_page.html')
    if request.method == "POST":
        td_name = request.form['td-name']
        thumb_img  = request.files['thumb-nail']
        td_file = request.files['td-file']
        thumb_img_name = secure_filename(thumb_img.filename)
        td_file_name = secure_filename(td_file.filename)
        desc = request.form['td-desc']
        td_obj = td.TdDAO()        
        from datetime import date,datetime
        today = date.today()    
        text_to_append = str(datetime.now())[:-7].replace(":","").replace(" ","").replace("-","")
        file_name1 = os.path.splitext(thumb_img_name)
        thumb_img_name  ="IMG" + str(text_to_append) +file_name1[1]
        file_name1 = os.path.splitext(td_file_name)
        td_file_name  = "TD"+ str(text_to_append) +file_name1[1]
        thumb_img.save(os.path.join(app.config['UPLOAD_TRAINING_IMAGES'], thumb_img_name))
        td_file.save(os.path.join(app.config['UPLOAD_TRAINING_FILES'], td_file_name))        
        status = td_obj.setData(td_name, thumb_img_name, td_file_name, 0, desc, 'sample.pkl', str(today),97.65)
        json_td_file_name = {"td_file" : td_file_name}
        return render_template("generatePKL.html", status = status, json_td_file_name = json_td_file_name)


@app.route("/viewTrainingData",methods = ['GET', 'POST'])
def generate_pkl():
    if session.get('u-type') is None:
        return render_template('error_page.html')
    import re
    td_file_name = request.form['td_file']
    td_file_name_without_ext = re.sub(".json", "", td_file_name)
    accuracy= make_model(file_name = td_file_name, column_review='reviewText', column_rating='overall', json_balanced = False, have_corpus = False, size = 25000)
    model_name = td_file_name_without_ext + ".h5"
    td_dao = td.TdDAO()
    td_dao.updateModel(td_file_name, model_name, accuracy*100)
    return render_template("confirmTD.html", status = 1)


# =============================================================================
# ========>Feedback Data Upload<=========
# Uploading and Processing the Feedback Dataset Files along
# with presenting results
# =============================================================================

@app.route("/addFDConfirm",methods = ['GET', 'POST'])
def add_fd_confirm():
    if session.get('u-type') is None:
        return render_template('error_page.html')
    if request.method == "POST":      
        fd_name = request.form['fd-name']
        thumb_img  = request.files['thumb-nail']
        fd_file = request.files['fd-file']
        thumb_img_name = secure_filename(thumb_img.filename)
        fd_file_name = secure_filename(fd_file.filename)
        desc = request.form['fd-desc']
        td_id = request.form['td-id']
        fd_obj = fd.FdDAO()        
        from datetime import date,datetime
        today = date.today()    
        text_to_append = str(datetime.now())[:-7].replace(":","").replace(" ","").replace("-","")
        file_name1 = os.path.splitext(thumb_img_name)
        thumb_img_name  ="IMG" + str(text_to_append) +file_name1[1]
        file_name1 = os.path.splitext(fd_file_name)
        fd_file_name  = "TD"+ str(text_to_append) +file_name1[1]        
        if request.form['cloud_local'] == 'local':
            thumb_img.save(os.path.join(app.config['UPLOAD_FEEDBACK_IMAGES'], thumb_img_name))
            fd_file.save(os.path.join(app.config['UPLOAD_FEEDBACK_FILES'], fd_file_name))
            status = fd_obj.setData(fd_name, thumb_img_name,str(td_id), fd_file_name,  desc,  str(today),"sample.json")
            
        elif request.form['cloud_local'] == 'cloud':
            thumb_img.save(os.path.join(app.config['UPLOAD_CLOUD_FEEDBACK_IMAGES'], thumb_img_name))
            fd_file.save(os.path.join(app.config['UPLOAD_CLOUD_FEEDBACK_FILES'], fd_file_name))
            import boto3
            s3 = boto3.client('s3')
            with open(os.path.join(app.config['UPLOAD_CLOUD_FEEDBACK_FILES'], fd_file_name), "rb") as f:
                s3.upload_fileobj(f, "feedback-data-try", 'static/DBAlpha/FeedbackDB/Files/'+str(fd_file_name))
            with open(os.path.join(app.config['UPLOAD_CLOUD_FEEDBACK_IMAGES'], thumb_img_name), "rb") as f:
                s3.upload_fileobj(f, "feedback-data-try", 'static/DBAlpha/FeedbackDB/Images/'+str(thumb_img_name))
            if os.path.exists(os.path.join(app.config['UPLOAD_CLOUD_FEEDBACK_FILES'], fd_file_name)):
              os.remove(os.path.join(app.config['UPLOAD_CLOUD_FEEDBACK_FILES'], fd_file_name))
            else:
              print("The file does not exist")
            if os.path.exists(os.path.join(app.config['UPLOAD_CLOUD_FEEDBACK_IMAGES'], thumb_img_name)):
              os.remove(os.path.join(app.config['UPLOAD_CLOUD_FEEDBACK_IMAGES'], thumb_img_name))
            else:
              print("The file does not exist")
            dynamoDB = boto3.resource('dynamodb')
            dynamoTable = dynamoDB.Table('feedback-form-data')
            time_field = str(datetime.now()).replace(":","").replace(" ","").replace("-","")
            dynamoTable.put_item(
                        Item = { "date":str(time_field),
                                 "fd_desc":desc,
                                 "fd_file":fd_file_name,
                                 "fd_img":thumb_img_name,
                                 "fd_name":fd_name,
                                 "result_page":"sample.json",
                                 "td_id":str(td_id)
                                }
                    )
            status = 1
        return render_template("confirmTD.html", status = status)



# =============================================================================
# ========>Modify/Remove Training Data<=========
# =============================================================================

@app.route("/editTDData", methods = ['GET','POST'])
def edit_td_data():
    if session.get('u-type') is None:
        return render_template('error_page.html')
    if request.method =="POST":
        td_id = request.form['td-id']
        td_obj = td.TdDAO()
        p =td_obj.getData(td_id)        
        return render_template("editTrainingDataset.html", p = p)

@app.route("/editTDDataConfirm", methods = ['GET', 'POST'])
def edit_td_data_Confirm():
    if session.get('u-type') is None:
        return render_template('error_page.html')
    if request.method == "POST":
        req_type = request.form['submit']
        td_id = request.form['td-id']
        td_obj = td.TdDAO()        
        if req_type == 'update':
            td_name = request.form['td-name']
            td_desc = request.form['td-desc']
            status = (td_obj.updateName(td_id, td_name)) and (td_obj.updateDesc(td_id, td_desc))
            td_names = td_obj.fetch_all_td()
            return render_template("viewTrainingDatasets.html",td_names = td_names)
        elif req_type == 'remove':
            file_name = request.form['td-file']
            file_name = re.sub(".json ", "", file_name)
            status = td_obj.delete_dataset(td_id, UPLOAD_TRAINING_FILES+str(request.form['td-file']), UPLOAD_TRAINING_IMAGES+str(request.form['td-img']), 
                                           UPLOAD_TRAINING_MODELS+str(file_name)+".h5", UPLOAD_TRAINING_MODELS+"TOKEN_"+str(file_name)+".pkl")
            print("Dataset Deleted Status: ", status)
            td_names = td_obj.fetch_all_td()
            return render_template("viewTrainingDatasets.html",td_names = td_names)
            
        

# =============================================================================
# ========>Modify/Remove Feedback Data<=========
# =============================================================================

@app.route("/editFDData", methods=['GET', 'POST'])    
def edit_fd_data():
    if session.get('u-type') is None:
        return render_template('error_page.html')
    if request.method =="POST":
        fd_id = request.form['fd-id']
        fd_dao = fd.FdDAO()
        fd_obj = fd.FdObj()
        fd_obj = fd_dao.getData(fd_id)
        req_type = request.form['submit']
        if req_type =="modify":
            td_dao = td.TdDAO()
            training_data_dict = td_dao.fetch_all_td()
            td_obj = td.TdObj()
            td_obj = td_dao.getData(fd_obj.tid)
            return render_template("editFeedbackDataset.html", p = fd_obj, td_id = td_obj.id, dict_training_data = training_data_dict, storage_type= str("local"))
        elif req_type =="result-page":
            td_dao = td.TdDAO()
            model_file = td_dao.getFileNamebyID(fd_obj.tid)
            model_file = re.sub(".json", "", model_file)
            aspect_json, overall_rate, progress_json, suggestions_json = full_analysis(file_name = fd_obj.file, model_file = model_file, no_entities = 2, lang="")
            return render_template("results.html", aspect_json = aspect_json, overall_rate = overall_rate, progress_json = progress_json, suggestions_json = suggestions_json, fd_id = fd_id)
        
@app.route("/editFDCloudData", methods=['GET','POST'])
def edit_fd_cloud_data():
    if session.get('u-type') is None:
        return render_template('error_page.html')
    import boto3
    dynamoDB = boto3.resource('dynamodb')
    dynamoTable = dynamoDB.Table('feedback-form-data')
    fd_date = request.form['fd-date-id']
    response = dynamoTable.get_item(
    Key={ 'date': fd_date})
    item = response['Item']
    fd_obj = fd.FdObj()
    fd_obj.name = item['fd_name']
    fd_obj.image = item['fd_img']
    fd_obj.tid = item['td_id']
    fd_obj.file = item['fd_file']
    fd_obj.desc = item['fd_desc']
    fd_obj.date = fd_date
    fd_obj.result_page = item['result_page']
    fd_obj.fid = fd_date
    req_type = request.form['submit']
    if req_type =="modify":
        td_dao = td.TdDAO()
        training_data_dict = td_dao.fetch_all_td()
        td_obj = td.TdObj()
        td_obj = td_dao.getData(fd_obj.tid)
        return render_template('editFeedbackDataset.html', p = fd_obj, td_id = td_obj.id, dict_training_data = training_data_dict, storage_type= str("cloud"))
    elif req_type =="result-page":
        td_dao = td.TdDAO()
        model_file = td_dao.getFileNamebyID(fd_obj.tid)
        import botocore
        s3 = boto3.resource('s3')
        BUCKET_NAME = 'feedback-data-try'
        try:
            s3.Bucket(BUCKET_NAME).download_file('static/DBAlpha/FeedbackDB/Files/'+str(fd_obj.file), 'static/DBAlpha/FeedbackDB/Files/'+str(fd_obj.file))
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise

        model_file = re.sub(".json", "", model_file)
        aspect_json, overall_rate, progress_json, suggestions_json = full_analysis(file_name = fd_obj.file, model_file = model_file, no_entities = -1, lang="")
        return render_template("results.html", aspect_json = aspect_json, overall_rate = overall_rate, progress_json = progress_json, suggestions_json = suggestions_json, fd_id = fd_obj.fid)

       
@app.route("/editFDDataConfirm", methods = ['GET', 'POST'])
def edit_fd_data_Confirm():
    if session.get('u-type') is None:
        return render_template('error_page.html')
    if request.method == "POST":
        storage_type = request.form['storage-type']
        req_type = request.form['submit']
        fd_obj = fd.FdDAO()
        if storage_type == "local":
            if req_type == "update":
                fd_id = request.form['fd-id']
                fd_name = request.form['fd-name']
                fd_desc = request.form['fd-desc']
                fd_td = request.form['fd-td']
                status = (fd_obj.updateName(fd_id, fd_name)) and (fd_obj.updateDesc(fd_id, fd_desc)) and (fd_obj.updateTrainingData(fd_id, fd_td))
            elif req_type == "remove":
                fd_id = request.form['fd-id']
                status = fd_obj.delete_dataset(fd_id, UPLOAD_FEEDBACK_FILES+str(request.form['fd-file']), UPLOAD_FEEDBACK_IMAGES+str(request.form['fd-img']), DOWNLOAD_RESULT_FILE, request.form['fd-file'])
                print("Dataset Deleted Status: ", status)
            
        elif storage_type == "cloud":
            fd_id = request.form['fd-id']
            if req_type == "update":
                fd_name = request.form['fd-name']
                fd_desc = request.form['fd-desc']
                fd_td = request.form['fd-td']
                import boto3
                dynamoDB = boto3.resource('dynamodb')
                dynamoTable = dynamoDB.Table('feedback-form-data')
                dynamoTable.update_item(
                        Key = {
                                'date':fd_id
                                },
                        UpdateExpression = 'SET fd_name = :name, fd_desc = :desc, td_id = :td',
                        ExpressionAttributeValues = {
                                ':name': fd_name,
                                ':desc': fd_desc,
                                ':td': fd_td
                                },
                        )
            elif req_type== "remove":
                fd_img = request.form['fd-img']
                fd_file = request.form['fd-file']
                import boto3
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('feedback-form-data')
                status = fd_obj.delete_cloud_files(UPLOAD_FEEDBACK_FILES+str(request.form['fd-file']), UPLOAD_CLOUD_FEEDBACK_IMAGES+str(request.form['fd-img']), DOWNLOAD_RESULT_FILE, request.form['fd-file'])
                print("Dataset Deleted Status: ", status)
                table.delete_item( Key={'date': fd_id})
                client = boto3.client('s3')
                responseDeleteFile = client.delete_object(
                        Bucket='feedback-data-try',
                        Key='static/DBAlpha/FeedbackDB/Files/'+fd_file
                        )
                responseDeleteImage = client.delete_object(
                        Bucket='feedback-data-try',
                        Key='static/DBAlpha/FeedbackDB/Images/'+fd_img
                        )
                print("File Deleted Response: ",responseDeleteFile)
                print("Image Deleted Response: ", responseDeleteImage)
                
        # Fetching all records to present
        fd_names = fd_obj.fetch_all_fd()
        import boto3
        import botocore
        s3 = boto3.client('s3')
        dynamoDB = boto3.resource('dynamodb')
        dynamoTable = dynamoDB.Table('feedback-form-data')
        response = dynamoTable.scan()
        items = response['Items']
        BUCKET_NAME = 'feedback-data-try' # Bucket name
        s3 = boto3.resource('s3')
        KEY=[]
        fd_cloud_names = items
        for val in items:
            KEY.append('static/DBAlpha/FeedbackDB/Images/'+str(val['fd_img']))
            try:
                s3.Bucket(BUCKET_NAME).download_file('static/DBAlpha/FeedbackDB/Images/'+str(val['fd_img']), 'static/DBAlpha/FeedbackDB/Images/Cloud/'+str(val['fd_img']))
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    print("The object does not exist.")
                else:
                    raise
                    
        # Rendering the view feedbak data template
        return render_template('viewFeedbackDatasets.html',fd_names = fd_names, fd_cloud_names = fd_cloud_names)


# =============================================================================
# ========> Downloading Sample Feedback and Training Dataset Files <========
# =============================================================================
@app.route("/downloadSampleFeedbackData")
def download_sample_feedback_dataset():
    if session.get('u-type') is None:
        return render_template('error_page.html')
    file_name = "Sample_Feedback_Data.json"
    return send_file(str(UPLOAD_FEEDBACK_FILES)+str(file_name),as_attachment=True)

@app.route("/downloadSampleTrainingData")
def download_sample_training_dataset():
    if session.get('u-type') is None:
        return render_template('error_page.html')
    file_name = "Sample_Training_Data.json"
    return send_file(str(UPLOAD_TRAINING_FILES)+str(file_name),as_attachment=True)

# =============================================================================
# =============> Downloading the Result Files <=================       
# =============================================================================
@app.route("/viewDownloadableFiles/<fd_id>")
def viewDownloadableFiles(fd_id):
    if session.get('u-type') is None:
        return render_template('error_page.html')
    return render_template('download_result_files.html', fd_id = fd_id)

@app.route("/downloadOverallAnalysisXLSX/<fd_id>")
def downloadOverallAnalysisXLSX(fd_id):
    if session.get('u-type') is None:
        return render_template('error_page.html')
    if fd_id == str(-1):
        fd_file = "WebAPI"
    elif len(fd_id)>14:
        fd_file = main_cloud.get_file_name_by_id(fd_id)
        fd_file = re.sub(".json", "", fd_file)
    else:
        fd_dao = fd.FdDAO()
        fd_file = fd_dao.getFileNamebyID(fd_id)
        fd_file = re.sub(".json", "", fd_file)
    file_name = fd_file+'_Individual_Comment_Ratings.xlsx'
    return send_file(str(DOWNLOAD_RESULT_FILE)+str(file_name),as_attachment=True)

@app.route("/downloadAspectBasedAnalysisXLSX/<fd_id>")
def downloadAspectBasedAnalysisXLSX(fd_id):
    if session.get('u-type') is None:
        return render_template('error_page.html')
    if fd_id == str(-1):
        fd_file = "WebAPI"
    elif len(fd_id)>14:
        fd_file = main_cloud.get_file_name_by_id(fd_id)
        fd_file = re.sub(".json", "", fd_file)
    else:
        fd_dao = fd.FdDAO()
        fd_file = fd_dao.getFileNamebyID(fd_id)
        fd_file = re.sub(".json", "", fd_file)
    file_name = fd_file+'_Aspect_Based_Analysis.xlsx'
    return send_file(str(DOWNLOAD_RESULT_FILE)+str(file_name),as_attachment=True)

@app.route("/downloadProgressTimelineAnalysisXLSX/<fd_id>")
def downloadProgressTimelineAnalysisXLSX(fd_id):
    if session.get('u-type') is None:
        return render_template('error_page.html')
    if fd_id == str(-1):
        fd_file = "WebAPI"
    elif len(fd_id)>14:
        fd_file = main_cloud.get_file_name_by_id(fd_id)
        fd_file = re.sub(".json", "", fd_file)
    else:
        fd_dao = fd.FdDAO()
        fd_file = fd_dao.getFileNamebyID(fd_id)
        fd_file = re.sub(".json", "", fd_file)
    file_name = fd_file+'_Progress_Timeline.xlsx'
    return send_file(str(DOWNLOAD_RESULT_FILE)+str(file_name),as_attachment=True)

@app.route("/downloadSuggestionsAnalysisJSON/<fd_id>")
def downloadSuggestionsAnalysisJSON(fd_id):
    if session.get('u-type') is None:
        return render_template('error_page.html')
    if fd_id == str(-1):
        fd_file = "WebAPI"
    elif len(fd_id)>14:
        fd_file = main_cloud.get_file_name_by_id(fd_id)
        fd_file = re.sub(".json", "", fd_file)
    else:
        fd_dao = fd.FdDAO()
        fd_file = fd_dao.getFileNamebyID(fd_id)
        fd_file = re.sub(".json", "", fd_file)
    file_name = fd_file+'_Suggestions.json'
    return send_file(str(DOWNLOAD_RESULT_FILE)+str(file_name),as_attachment=True)

    
@app.route("/downloadOverallAnalysisCSV/<fd_id>")
def downloadOverallAnalysisCSV(fd_id):
    if session.get('u-type') is None:
        return render_template('error_page.html')
    if fd_id == str(-1):
        fd_file = "WebAPI"
    elif len(fd_id)>14:
        fd_file = main_cloud.get_file_name_by_id(fd_id)
        fd_file = re.sub(".json", "", fd_file)
    else:
        fd_dao = fd.FdDAO()
        fd_file = fd_dao.getFileNamebyID(fd_id)
        fd_file = re.sub(".json", "", fd_file)
    file_name = fd_file+'_Individual_Comment_Ratings.csv'
    return send_file(str(DOWNLOAD_RESULT_FILE)+str(file_name),as_attachment=True)

@app.route("/downloadAspectBasedAnalysisCSV/<fd_id>")
def downloadAspectBasedAnalysisCSV(fd_id):
    if session.get('u-type') is None:
        return render_template('error_page.html')
    if fd_id == str(-1):
        fd_file = "WebAPI"
    elif len(fd_id)>14:
        fd_file = main_cloud.get_file_name_by_id(fd_id)
        fd_file = re.sub(".json", "", fd_file)
    else:
        fd_dao = fd.FdDAO()
        fd_file = fd_dao.getFileNamebyID(fd_id)
        fd_file = re.sub(".json", "", fd_file)
    file_name = fd_file+'_Aspect_Based_Analysis.csv'
    return send_file(str(DOWNLOAD_RESULT_FILE)+str(file_name),as_attachment=True)

@app.route("/downloadProgressTimelineAnalysisCSV/<fd_id>")
def downloadProgressTimelineAnalysisCSV(fd_id):
    if session.get('u-type') is None:
        return render_template('error_page.html')
    if fd_id == str(-1):
        fd_file = "WebAPI"
    elif len(fd_id)>14:
        fd_file = main_cloud.get_file_name_by_id(fd_id)
        fd_file = re.sub(".json", "", fd_file)
    else:
        fd_dao = fd.FdDAO()
        fd_file = fd_dao.getFileNamebyID(fd_id)
        fd_file = re.sub(".json", "", fd_file)
    file_name = fd_file+'_Progress_Timeline.csv'
    return send_file(str(DOWNLOAD_RESULT_FILE)+str(file_name),as_attachment=True)



# =============================================================================
# ============> Web API <============
# =============================================================================
@app.route("/webAPI", methods = ['GET', 'POST'])
def view_web_api():
    if session.get('u-type') is None:
        return render_template('error_page.html')
    return render_template('viewWebAPI.html')

@app.route("/webAPIResults", methods = ['GET', 'POST'])
def view_web_api_results():
    if session.get('u-type') is None:
        return render_template('error_page.html')
    main_web_api.store_web_api()
    aspect_json, overall_rate, progress_json, suggestions_json = full_analysis(file_name = "WebAPI.json", model_file = "TD20200309210544", no_entities = -1, lang="")
    return render_template("results.html", aspect_json = aspect_json, overall_rate = overall_rate, progress_json = progress_json, suggestions_json = suggestions_json, fd_id = -1)

@app.route("/downloadWebAPIDataset")
def download_web_api_dataset():
    if session.get('u-type') is None:
        return render_template('error_page.html')
    main_web_api.store_web_api()
    file_name = "WebAPI.json"
    return send_file(str(UPLOAD_FEEDBACK_FILES)+str(file_name),as_attachment=True)
    
# =============================================================================
# =============> User Login/Logout Modules <=============
# =============================================================================
@app.route("/loginConfirm", methods=['POST'])
def login_confirm():
    u_name = request.form["u_name"]    
    u_pwd = request.form["u_pwd"]
    if u_name=="alpha_squad" and u_pwd == "alpha":
        session['u-type'] = 'super-admin'
        return render_template("userDashboard.html")
    user_obj = users.UserDAO()
    obj = user_obj.getData(u_name, u_pwd)
    if obj ==False:
        return render_template("index.html")
    else:
        session['username'] = u_name
        session['u-type'] = 'admin'
        session['u-name'] = obj.name
        session['u-dept'] = obj.dept
        session['u-email'] = obj.email
        session['u-phone'] = obj.phone
        return render_template("userDashboard.html")


@app.route("/logout",methods = ['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.pop('u-type', None)
    session.pop('u-name', None)
    session.pop('u-dept', None)
    session.pop('u-email', None)
    session.pop('u-phone', None)
    filelist = [ f for f in os.listdir(app.config['UPLOAD_CLOUD_FEEDBACK_IMAGES']) if f.endswith(".png") ]
    for f in filelist:
        os.remove(os.path.join(app.config['UPLOAD_CLOUD_FEEDBACK_IMAGES'], f))
    return render_template("index.html")



# =============================================================================
# =============>User Dashboard<=============
# =============================================================================

@app.route("/dashboard" , methods=['GET','POST'])
def dashboard():
    if session.get('u-type') is None:
        return render_template('error_page.html')
    return render_template("userDashboard.html")
    
 
    
# =============================================================================
# ==================>User Management<===================
# Add, Remove and Modify users
# =============================================================================

@app.route("/userManagement", methods = ['GET', 'POST'])
def user_management():
    if session.get('u-type') is None:
        return render_template('error_page.html')
    user_obj = users.UserDAO()
    user_data = user_obj.fetch_all_users()  
    return render_template("userManagement.html",user_data = user_data)
   
@app.route("/userManagementAction", methods = ['GET', 'POST'])
def user_management_action():
    if session.get('u-type') is None:
        return render_template('error_page.html')
    user_obj = users.UserDAO()
    req_type = request.form['submit']
    if req_type == "add":
        user_obj.setData(request.form['uname'], request.form['pwd'], request.form['name'], request.form['dept'], request.form['email'], request.form['phone'])
        user_data = user_obj.fetch_all_users()
        return render_template("userManagement.html", user_data = user_data)
    if req_type == "update":
        user_obj.updateName(request.form['uname'],request.form['name'])
        user_obj.updateEmail(request.form['uname'],request.form['email'])
        user_obj.updatePhone(request.form['uname'],request.form['phone'])
        user_obj.updatePwd(request.form['uname'],request.form['pwd'])
        user_obj.updateDept(request.form['uname'],request.form['dept'])
        user_data = user_obj.fetch_all_users()
        return render_template("userManagement.html", user_data = user_data)
    if req_type == "remove":
        user_obj.delete_user(request.form['uname'])
        user_data = user_obj.fetch_all_users()
        return render_template("userManagement.html", user_data = user_data)
    
    
    
# =============================================================================
# =================>Calling the Flask Server<====================
# =============================================================================
        
if __name__ == "__main__":
    app.run(debug=False)
    
