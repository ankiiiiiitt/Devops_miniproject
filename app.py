import os
import datetime
import random
import PyPDF2
from flask import Flask, render_template, request, session, redirect, url_for, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from config import client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"

app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# ================= MONGODB SETUP =================
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/ai_sem_project")
mongo_client = MongoClient(MONGO_URI)
db = mongo_client.get_default_database() if mongo_client.get_default_database().name else mongo_client['ai_sem_project']

users_col = db.users
cache_col = db.cache
chats_col = db.chats
notes_col = db.notes
bookmarks_col = db.bookmarks

# ================= MAIL SETUP =================
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 465))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'False').lower() in ['true', '1', 't']
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'True').lower() in ['true', '1', 't']
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'your-email@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'your-app-password')

mail = Mail(app)

# ================= GROQ =================
def ask_ai(prompt):
    cached = cache_col.find_one({"prompt": prompt})
    if cached:
        return cached["response"]

    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        text = response.choices[0].message.content.strip()

    except Exception as e:
        print("GROQ ERROR:", e)
        return "AI service temporarily unavailable."

    cache_col.insert_one({"prompt": prompt, "response": text})
    return text


# ================= ROUTES =================

@app.route("/")
def home():
    user = session.get("user")
    return render_template("index.html", user=user)

# ================= NOTES =================
@app.route("/notes", methods=["GET", "POST"])
def notes():
    if "user" not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        if title and content:
            import datetime
            notes_col.insert_one({
                "user_email": session.get("user_email"),
                "title": title,
                "content": content,
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            })
        return redirect(url_for("notes"))
        
    user_notes = list(notes_col.find({"user_email": session.get("user_email")}).sort("created_at", -1))
    return render_template("notes.html", notes=user_notes)

@app.route("/notes/delete/<note_id>", methods=["POST"])
def delete_note(note_id):
    if "user" not in session:
        return redirect(url_for("login"))
        
    from bson.objectid import ObjectId
    try:
        notes_col.delete_one({"_id": ObjectId(note_id), "user_email": session.get("user_email")})
    except:
        pass
    return redirect(url_for("notes"))

