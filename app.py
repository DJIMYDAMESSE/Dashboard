#Flask
from flask import Flask, render_template, request, url_for, flash, redirect

#Graph
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

#Perso
from graph import Graphs




#FLASK
app = Flask(__name__)




@app.route('/', methods=['POST', 'GET'])
def main():
    bar = Graphs().map()
    return render_template("main.html", plot=bar, plot2=bar)