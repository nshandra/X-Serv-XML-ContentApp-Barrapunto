from django.http import HttpResponse, HttpResponseNotFound
from ContentApp.models import Pages, RSS
from django.shortcuts import render
import parser_rss_barrapunto
import urllib.request
import sys


def update(request):
    parser_rss_barrapunto.parse()
    return HttpResponse("Barrapunto RSS db updated.")


def show_links():
    rss = RSS.objects.all()[:5]
    resp = "<br><br>Barrapunto links:<br>"
    for item in rss:
        resp += item.link
    return resp


def main(request):
    resp = "Available pages: "
    pages = Pages.objects.all()
    for page in pages:
        resp += "<br><a href=/" + page.name + ">" + page.name + "</a>"
    return HttpResponse(resp)


def get_page(request, requested_name):
    try:
        resp = Pages.objects.get(name=requested_name).page
        resp += show_links()
        return HttpResponse(resp)
    except Pages.DoesNotExist:
        return HttpResponseNotFound("<h1>Page does not exist.</h1>")