# ================= BOOKMARKS =================
@app.route("/bookmark", methods=["POST"])
def add_bookmark():
    if "user" not in session:
        return {"error": "Unauthorized"}, 401

    data = request.json
    title = data.get("title")
    content = data.get("content")
    item_type = data.get("type", "AI Answer")

    if not content:
        return {"error": "Content is required"}, 400

    bookmark_doc = {
        "user_email": session.get("user_email"),
        "title": title or (content[:50] + "..." if len(content) > 50 else content),
        "content": content,
        "type": item_type,
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    
    bookmarks_col.insert_one(bookmark_doc)
    return {"status": "success", "message": "Bookmarked successfully!"}

@app.route("/bookmarks")
def bookmarks():
    if "user" not in session:
        return redirect(url_for("login"))
    
    user_bookmarks = list(bookmarks_col.find({"user_email": session.get("user_email")}).sort("created_at", -1))
    return render_template("bookmarks.html", bookmarks=user_bookmarks)

@app.route("/bookmarks/delete/<bookmark_id>", methods=["POST"])
def delete_bookmark(bookmark_id):
    if "user" not in session:
        return redirect(url_for("login"))
        
    from bson.objectid import ObjectId
    try:
        bookmarks_col.delete_one({"_id": ObjectId(bookmark_id), "user_email": session.get("user_email")})
    except:
        pass
    return redirect(url_for("bookmarks"))

# ================= CHAT =================
@app.route("/chat")
@app.route("/chat/<chat_id>")
def chat(chat_id=None):
    if "user" not in session:
        return redirect(url_for("login"))
    
    messages = []
    if chat_id:
        from bson.objectid import ObjectId
        from bson.errors import InvalidId
        try:
            current_chat = chats_col.find_one({"_id": ObjectId(chat_id), "user_email": session.get("user_email")})
            if current_chat:
                messages = current_chat.get("messages", [])
        except InvalidId:
            pass
            
    return render_template("chat.html", chat_id=chat_id, messages=messages)

@app.route("/api/chats")
def list_chats():
    if "user" not in session:
        return {"error": "Unauthorized"}, 401
    
    user_email = session.get("user_email")
    chats = list(chats_col.find({"user_email": user_email}).sort("updated_at", -1).limit(50))
    
    chat_list = []
    for c in chats:
        chat_list.append({
            "id": str(c["_id"]),
            "title": c.get("title", "New Chat")
        })
    return {"chats": chat_list}

@app.route("/api/chats/delete/<chat_id>", methods=["POST"])
def delete_chat(chat_id):
    if "user" not in session:
        return redirect(url_for("login"))
        
    from bson.objectid import ObjectId
    try:
        chats_col.delete_one({"_id": ObjectId(chat_id), "user_email": session.get("user_email")})
    except:
        pass
    return redirect(url_for("chat"))

@app.route("/chat_api", methods=["POST"])
def chat_api():
    if "user" not in session:
        return {"error": "Unauthorized"}, 401

    data = request.json
    chat_id = data.get("chat_id")
    user_message = data.get("message")
    user_email = session.get("user_email")
    
    if not user_message:
        return {"error": "Message is required"}, 400

    from bson.objectid import ObjectId
    import datetime

    chat_doc = None
    if chat_id:
        try:
            chat_doc = chats_col.find_one({"_id": ObjectId(chat_id), "user_email": user_email})
        except:
            chat_doc = None

    if not chat_doc:
        system_msg = {"role": "system", "content": "You are FocusVault, an incredibly smart, encouraging, and helpful AI study assistant."}
        chat_doc = {
            "user_email": user_email,
            "title": user_message[:30] + "..." if len(user_message) > 30 else user_message,
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "messages": [system_msg]
        }
        res = chats_col.insert_one(chat_doc)
        chat_id = str(res.inserted_id)
        chat_doc["_id"] = res.inserted_id

    new_user_msg = {"role": "user", "content": user_message}
    chat_doc["messages"].append(new_user_msg)
    
    try:
        response = client.chat.completions.create(
            messages=chat_doc["messages"],
            model="llama-3.3-70b-versatile"
        )
        reply = response.choices[0].message.content.strip()
        
        new_ai_msg = {"role": "assistant", "content": reply}
        chat_doc["messages"].append(new_ai_msg)
        
        chats_col.update_one(
            {"_id": ObjectId(chat_id)},
            {"$set": {
                "messages": chat_doc["messages"],
                "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }}
        )
        
        return {"reply": reply, "chat_id": chat_id}

    except Exception as e:
        print("GROQ CHAT ERROR:", e)
        return {"error": "AI service temporarily unavailable."}, 500

# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = users_col.find_one({"email": email})

        if user and check_password_hash(user.get("password", ""), password):
            session["user"] = user.get("name")
            session["user_email"] = user.get("email")
            return redirect(url_for("chat"))
        else:
            return render_template("login.html", error="Invalid email or password")

    return render_template("login.html")


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("user_email", None)
    return redirect(url_for("home"))


# ================= REGISTER =================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = users_col.find_one({"email": email})

        if existing_user:
            return render_template("register.html", error="User already exists")

        new_user = {
            "name": name,
            "age": int(age) if age else None,
            "gender": gender,
            "email": email,
            "password": generate_password_hash(password),
            "daily_count": 0,
            "last_reset": datetime.date.today().isoformat(),
            "otp": None,
            "otp_expiry": None
        }

        users_col.insert_one(new_user)
        return redirect(url_for("login"))

    return render_template("register.html")

# ================= FORGOT PASSWORD =================
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        user = users_col.find_one({"email": email})
        
        if not user:
            return render_template("forgot_password.html", error="Email not registered.")
            
        # Generate OTP
        otp = str(random.randint(100000, 999999))
        expiry = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=10)
        
        users_col.update_one(
            {"email": email},
            {"$set": {"otp": otp, "otp_expiry": expiry}}
        )
        
        # Send Email
        try:
            msg = Message("Your Password Reset OTP",
                          sender=app.config.get('MAIL_USERNAME'),
                          recipients=[email])
            msg.body = f"Your OTP for password reset is {otp}. It is valid for 10 minutes."
            mail.send(msg)
            
            # Save email in session temporarily to verify otp
            session['reset_email'] = email
            return redirect(url_for("verify_otp"))
        except Exception as e:
            print("Mail Error:", e)
            return render_template("forgot_password.html", error="Failed to send email. Please check configuration.")

    return render_template("forgot_password.html")

@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():
    if 'reset_email' not in session:
        return redirect(url_for("forgot_password"))
        
    if request.method == "POST":
        otp_entered = request.form.get("otp")
        email = session.get("reset_email")
        
        user = users_col.find_one({"email": email})
        
        if not user or not user.get("otp"):
            return render_template("verify_otp.html", error="Invalid request.")
            
        # Check expiry
        now = datetime.datetime.now(datetime.timezone.utc)
        otp_expiry = user.get("otp_expiry")
        if otp_expiry:
            if otp_expiry.tzinfo is None:
                otp_expiry = otp_expiry.replace(tzinfo=datetime.timezone.utc)
            if otp_expiry < now:
                return render_template("verify_otp.html", error="OTP has expired.")
            
        if user.get("otp") == otp_entered:
            session['otp_verified'] = True
            return redirect(url_for("reset_password"))
        else:
            return render_template("verify_otp.html", error="Invalid OTP.")
            
    return render_template("verify_otp.html")

@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if not session.get("otp_verified") or 'reset_email' not in session:
        return redirect(url_for("forgot_password"))
        
    if request.method == "POST":
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        if password != confirm_password:
            return render_template("reset_password.html", error="Passwords do not match.")
            
        email = session.get("reset_email")
        
        users_col.update_one(
            {"email": email},
            {
                "$set": {"password": generate_password_hash(password)},
                "$unset": {"otp": "", "otp_expiry": ""}
            }
        )
        
        session.pop('reset_email', None)
        session.pop('otp_verified', None)
        
        return redirect(url_for("login"))
        
    return render_template("reset_password.html")


# ================= AUTH CHECK =================
def login_required():
    if "user" not in session:
        return redirect(url_for("login"))


# ================= QUESTION GENERATOR =================
@app.route("/question-generator", methods=["GET", "POST"])
def question_generator():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        paragraph = request.form.get("paragraph")

        questions = ask_ai(
            f"Generate 5 exam questions in numbered format:\n{paragraph}"
        )

        questions_list = [q.strip() for q in questions.split("\n") if q.strip()]

        return render_template(
            "question_generator_result.html",
            questions=questions_list
        )

    return render_template("question_generator.html")

# ================= SUMMARIZER =================
@app.route("/summarizer", methods=["GET", "POST"])
def summarizer():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        text = request.form["user_text"]

        summary = ask_ai(
            f"Summarize the following text into clear exam-ready bullet points:\n{text}"
        )

        return render_template("summarizer_result.html", summary=summary)

    return render_template("summarizer.html")


# ================= QA =================
@app.route("/qa", methods=["GET", "POST"])
def qa():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        context = request.form["context"]
        question = request.form["question"]

        answer = ask_ai(
            f"Context:\n{context}\n\nQuestion:\n{question}"
        )

        return render_template("qa_result.html", answer=answer)

    return render_template("qa.html")


# ================= STUDY PLAN =================
@app.route("/study-plan", methods=["GET", "POST"])
def study_plan():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        syllabus = request.form.get("syllabus")
        topics = request.form.get("topics")
        start_date = request.form.get("start_date")
        deadline = request.form.get("deadline")

        plan = ask_ai(
            f"""
Create a structured daily study plan.

Syllabus:
{syllabus}

Topics:
{topics}

Start Date:
{start_date}

Deadline:
{deadline}

Format:
Day-wise plan with topics and revision.
"""
        )

        return render_template("study_plan_result.html", plan=plan)

    return render_template("study_plan.html")


# ================= UPLOAD NOTES =================
@app.route("/upload-notes", methods=["GET", "POST"])
def upload_notes():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        if "pdf_file" not in request.files:
            return render_template("upload_notes.html", error="No file part uploaded.")

        file = request.files["pdf_file"]
        if file.filename == '':
            return render_template("upload_notes.html", error="No selected file.")

        if not file.filename.lower().endswith('.pdf'):
            return render_template("upload_notes.html", error="Only PDF files are allowed.")

        # Read and check file size (5MB limit)
        file_data = file.read()
        if len(file_data) > 5 * 1024 * 1024:
            return render_template("upload_notes.html", error="File size exceeds the 5MB limit.")

        try:
            from io import BytesIO
            pdf = PyPDF2.PdfReader(BytesIO(file_data))
            text = ""
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

            if not text.strip():
                return render_template("upload_notes.html", error="Could not extract any text from the PDF.")

            # Limit text size to ~20000 characters to prevent API token limits
            text_to_process = text[:20000]

            summary = ask_ai(
                f"Summarize the following text into clear exam-ready bullet points:\n{text_to_process}"
            )

            questions_text = ask_ai(
                f"Generate 5 exam questions in numbered format based on the following text:\n{text_to_process}"
            )
            questions_list = [q.strip() for q in questions_text.split("\n") if q.strip()]

            return render_template(
                "upload_result.html",
                summary=summary,
                questions=questions_list
            )

        except Exception as e:
            print("PDF Extraction Error:", e)
            return render_template("upload_notes.html", error="An error occurred processing the PDF file.")

    return render_template("upload_notes.html")


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)