# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response#, get_object_or_404, render
from django.http import HttpResponseRedirect
from m12.models import Pro, Parf,Period
from m12.forms import TstForm
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
'''
def main_form(request):
    print 'edo arxizei i main_form'
    if request.method == 'POST':
        print 'edo pame gia form valid'
        #form = ProForm(data=request.POST)
        if form.is_valid():
            print 'edo sozoume'
            a1 = form.save(commit=False)
            a1.author = request.user
            a1.save()
            return HttpResponseRedirect(a1.get_absolute_url())
    else:
        print 'edo Proform()'
        #form = ProForm()
    return render_to_response('main.html',locals(),context_instance=RequestContext(request))
main_form = login_required(main_form)
'''
def search_form(request):
    return render_to_response('search_form.html')

def search(request):
    if 'q' in request.GET:
        message = u'Κάνατε αναζήτηση για: %s' % request.GET['q']
    else:
        message = u'You submitted an empty form.'
    return render_to_response('searchResult.html',locals())

def spro(request):
    pr = Pro.objects.all()
    return render_to_response('pr.html',locals())

def paroysies(request,xris,per):
    par = Parf.objects.filter(xrisi__xrisi=xris,period__period=per)
    xr = xris
    pe = Period.objects.get(period=per).periodp
    for el in par:
        #el.ppp = ProMis.objects.get(xrisi__xrisi=xris,)
        tmppromis = el.pro.promis_set.all()
        if not tmppromis:
            el.ted = u'Κενό'
        else:
            el.ted = tmppromis[0].poso
        tv = el.calc()
        el.tmis = tv['mis']
        el.tikaenos  = tv['ikaenos']
        el.tikaetis  = tv['ikaetis']
        el.tika      = tv['ika']
        el.tkenos    = tv['tkenos']
        el.tplir     = tv['plir']
    return render_to_response('paroysies.html',locals())

from reportlab.pdfgen import canvas
from django.http import HttpResponse

def some_view(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response