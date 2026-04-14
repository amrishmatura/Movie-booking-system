# Online Movie Ticket Booking System 🍿

A premium, interactive web application that allows users to seamlessly browse movies, select cinema seats dynamically, and process ticket bookings. The platform features an administrative dashboard to manage theaters, screens, and shows globally. 

Built completely with **Python Django** and styled with **Tailwind CSS**.

## ✨ Key Features
- **User Authentication:** Secure registration and login portals mapped to the internal Django Auth schema.
- **Interactive Seat Matrix:** Visual, click-based theater mapping allowing users to pinpoint precise seats. Cart details auto-compute dynamically in real-time.
- **Admin Automation:** Creating a Screen dimensions auto-spawns bulk seats instantaneously into the database, dramatically reducing box-office deployment overhead.
- **Zero-Config Database:** Natively utilizes SQLite3 for absolute portability without demanding local SQL server dependency.
- **Premium UI:** Glassmorphic design layers using Tailwind CSS providing a modern aesthetic.

## 🛠️ Technology Stack
* **Backend:** Python + Django MVT Framework
* **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript
* **Database:** SQLite3

## 🚀 How to Run Locally 

### 1. Clone the repository
```bash
git clone https://github.com/amrishmatura/Movie-booking-system.git
cd Movie-booking-system
```

### 2. Set up the Virtual Environment & Dependencies
*(Assuming Python is installed locally)*
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\Activate.ps1
# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Apply Database Migrations
```bash
python manage.py migrate
```

### 4. Create an Admin Account (Optional)
```bash
python manage.py createsuperuser
```

### 5. Run the Server
```bash
python manage.py runserver
```
Navigate to `http://127.0.0.1:8000/` in your browser to view the application!

---
*Created for CSN301 Software Engineering (Even Semester, 2026).*
