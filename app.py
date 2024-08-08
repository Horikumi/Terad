from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/play')
def play():
    play_url = request.args.get('play_url')
    thumb = request.args.get('thumb')
    return render_template('play.html', play_url=play_url, thumb=thumb)

@app.route('/')
def hello_world():
    return 'cheems'

if __name__ == "__main__":
    app.run()
