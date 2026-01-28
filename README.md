\# 📘 Smart Study Routine Generator



Smart Study Routine Generator is a full-stack web application designed to help students create personalized, balanced, and effective study routines based on their subjects, difficulty levels, weaknesses, and available study time.



---



\## 📌 Project Information



\- \*\*Project Title:\*\* Smart Study Routine Generator  

\- \*\*Course:\*\* Final Project  

\- \*\*Department:\*\* Computer Science \& Engineering (CSE)  

\- \*\*University:\*\* Northern University Bangladesh  

\- \*\*Student Name:\*\* Md. Hasan Sikder  



---



\## 🧠 Abstract



Time management is a critical challenge for students, especially during exam periods. Many students fail to prepare effective study routines due to a lack of structured planning and personalized guidance.  

The Smart Study Routine Generator is a web-based application that generates customized study routines based on subject difficulty, individual weaknesses, priorities, and available study time.  

The system uses a rule-based weighted algorithm to distribute study time efficiently while ensuring balance, breaks, and sustainability. This project aims to improve students’ productivity, reduce burnout, and enhance academic performance.



---



\## ✨ Features



\- 🔐 User Registration with Email OTP Verification

\- 🔑 Secure Login System

\- 📚 Add, Edit, Delete Subjects

\- ⚖️ Priority-based routine generation

\- ☕ Automatic break insertion

\- 🧾 Routine history management

\- 🗑️ Delete single routine or entire history

\- 🎨 Modern Glassmorphism UI

\- 🔒 Login-protected dashboard access



---



\## 🛠️ Technology Stack



\### Frontend

\- HTML5  

\- CSS3 (Glass UI / Glassmorphism)  

\- JavaScript (Vanilla)



\### Backend

\- Python  

\- FastAPI



\### Database

\- MySQL (XAMPP)



\### Tools

\- VS Code  

\- Git \& GitHub  

\- Postman  

\- XAMPP  



---



\## 🗂️ Project Structure



smart-study-routine/

│

├── FrontEnd/

│ ├── index.html

│ └── register.html

│

├── routes/

│ ├── auth.py

│ ├── subjects.py

│ ├── routine.py

│ └── init.py

│

├── database.py

├── main.py

├── .gitignore

└── README.md



---



\## ⚙️ System Workflow



1\. User registers using email (OTP verification required)

2\. User logs in securely

3\. User adds subjects with:

&nbsp;  - Credit

&nbsp;  - Difficulty

&nbsp;  - Weakness level

4\. User provides total available study hours

5\. System calculates priority score

6\. Study time is distributed proportionally

7\. Breaks are inserted automatically

8\. Routine is generated and saved

9\. User can view or delete routine history



---



\## 🧮 Algorithm Overview



Each subject receives a \*\*priority score\*\* based on:

\- Subject difficulty

\- User weakness

\- Credit value



Study hours are distributed proportionally according to these scores.  

This ensures:

\- Fair time distribution

\- Higher focus on difficult subjects

\- Balanced and realistic study plan



---



\## ▶️ How to Run the Project



\### Step 1: Start Backend Server

```bash

cd smart-study-routine

python -m uvicorn main:app --reload

Step 2: Run Frontend



Open FrontEnd/index.html in browser



Make sure backend server is running



🧪 Example Use Case



User adds 4 subjects



Sets total study time as 3 hours



System generates:



Subject-wise study distribution



Breaks between sessions



Routine is saved in history for future review



🚀 Future Scope



Multi-day routine generation



AI-based routine optimization



PDF export feature



Mobile application



Exam countdown-based scheduling



User profile management



📄 Conclusion



The Smart Study Routine Generator provides an effective solution for students to manage their study time efficiently. By combining logical decision-making with modern web technologies, the system offers a practical and scalable tool for academic success.



📚 References



FastAPI Documentation



MySQL Documentation



JavaScript Documentation



GitHub Documentation



👨‍🎓 Author



Md. Hasan Sikder

Department of Computer Science \& Engineering

Northern University Bangladesh



⭐ License



This project is developed for academic and learning purposes.

