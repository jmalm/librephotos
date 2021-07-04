import pyvips
import os
import ownphotos.settings
from api.util import logger
import subprocess

def isRawPicture(path):
    fileextension = os.path.splitext(path)[1]
    rawformats = [".RWZ",".CR2",".NRW",".EIP",".RAF",".ERF",".RW2",".NEF",".ARW",".K25",".DNG",".SRF",".DCR",".RAW",".CRW",".BAY",".3FR",".CS1",".MEF",".ORF",".ARI",".SR2",".KDC",".MOS",".MFW",".FFF",".CR3",".SRW",".RWL",".J6I",".KC2",".X3F",".MRW",".IIQ",".PEF",".CXI",".MDC"]
    return fileextension.upper() in rawformats

def createThumbnailForRaw(inputPath, outputHeight, outputPath, hash, fileType):
    completeOutputPath = os.path.join(ownphotos.settings.MEDIA_ROOT,outputPath, hash + ".jpg").strip()
    subprocess.call(['darktable-cli', inputPath, completeOutputPath, "--height", str(outputHeight)])
    return completeOutputPath

def createThumbnail(inputPath, outputHeight, outputPath, hash, fileType):
    if(isRawPicture(inputPath)):
        return createThumbnailForRaw(inputPath, outputHeight, outputPath, hash, fileType)
    else:
        x = pyvips.Image.thumbnail(inputPath, 10000, height=outputHeight, size=pyvips.enums.Size.DOWN)
        completePath = os.path.join(ownphotos.settings.MEDIA_ROOT, outputPath, hash + fileType).strip()
        x.write_to_file(completePath)
        return completePath

def createAnimatedThumbnail(inputPath, outputHeight, outputPath, hash, fileType):
    output = os.path.join(ownphotos.settings.MEDIA_ROOT, outputPath, hash + fileType).strip()
    subprocess.call(['ffmpeg', '-i', inputPath, '-to', '00:00:05', '-vcodec', 'libx264', '-crf', '20', '-an', '-filter:v', ('scale=-2:' + str(outputHeight)), output])

def createThumbnailForVideo(inputPath, outputPath, hash, fileType):
    subprocess.call(['ffmpeg', '-i', inputPath, '-ss', '00:00:00.000', '-vframes', '1', os.path.join(ownphotos.settings.MEDIA_ROOT,outputPath, hash + fileType).strip()])

def doesStaticThumbnailExists(outputPath, hash):
    return os.path.exists(os.path.join(ownphotos.settings.MEDIA_ROOT, outputPath, hash + ".webp").strip())

def doesVideoThumbnailExists(outputPath, hash):
    return os.path.exists(os.path.join(ownphotos.settings.MEDIA_ROOT, outputPath, hash + ".mp4").strip())