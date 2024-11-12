from flask import Flask, render_template, request, redirect, url_for, session, flash

def logout() :
    session.pop("username")
    session.clear()
    session.modified = True
    return redirect(url_for('logout'))