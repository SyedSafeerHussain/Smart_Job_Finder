from flask import Flask, render_template, request
from scraper.helper import save_to_csv, read_csv
from scraper import guru, pph, freelancer
import os

app = Flask(__name__)

# Create data directory if not exists
if not os.path.exists('data'):
    os.makedirs('data')

@app.route('/', methods=['GET', 'POST'])
def index():
    jobs = []
    platform = None
    
    if request.method == 'POST':
        site = request.form.get('site')
        keyword = request.form.get('keyword')
        platform = site
        
        if site == 'guru':
            jobs = guru.scrape(keyword)
            save_to_csv(jobs, "guru.csv")
        elif site == 'pph':
            jobs = pph.scrape(keyword)
            save_to_csv(jobs, "pph.csv")
        elif site == 'freelancer':
            jobs = freelancer.scrape(keyword)
            save_to_csv(jobs, "freelancer.csv")
    
    return render_template('index.html', jobs=jobs, platform=platform)

if __name__ == "__main__":
    app.run(debug=True)