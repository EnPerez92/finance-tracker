from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from .extensions import db
from .models import User, Transaction

CATEGORIES = ["Rent", "Groceries", "Dining", "Gas", "Bills", "Savings", "School", "Other"]

def register_routes(app):

    @app.route("/")
    @login_required
    def dashboard():
        txs = Transaction.query.filter_by(user_id=current_user.id).all()
        income = sum(t.amount for t in txs if t.kind == "income")
        expenses = sum(t.amount for t in txs if t.kind == "expense")
        net = income - expenses
        return render_template("dashboard.html", income=income, expenses=expenses, net=net)

    @app.route("/transactions", methods=["GET", "POST"])
    @login_required
    def transactions():
        if request.method == "POST":
            tx = Transaction(
                user_id=current_user.id,
                kind=request.form["kind"],
                amount=float(request.form["amount"]),
                category=request.form["category"],
                description=request.form.get("description", ""),
                date=request.form["date"]
            )
            db.session.add(tx)
            db.session.commit()
            flash("Transaction added!", "success")
            return redirect(url_for("transactions"))

        txs = Transaction.query.filter_by(user_id=current_user.id).all()
        return render_template("transactions.html", txs=txs, categories=CATEGORIES)

    @app.route("/delete/<int:tx_id>", methods=["POST"])
    @login_required
    def delete(tx_id):
        tx = Transaction.query.filter_by(id=tx_id, user_id=current_user.id).first_or_404()
        db.session.delete(tx)
        db.session.commit()
        flash("Deleted!", "info")
        return redirect(url_for("transactions"))

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            email = request.form["email"].lower().strip()
            password = request.form["password"]

            if User.query.filter_by(email=email).first():
                flash("Email already exists.", "danger")
                return redirect(url_for("register"))

            user = User(email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Account created. Please log in.", "success")
            return redirect(url_for("login"))

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form["email"].lower().strip()
            password = request.form["password"]

            user = User.query.filter_by(email=email).first()
            if not user or not user.check_password(password):
                flash("Invalid login.", "danger")
                return redirect(url_for("login"))

            login_user(user)
            return redirect(url_for("dashboard"))

        return render_template("login.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))
