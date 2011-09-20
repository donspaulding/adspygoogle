################################################## 
# ReportService_services.py 
# generated by ZSI.generate.wsdl2python
##################################################


from ReportService_services_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
import ZSI

# Locator
class ReportServiceLocator:
    ReportServiceInterface_address = "https://www.google.com:443/apis/ads/publisher/v201107/ReportService"
    def getReportServiceInterfaceAddress(self):
        return ReportServiceLocator.ReportServiceInterface_address
    def getReportServiceInterface(self, url=None, **kw):
        return ReportServiceSoapBindingSOAP(url or ReportServiceLocator.ReportServiceInterface_address, **kw)

# Methods
class ReportServiceSoapBindingSOAP:
    def __init__(self, url, **kw):
        kw.setdefault("readerclass", None)
        kw.setdefault("writerclass", None)
        # no resource properties
        self.binding = client.Binding(url=url, **kw)
        # no ws-addressing

    # get: getReportDownloadURL
    def getReportDownloadURL(self, request):
        if isinstance(request, getReportDownloadURLRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getReportDownloadURLResponse.typecode)
        return response

    # get: getReportJob
    def getReportJob(self, request):
        if isinstance(request, getReportJobRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getReportJobResponse.typecode)
        return response

    # op: runReportJob
    def runReportJob(self, request):
        if isinstance(request, runReportJobRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(runReportJobResponse.typecode)
        return response

getReportDownloadURLRequest = ns0.getReportDownloadURL_Dec().pyclass

getReportDownloadURLResponse = ns0.getReportDownloadURLResponse_Dec().pyclass

getReportJobRequest = ns0.getReportJob_Dec().pyclass

getReportJobResponse = ns0.getReportJobResponse_Dec().pyclass

runReportJobRequest = ns0.runReportJob_Dec().pyclass

runReportJobResponse = ns0.runReportJobResponse_Dec().pyclass
