################################################## 
# PlacementService_services.py 
# generated by ZSI.generate.wsdl2python
##################################################


from PlacementService_services_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
import ZSI

# Locator
class PlacementServiceLocator:
    PlacementServiceInterface_address = "https://www.google.com:443/apis/ads/publisher/v201104/PlacementService"
    def getPlacementServiceInterfaceAddress(self):
        return PlacementServiceLocator.PlacementServiceInterface_address
    def getPlacementServiceInterface(self, url=None, **kw):
        return PlacementServiceSoapBindingSOAP(url or PlacementServiceLocator.PlacementServiceInterface_address, **kw)

# Methods
class PlacementServiceSoapBindingSOAP:
    def __init__(self, url, **kw):
        kw.setdefault("readerclass", None)
        kw.setdefault("writerclass", None)
        # no resource properties
        self.binding = client.Binding(url=url, **kw)
        # no ws-addressing

    # op: createPlacement
    def createPlacement(self, request):
        if isinstance(request, createPlacementRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(createPlacementResponse.typecode)
        return response

    # op: createPlacements
    def createPlacements(self, request):
        if isinstance(request, createPlacementsRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(createPlacementsResponse.typecode)
        return response

    # get: getPlacement
    def getPlacement(self, request):
        if isinstance(request, getPlacementRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getPlacementResponse.typecode)
        return response

    # get: getPlacementsByStatement
    def getPlacementsByStatement(self, request):
        if isinstance(request, getPlacementsByStatementRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(getPlacementsByStatementResponse.typecode)
        return response

    # op: performPlacementAction
    def performPlacementAction(self, request):
        if isinstance(request, performPlacementActionRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(performPlacementActionResponse.typecode)
        return response

    # op: updatePlacement
    def updatePlacement(self, request):
        if isinstance(request, updatePlacementRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(updatePlacementResponse.typecode)
        return response

    # op: updatePlacements
    def updatePlacements(self, request):
        if isinstance(request, updatePlacementsRequest) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="", **kw)
        # no output wsaction
        response = self.binding.Receive(updatePlacementsResponse.typecode)
        return response

createPlacementRequest = ns0.createPlacement_Dec().pyclass

createPlacementResponse = ns0.createPlacementResponse_Dec().pyclass

createPlacementsRequest = ns0.createPlacements_Dec().pyclass

createPlacementsResponse = ns0.createPlacementsResponse_Dec().pyclass

getPlacementRequest = ns0.getPlacement_Dec().pyclass

getPlacementResponse = ns0.getPlacementResponse_Dec().pyclass

getPlacementsByStatementRequest = ns0.getPlacementsByStatement_Dec().pyclass

getPlacementsByStatementResponse = ns0.getPlacementsByStatementResponse_Dec().pyclass

performPlacementActionRequest = ns0.performPlacementAction_Dec().pyclass

performPlacementActionResponse = ns0.performPlacementActionResponse_Dec().pyclass

updatePlacementRequest = ns0.updatePlacement_Dec().pyclass

updatePlacementResponse = ns0.updatePlacementResponse_Dec().pyclass

updatePlacementsRequest = ns0.updatePlacements_Dec().pyclass

updatePlacementsResponse = ns0.updatePlacementsResponse_Dec().pyclass
