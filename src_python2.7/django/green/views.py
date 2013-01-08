from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response
import datetime
from django.core.mail import send_mail
from django.contrib.sessions.backends.db import SessionStore

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def prova(request):
    #s = SessionStore()
    html = "<a href='http://127.0.0.1:8000/prova' target='_blank'>Visit W3Schools.com!</a>"
    id = request.session.get('fav_color', False)
    print id
    return HttpResponse(html)
    
    # file charts.py
def simple(request):
    import random
    import django
    import datetime
    
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter
    print "hello"
    
    #print form['subject'].value()
    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
    #return HttpResponse(html)
from django import  forms
TOPIC_CHOICES = (
    ('general', 'General enquiry'),
    ('bug', 'Bug report'),
    ('suggestion', 'Suggestion'),
)

class ContactForm(forms.Form):
    topics = forms.ChoiceField(choices=TOPIC_CHOICES)
    message = forms.CharField()
    sender = forms.EmailField()
    
def contact(request):
    

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
           s = SessionStore()
           message = form.cleaned_data['message']
           topics = form.cleaned_data['topics']
           sender = form.cleaned_data['sender']
           request.session['fav_color'] = sender
           s.save()
           return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm()
    return render_to_response('contact.html', {'form': form})
