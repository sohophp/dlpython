# -*- coding=utf-8 -*-
from io import StringIO
import os
from pprint import pprint
import re
import subprocess
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
# 首页


def index(request):
    if(request.method == "POST"):
        return info(request)

    return render(request, 'downloader/index.html')

# POST 表单返回结果


def info(request):
    result = {
        'thumbnail': '',
        'download': '',
        'status': 0,
        'formats': [],
        'title': ''
    }

    url = request.POST.get('url', '')

    if(url == ''):
        result['message'] = _('Please enter the url')
        return JsonResponse(result)

    os.system('LC_AL=en_US.UTF-8')
    call = subprocess.run(['youtube-dl', '--get-title', url],
                          stdout=subprocess.PIPE, text=True)
    title = call.stdout.strip()
    if(title == ''):
        result['message'] = "标题获取失败"
        return JsonResponse(result)

    result['title'] = title

    call = subprocess.run(
        ['youtube-dl', '--get-thumbnail', url], stdout=subprocess.PIPE, text=True)
    thumbnail = call.stdout.strip()
    if(thumbnail == ''):
        result['message'] = "缩略图获取失败"
        return JsonResponse(result)
    request.session['download_url'] = url
    result['thumbnail'] = thumbnail
    result['formats'] = listFormats(url)
    result['status'] = 1
    result['download'] = reverse('downloader:download', args=(0,))
    return JsonResponse(result)

# 只留Mp4单个视频


def isMp4(string: str):
    return re.search(r'mp4', string, re.M | re.I) and not re.search('only', string, re.M | re.I)

# 获取格式列表


def listFormats(url: str):
    call = subprocess.run(
        ['youtube-dl', '--list-formats', url], stdout=subprocess.PIPE, text=True)
    output = call.stdout.strip()
    if(output == ''):
        return []
    formats = re.split("[\r\n]+", output)[2:]
    listFormats = filter(isMp4, formats)
    formats = []
    for line in listFormats:
        matched = re.search(
            r'^(?P<formatCode>\d+) (?P<note>.*?)$',
            line,
            re.M
        )
        if(matched):
            item = {}
            item['formatCode'] = matched.group('formatCode')
            item['title'] = matched.group('note')
            item['url'] = reverse('downloader:download',
                                  args=(matched.group('formatCode'),))
            formats.append(item)

    return formats

# 下载视频


def download(request, formatCode):

    url = request.session.get('download_url', '')
    if(url == ''):
        raise Http404("Url Not Found!")
    format = 'best[ext=mp4]/best'
    if(formatCode != '0'):
        format = formatCode
    os.system('LC_ALL=en_US.UTF-8')
    cmd = ['youtube-dl', '--no-playlist', '--no-cache-dir', '--abort-on-error',
           '--limit-rate=2M', '--max-filesize=1000M', '--max-downloads=1', '-f "%s"' % format,
           '--get-filename', '-o "%(title)s.%(ext)s"',  '--restrict-filenames', '"%s"' % url]

    output = subprocess.run(" ".join(
        cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if(output.stderr != ''):
        return HttpResponse(output.stderr)

    filename = output.stdout.strip()

    if(filename == ''):
        raise Http404('Filename Not Found!')
    cmd = ['youtube-dl', '--no-playlist', '--no-cache-dir', '--abort-on-error',
           '--limit-rate=1M', '--max-filesize=1000M', '--max-downloads=1',
           '-f "%s"' % format, '-o -',  '"%s"' % url]
    # cmd=['cat',__file__]
    proc = subprocess.Popen(" ".join(cmd), shell=True, stdout=subprocess.PIPE)
    response = FileResponse(proc.stdout, as_attachment=True,
                            filename="{}".format(filename))
    return response
